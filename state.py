import flet as ft
from dataclasses import dataclass, field
from typing import Literal, Dict, List, Tuple


@dataclass
class AppGlobalState:
    compressed_dir: str = "compressed"
    selected_files: List[ft.FilePickerFile] = field(default_factory=list)
    compressed_file_paths: Dict[str, int] = field(default_factory=dict[str, int])
    theme_mode: Literal[ft.ThemeMode.LIGHT] | Literal[ft.ThemeMode.DARK] = (
        ft.ThemeMode.LIGHT
    )
    theme_icon: ft.Icons = ft.Icons.LIGHT_MODE
    quality: Literal["screen", "ebook", "printer"] = "screen"
    tab_selected: str = "Selected Files"
    tab_options: List[str] = field(default_factory=lambda: ["Selected Files", "Compress Files"])

    def toggle_theme(self, e: ft.ControlEvent | None = None):
        self.theme_mode = (
            ft.ThemeMode.DARK
            if self.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.theme_icon = (
            ft.Icons.DARK_MODE
            if self.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.LIGHT_MODE
        )
        e.page.theme_mode = self.theme_mode  # type: ignore

    def set_quality(self, e: ft.Event[ft.Dropdown] | None):
        self.quality = e.control.value  # type: ignore

    def tab_changed(self, e: ft.Event[ft.Tabs]):
        self.tab_selected = self.tab_options[e.control.selected_index]


@dataclass
class SidebarState:
    pb: ft.ProgressBar = ft.ProgressBar(value=0)

    def update_progress(self, comp: int, all: int):
        self.pb.value = comp / all
        self.pb.update()
