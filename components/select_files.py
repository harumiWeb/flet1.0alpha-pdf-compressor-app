import flet as ft
from pathlib import Path
import shutil
import tempfile

from state import AppGlobalState, SelectedFile


def PageSelectDialog(sf: SelectedFile):
    __setting = sf.output_pages_setting.copy()

    def handle_switch(e: ft.Event[ft.Switch], idx: int):
        __setting[idx] = e.control.value

    def handle_edit(e: ft.Event[ft.TextButton]):
        sf.on_setting_edit(e, __setting)

    dlg = ft.AlertDialog(
        content=ft.Container(
            ft.Column(
                [
                    ft.Text("Please select the pages to output."),
                    ft.ListView(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"Page {int(idx) + 1}"),
                                    ft.Switch(
                                        value=is_out,
                                        on_change=lambda e, idx=idx: handle_switch(
                                            e, idx
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            )
                            for idx, is_out in sf.output_pages_setting.items()
                        ]
                    ),
                ]
            ),
            height=300,
        ),
        actions=[
            ft.TextButton("OK", on_click=lambda e: (handle_edit(e), e.page.pop_dialog())),  # type: ignore
            ft.TextButton("Cancel", on_click=lambda e: e.page.pop_dialog()),  # type: ignore
        ],
    )
    return dlg


def SelectedFileItem(
    file: SelectedFile, idx: int, global_state: AppGlobalState
) -> ft.SafeArea:
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
                        f"{idx + 1}",
                        style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                        width=30,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Icon(
                        name=ft.Icons.PICTURE_AS_PDF,
                        size=24,
                        color=ft.Colors.RED,
                    ),
                    ft.Text(
                        file.file.name,
                        style=ft.TextStyle(size=16, weight=ft.FontWeight.NORMAL),
                        expand=True,
                    ),
                    ft.Row(
                        controls=[
                            ft.TextButton("Page Select", on_click=lambda e: e.page.show_dialog(PageSelectDialog(file))),  # type: ignore
                            ft.Text(
                                f"{calculate_size(file.file.size)}",
                                style=ft.TextStyle(size=14, color=ft.Colors.GREY),
                                text_align=ft.TextAlign.RIGHT,
                                no_wrap=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                bgcolor=ft.Colors.RED,
                                on_click=lambda e: global_state.select_file_remove(
                                    e, file
                                ),
                                icon_color=ft.Colors.WHITE,
                                tooltip="Deselect",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=1)
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                    ),
                ],
                expand=True,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
        )
    )


def CompressedFileItem(
    file_path: str, origin_size, idx: int, global_state: AppGlobalState
) -> ft.SafeArea:
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
                        f"{idx + 1}",
                        style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                        width=30,
                        text_align=ft.TextAlign.CENTER,
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
                                    ratio if not global_state.is_join else "",
                                    style=ft.TextStyle(
                                        size=14,
                                        color=ft.Colors.WHITE,
                                        word_spacing=3,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ),
                                bgcolor=(
                                    None
                                    if global_state.is_join
                                    else (
                                        ft.Colors.GREEN
                                        if "-" in ratio
                                        else ft.Colors.RED
                                    )
                                ),
                                padding=ft.Padding.symmetric(vertical=5,horizontal=5),
                                border_radius=4,
                            ),
                            ft.Text(
                                f"{calculate_size(file.stat().st_size)}",
                                style=ft.TextStyle(size=14, color=ft.Colors.GREY),
                                text_align=ft.TextAlign.RIGHT,
                                no_wrap=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                bgcolor=ft.Colors.RED,
                                on_click=lambda e: global_state.compressed_file_remove(
                                    e, file_path
                                ),
                                icon_color=ft.Colors.WHITE,
                                tooltip="Deselect",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=1)
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                expand=True,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
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
                                    SelectedFileItem(file, idx, global_state)
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
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        expand=True,
    )


def CompressedFiles(global_state: AppGlobalState, page: ft.Page) -> ft.Container:
    # add to services for file picker
    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    async def save_file(e: ft.Event[ft.TextButton]):
        save_dir = await file_picker.get_directory_path_async(
            dialog_title="Select Save Directory"
        )
        if not save_dir:
            cancel_dlg = ft.AlertDialog(
                content=ft.Container(ft.Text("Cancelled!")),
                actions=[
                    ft.TextButton(
                        content=ft.Text("OK"),
                        on_click=lambda e: e.page.close(cancel_dlg),  # type: ignore
                    )
                ],
            )
            e.page.show_dialog(cancel_dlg)  # type: ignore
            return

        source_dir = Path("compressed")
        destination_dir = Path(save_dir)
        output_zip_name = "compressed_pdf"

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            temp_zip_path = temp_path / output_zip_name

            shutil.make_archive(str(temp_zip_path), "zip", root_dir=str(source_dir))

            zip_file = temp_zip_path.with_suffix(".zip")
            destination_path = destination_dir / zip_file.name

            shutil.move(str(zip_file), str(destination_path))

            success_dlg = ft.AlertDialog(
                content=ft.Container(ft.Text("Saved!")),
                actions=[
                    ft.TextButton(
                        content=ft.Text("OK"),
                        on_click=lambda e: e.page.close(success_dlg),  # type: ignore
                    )
                ],
            )
            e.page.show_dialog(success_dlg)  # type: ignore
        return

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    controls=[
                        ft.Text(
                            "Compressed Files",
                            style=ft.TextStyle(
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                        ft.Row(
                            controls=[
                                ft.TextButton(
                                    "Save Zip",
                                    on_click=save_file,
                                    icon=ft.Icons.SAVE_ALT_OUTLINED,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=(
                                            ft.Colors.GREEN_ACCENT_400
                                            if global_state.compressed_file_paths
                                            else ft.Colors.GREY_300
                                        ),
                                        shape=ft.RoundedRectangleBorder(radius=5),
                                    ),
                                    width=200,
                                    tooltip=(
                                        "Save File"
                                        if global_state.compressed_file_paths
                                        else "Please Compress"
                                    ),
                                    disabled=(
                                        False
                                        if global_state.compressed_file_paths
                                        else True
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            expand=True,
                        ),
                    ]
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ListView(
                                controls=[
                                    CompressedFileItem(
                                        file_path, origin_size, idx, global_state
                                    )
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
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        expand=True,
    )
