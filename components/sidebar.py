import subprocess
from typing import Any
import flet as ft
from state import AppGlobalState, SidebarState, SelectedFile
from pathlib import Path
import asyncio
from pypdf import PdfReader


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

    async def open_file_picker(e: ft.ControlEvent | None = None):
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

    def single_compress(file: ft.FilePickerFile, save_path_dir: Path):
        input_path = Path(file.path)  # type: ignore
        output_filename = f"{input_path.stem}.pdf"
        save_path = save_path_dir / output_filename
        origin_size = input_path.stat().st_size

        subprocess.run(
            [
                r".\assets\bin\gswin64c",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{global_state.quality}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={str(save_path)}",
                str(input_path),
            ]
        )

        global_state.compressed_file_paths[str(save_path)] = origin_size

        my_state.update_progress(
            len(global_state.compressed_file_paths),
            len(global_state.selected_files),
        )

    def compress_and_join(selected_files: list[SelectedFile], save_path_dir: Path):
        output_filename = "joined.pdf"
        save_path = save_path_dir / output_filename

        pdf_paths: list[str] = [str(file.file.path) for file in selected_files]

        result = subprocess.run(
            [
                r".\assets\bin\gswin64c",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS=/{global_state.quality}",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={str(save_path)}",
            ]
            + pdf_paths
        )

        global_state.compressed_file_paths[str(save_path)] = save_path.stat().st_size

        my_state.update_progress(
            len(global_state.compressed_file_paths),
            len(global_state.selected_files),
        )

    async def handle_compress_click(e: ft.Event[ft.TextButton]):
        page.show_dialog(pd)
        await asyncio.sleep(0.001)

        save_path_dir = Path(global_state.compressed_dir)

        if global_state.is_join:
            compress_and_join(global_state.selected_files, save_path_dir)
        else:
            for file in global_state.selected_files:
                single_compress(file.file, save_path_dir)
                await asyncio.sleep(0.001)

        page.pop_dialog()
        page.update()

    def await_tab_change(e: ft.Event[ft.TextButton]):
        global_state.compressed_tab_move()

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
                            ft.TextButton(
                                "Select Files",
                                on_click=open_file_picker,
                                icon=ft.Icons.FOLDER_OPEN,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_ACCENT_700,
                                    shape=ft.RoundedRectangleBorder(radius=5),
                                ),
                                width=200,
                                tooltip="Select PDF Files",
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
                            ft.TextButton(
                                "COMPRESS",
                                on_click=lambda e: (
                                    asyncio.create_task(
                                        handle_compress_click(e),
                                    ),
                                    await_tab_change(e),
                                ),
                                icon=ft.Icons.COMPRESS,
                                style=ft.ButtonStyle(
                                    color=(
                                        ft.Colors.WHITE
                                        if global_state.selected_files
                                        else ft.Colors.GREY
                                    ),
                                    bgcolor=(
                                        ft.Colors.GREEN_ACCENT_700
                                        if global_state.selected_files
                                        else ft.Colors.GREY_300
                                    ),
                                    shape=ft.RoundedRectangleBorder(radius=5),
                                    padding=ft.padding.symmetric(
                                        horizontal=20, vertical=18
                                    ),
                                ),
                                tooltip=(
                                    "Start Compression"
                                    if global_state.selected_files
                                    else "No files selected"
                                ),
                                width=200,
                                disabled=not global_state.selected_files,
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
        padding=ft.padding.all(10),
        bgcolor=(
            ft.Colors.BLUE_GREY_100
            if global_state.theme_mode == ft.ThemeMode.LIGHT
            else ft.Colors.BLACK
        ),
        width=220,
    )
    return sidebar
