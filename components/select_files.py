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


def CompressedFileItem(file_path: str, origin_size, idx: int) -> ft.SafeArea:
    file = Path(file_path)
    compressed_size = file.stat().st_size

    def calculate_size(size: int) -> str:
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    def calculate_ratio(original: int, compressed: int) -> str:
        if original == 0:
            return "N/A"
        ratio = 100 - ((compressed / original) * 100)
        return f"-{ratio:.1f}%" if ratio > 0 else "+" + f"{ratio:.1f}%".replace("-", "")

    ratio = calculate_ratio(origin_size, compressed_size)

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
                            ft.Container(
                                content=ft.Text(
                                    ratio,
                                    style=ft.TextStyle(size=14, color=ft.Colors.WHITE, word_spacing=3, weight=ft.FontWeight.BOLD),
                                ),
                                bgcolor=(
                                    ft.Colors.GREEN if "-" in ratio else ft.Colors.RED
                                ),
                                padding=ft.padding.symmetric(5,5),
                                border_radius=4
                            ),
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
                                    CompressedFileItem(file_path, origin_size, idx)
                                    for idx, (file_path, origin_size) in enumerate(
                                        global_state.compressed_file_paths.items()
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
