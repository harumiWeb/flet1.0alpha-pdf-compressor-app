import subprocess
from typing import Any
import flet as ft
from state import AppGlobalState, SidebarState, SelectedFile
from pathlib import Path
import asyncio
from pypdf import PdfReader, PdfWriter
import tempfile
import webbrowser
import sys
import os

SELECT_FILES_BUTTON_THEME = ft.Theme(
    text_button_theme=ft.TextButtonTheme(
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_ACCENT_700,
            shape=ft.RoundedRectangleBorder(radius=5),
        )
    )
)

COMPRESS_BUTTON_THEME = ft.Theme(
    text_button_theme=ft.TextButtonTheme(
        style=ft.ButtonStyle(
            color=(ft.Colors.WHITE),
            bgcolor=(ft.Colors.GREEN_ACCENT_700),
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=ft.Padding.symmetric(horizontal=20, vertical=18),
        )
    ),
    disabled_color=ft.Colors.GREY,
)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS + "\\" + relative_path # type: ignore
    return os.path.join(os.path.abspath("."), relative_path)


class QualityDropdown(ft.Dropdown):
    def __init__(self, global_state: AppGlobalState):
        super().__init__(
            value=global_state.quality,
            options=[
                ft.DropdownOption("screen", "Low"),
                ft.DropdownOption("ebook", "Medium"),
                ft.DropdownOption("printer", "High"),
            ],
            on_change=lambda e: global_state.set_quality(e),
            width=200,
            label="Image Quality",
        )
        self.border_color = (
            ft.Colors.BLACK
            if global_state.theme_mode == ft.ThemeMode.LIGHT
            else ft.Colors.WHITE
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_frozen":
            return
        return super().__setattr__(name, value)


def ProcessingDialog(pb: ft.ProgressBar) -> ft.AlertDialog:
    dlg = ft.AlertDialog(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("compressing..."),
                        ]
                    ),
                    pb,
                ]
            ),
            height=200,
        ),
        modal=True,
        title="Processing",
    )
    return dlg


