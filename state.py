import flet as ft
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class AppGlobalState():
    selected_files: list[ft.FilePickerFile] = field(default_factory=list)
    compressed_file_paths: list[str] = field(default_factory=list)
    theme_mode: Literal[ft.ThemeMode.LIGHT] | Literal[ft.ThemeMode.DARK] = ft.ThemeMode.LIGHT
    theme_icon: ft.Icons = ft.Icons.LIGHT_MODE
    quality: Literal["screen", "ebook", "printer"] = "screen"

    def toggle_theme(self, e: ft.ControlEvent | None = None):
        self.theme_mode = ft.ThemeMode.DARK if self.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.theme_icon = (
            ft.Icons.DARK_MODE if self.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        )
        e.page.theme_mode = self.theme_mode  # type: ignore

    def set_quality(self, e: ft.Event[ft.Dropdown] | None):
        self.quality = e.control.value # type: ignore