import flet as ft
import shutil
from pathlib import Path

from state import AppGlobalState
from components import Sidebar, SelectFiles, CompressedFiles

APP_NAME = "Python PDF Compressor"


def AppView(state: AppGlobalState, page: ft.Page) -> ft.Container:
    tab = ft.Tabs(
        scrollable=False,
        selected_index=state.tab_options.index(state.tab_selected),
        on_change=state.tab_changed,
        tabs=[ft.Tab(label=tab) for tab in state.tab_options],
    )

    return ft.Container(
        content=ft.Row(
            [
                Sidebar(state, page),  # type: ignore
                ft.Container(
                    content=ft.Column(
                        controls=[
                            tab,
                            (
                                SelectFiles(state)
                                if tab.selected_index == 0
                                else CompressedFiles(state, page)
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        spacing=3,
                    ),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        expand=True,
    )


def main(page: ft.Page):
    global_state = AppGlobalState()
    # global_state.tabs =

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
    )
    page.dark_theme = ft.Theme(
        color_scheme_seed=ft.Colors.GREEN,
    )
    page.title = APP_NAME
    page.padding = 0

    for item in Path(global_state.compressed_dir).iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

    page.add(
        ft.ControlBuilder(global_state, lambda state: AppView(state, page), expand=True)
    )


ft.run(main)
