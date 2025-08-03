import subprocess
from typing import Any
import flet as ft
from state import AppGlobalState
from pathlib import Path


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


def Sidebar(global_state: AppGlobalState, page: ft.Page) -> ft.Container:
    # add to services for file picker
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    async def open_file_picker(e: ft.ControlEvent | None = None):
        files = await file_picker.pick_files_async(
            allow_multiple=True,
            allowed_extensions=["pdf"],
            dialog_title="Select PDF Files",
        )
        if files:
            global_state.selected_files.extend(files)

    async def compress(e: ft.Event[ft.TextButton] | None = None):
        # save_dir = await file_picker.get_directory_path_async(
        #     dialog_title="Select Save Directory"
        # )
        # if not save_dir:
        #     cancel_dlg = ft.AlertDialog(
        #         content=ft.Container(ft.Text("Cancelled!")),
        #         actions=[
        #             ft.TextButton(
        #                 content=ft.Text("OK"),
        #                 on_click=lambda e: e.page.close(cancel_dlg), # type: ignore
        #             )
        #         ],
        #     )
        #     e.page.show_dialog(cancel_dlg)  # type: ignore
        #     return
        save_path_dir = Path(global_state.compressed_dir)

        for file in global_state.selected_files:
            input_path = Path(file.path)  # type: ignore
            output_filename = f"{input_path.stem}_compressed.pdf"
            save_path = save_path_dir / output_filename

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
            global_state.compressed_file_paths.append(str(save_path))

    return ft.Container(
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
                            ft.TextButton(
                                "COMPRESS",
                                on_click=compress,
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
