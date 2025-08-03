import flet as ft

from state import AppGlobalState
from components.sidebar import Sidebar

APP_NAME = "Python PDF Compressor"


def AppView(state: AppGlobalState, page: ft.Page) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                Sidebar(state, page),  # type: ignore
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Main Content Area"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        expand=True,
    )


def main(page: ft.Page):
    global_state = AppGlobalState()

    page.theme_mode = global_state.theme_mode  # type: ignore
    page.theme = ft.Theme(
        color_scheme_seed= ft.Colors.BLUE,
    )
    page.dark_theme = ft.Theme(
        color_scheme_seed=ft.Colors.GREEN,
    )
    page.title = APP_NAME
    page.padding = 0
    
    page.add(ft.ControlBuilder(global_state, lambda state: AppView(state, page)))


ft.run(main)
