import flet as ft
from pathlib import Path

from state import AppGlobalState


def SelectedFileItem(file: ft.FilePickerFile, idx: int) -> ft.SafeArea:
    def calculate_size(size: int) -> str:
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    return ft.SafeArea(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        f"{idx + 1}.",
                        style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                    ),
                    ft.Icon(
                        name=ft.Icons.PICTURE_AS_PDF,
                        size=24,
                        color=ft.Colors.RED,
                    ),
                    ft.Text(
                        file.name,
                        style=ft.TextStyle(size=16, weight=ft.FontWeight.NORMAL),
                        expand=True,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{calculate_size(file.size)}",
                                style=ft.TextStyle(size=14, color=ft.Colors.GREY),
                                text_align=ft.TextAlign.RIGHT,
                                no_wrap=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                expand=True,
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        )
    )


def CompressedFileItem(file_path: str, idx: int) -> ft.SafeArea:
    file = Path(file_path)

    def calculate_size(size: int) -> str:
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
        
    # TODO: 圧縮率表示

    return ft.SafeArea(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        f"{idx + 1}.",
                        style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                    ),
                    ft.Icon(
                        name=ft.Icons.PICTURE_AS_PDF,
                        size=24,
                        color=ft.Colors.RED,
                    ),
                    ft.Text(
                        file.name,
                        style=ft.TextStyle(size=16, weight=ft.FontWeight.NORMAL),
                        expand=True,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{calculate_size(file.stat().st_size)}",
                                style=ft.TextStyle(size=14, color=ft.Colors.GREY),
                                text_align=ft.TextAlign.RIGHT,
                                no_wrap=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                expand=True,
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        )
    )


def SelectFiles(global_state: AppGlobalState) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Selected Files",
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ListView(
                                controls=[
                                    SelectedFileItem(file, idx)
                                    for idx, file in enumerate(
                                        global_state.selected_files
                                    )
                                ],
                                expand=True,
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                    border=ft.Border.all(
                        color=ft.Colors.GREY_300,
                        width=1,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
        expand=True,
    )


def CompressedFiles(global_state: AppGlobalState) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Compressed Files",
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ListView(
                                controls=[
                                    CompressedFileItem(file_path, idx)
                                    for idx, file_path in enumerate(
                                        global_state.compressed_file_paths
                                    )
                                ],
                                expand=True,
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                    border=ft.Border.all(
                        color=ft.Colors.GREY_300,
                        width=1,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
        expand=True,
    )