def Sidebar(global_state: AppGlobalState, page: ft.Page) -> ft.Container:
    my_state = SidebarState()

    # add to services for file picker
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    pd = ProcessingDialog(my_state.pb)

    async def open_file_picker(e: ft.Event[ft.TextButton] | None = None):
        files = await file_picker.pick_files_async(
            allow_multiple=True,
            allowed_extensions=["pdf"],
            dialog_title="Select PDF Files",
        )
        if files:
            existing_paths = {sf.file.path for sf in global_state.selected_files}

            for file in files:
                if file.path in existing_paths:
                    continue
                reader = PdfReader(str(file.path))
                global_state.selected_files.append(
                    SelectedFile(
                        file=file,
                        pages=reader.pages,
                        output_pages_setting={
                            idx: True for idx, _ in enumerate(reader.pages)
                        },
                    )
                )

    def run_ghostscript(input_paths: list[Path], output_path: Path):
        subprocess.run(
            [
                resource_path(r".\assets\bin\gswin64c"),
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{global_state.quality}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={str(output_path)}",
            ]
            + [str(p) for p in input_paths],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    def extract_pages_to_temp_pdf(sf: SelectedFile, tmp_dir: Path) -> Path:
        idx = global_state.selected_files.index(sf)
        true_idxs = [
            k
            for k, v in global_state.selected_files[idx].output_pages_setting.items()
            if v
        ]

        writer = PdfWriter()
        for page_num in true_idxs:
            writer.add_page(sf.pages[page_num])

        file_path = Path(str(sf.file.path))
        output_path = tmp_dir / file_path.name

        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path

    def record_compression(save_path: Path, original_size: int):
        global_state.compressed_file_paths[str(save_path)] = original_size
        my_state.update_progress(
            len(global_state.compressed_file_paths),
            len(global_state.selected_files),
        )

    def single_compress(file: ft.FilePickerFile, save_path_dir: Path):
        input_path = Path(file.path)  # type: ignore
        output_path = save_path_dir / f"{input_path.stem}.pdf"
        origin_size = input_path.stat().st_size

        run_ghostscript([input_path], output_path)
        record_compression(output_path, origin_size)

    def division_pdf(sf: SelectedFile, save_path_dir: Path):
        with tempfile.TemporaryDirectory() as dir:
            tmp_dir = Path(dir)
            temp_pdf = extract_pages_to_temp_pdf(sf, tmp_dir)

            save_path = save_path_dir / temp_pdf.name
            origin_size = Path(str(sf.file.path)).stat().st_size

            run_ghostscript([temp_pdf], save_path)
            record_compression(save_path, origin_size)

    def compress_and_join(selected_files: list[SelectedFile], save_path_dir: Path):
        output_path = save_path_dir / "joined.pdf"
        temp_pdfs: list[Path] = []

        with tempfile.TemporaryDirectory() as dir:
            tmp_dir = Path(dir)
            for sf in selected_files:
                if sf.is_division:
                    temp_pdf = extract_pages_to_temp_pdf(sf, tmp_dir)
                    temp_pdfs.append(temp_pdf)

            input_paths = (
                temp_pdfs
                if temp_pdfs
                else [Path(str(sf.file.path)) for sf in selected_files]
            )
            run_ghostscript(input_paths, output_path)
            record_compression(output_path, output_path.stat().st_size)

    async def handle_compress_click(e: ft.Event[ft.TextButton]):
        page.show_dialog(pd)
        await asyncio.sleep(0.001)

        save_path_dir = Path(global_state.compressed_dir)

        if global_state.is_join:
            compress_and_join(global_state.selected_files, save_path_dir)
        else:
            for file in global_state.selected_files:
                if file.is_division:
                    division_pdf(file, save_path_dir)
                    await asyncio.sleep(0.001)
                else:
                    single_compress(file.file, save_path_dir)
                    await asyncio.sleep(0.001)

        page.pop_dialog()
        page.update()

    def await_tab_change(e: ft.Event[ft.TextButton]):
        global_state.compressed_tab_move()

    def preview_license(e: ft.Event[ft.TextButton]):
        license_path = Path(resource_path("assets/LICENSE.md"))
        try:
            license_text = license_path.read_text(encoding="utf-8")
        except Exception as ex:
            license_text = f"ライセンス情報の読み込みに失敗しました。\n\n{ex}"

        dlg = ft.AlertDialog(
            content=ft.Container(
                ft.Column([ft.Markdown(license_text)], scroll=ft.ScrollMode.AUTO)
            ),
            modal=True,
            actions=[ft.TextButton("OK", on_click=lambda e: page.pop_dialog())],
        )
        page.show_dialog(dlg)

    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=global_state.theme_icon,
                                on_click=global_state.toggle_theme,
                                tooltip="Toggle Theme",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        expand=True,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                ft.TextButton(
                                    "Select Files",
                                    on_click=open_file_picker,
                                    icon=ft.Icons.FOLDER_OPEN,
                                    width=200,
                                    tooltip="Select PDF Files",
                                ),
                                theme=SELECT_FILES_BUTTON_THEME,
                                dark_theme=SELECT_FILES_BUTTON_THEME,
                            ),
                            QualityDropdown(global_state),
                            ft.Row(
                                [
                                    ft.Text("Merge all PDFs"),
                                    ft.Switch(
                                        value=global_state.is_join,
                                        on_change=global_state.handle_join_change,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(
                                ft.TextButton(
                                    "COMPRESS",
                                    on_click=lambda e: (
                                        asyncio.create_task(
                                            handle_compress_click(e),
                                        ),
                                        await_tab_change(e),
                                    ),
                                    icon=ft.Icons.COMPRESS,
                                    tooltip=(
                                        "Start Compression"
                                        if global_state.selected_files
                                        else "No files selected"
                                    ),
                                    width=200,
                                    disabled=not global_state.selected_files,
                                ),
                                theme=COMPRESS_BUTTON_THEME,
                                dark_theme=COMPRESS_BUTTON_THEME,
                            ),
                            ft.Column(
                                [
                                    ft.Container(
                                        ft.Row(
                                            [
                                                ft.TextButton(
                                                    "GitHub",
                                                    on_click=lambda e: webbrowser.open_new(
                                                        "https://github.com/harumiWeb/flet1.0alpha-pdf-compressor-app"
                                                    ),
                                                    icon=ft.Image(
                                                        src=(
                                                            resource_path("assets/github-mark-white.png")
                                                            if page.theme_mode
                                                            == ft.ThemeMode.DARK
                                                            else resource_path("assets/github-mark.png")
                                                        ),
                                                        height=20,
                                                    ),
                                                )
                                            ]
                                        )
                                    ),
                                    ft.TextButton(
                                        "LICENSE",
                                        on_click=preview_license,
                                        icon=ft.Icons.ATTACH_FILE,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                                expand=True,
                            ),
                        ],
                        spacing=20,
                    ),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=10,
        ),
        alignment=ft.Alignment.TOP_CENTER,
        padding=ft.Padding.all(10),
        bgcolor=(
            ft.Colors.BLUE_GREY_100
            if global_state.theme_mode == ft.ThemeMode.LIGHT
            else ft.Colors.BLACK
        ),
        width=220,
    )
    return sidebar
