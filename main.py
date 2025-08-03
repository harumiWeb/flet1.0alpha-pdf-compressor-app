import flet as ft

from state import AppGlobalState
from components import Sidebar, SelectFiles, CompressedFiles

APP_NAME = "Python PDF Compressor"


def AppView(state: AppGlobalState, page: ft.Page) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                Sidebar(state, page),  # type: ignore
                ft.Container(
                    content=ft.Column(
                        controls=[
                            SelectFiles(state),
                            ft.Divider(),
                            CompressedFiles(state),
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

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
    )
    page.dark_theme = ft.Theme(
        color_scheme_seed=ft.Colors.GREEN,
    )
    page.title = APP_NAME
    page.padding = 0

    page.add(ft.ControlBuilder(global_state, lambda state: AppView(state, page), expand=True))


ft.run(main)
