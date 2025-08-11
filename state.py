import flet as ft
import os
from dataclasses import dataclass, field
from typing import Literal, Dict, List, Tuple
from pypdf import PageObject


@dataclass
class SelectedFile:
    file: ft.FilePickerFile
    pages: List[PageObject]
    output_pages_setting: Dict[int, bool]
    is_division: bool = field(default_factory=bool)

    def on_setting_edit(self, e: ft.Event[ft.TextButton], setting: Dict[int, bool]):
        self.output_pages_setting = setting.copy()
        self.is_division = any(self.output_pages_setting.values())


@dataclass
class AppGlobalState:
    compressed_dir: str = "compressed"
    selected_files: List[SelectedFile] = field(default_factory=list)
    compressed_file_paths: Dict[str, int] = field(default_factory=dict[str, int])
    theme_mode: Literal[ft.ThemeMode.LIGHT] | Literal[ft.ThemeMode.DARK] = (
        ft.ThemeMode.LIGHT
    )
    theme_icon: ft.Icons = ft.Icons.LIGHT_MODE
    quality: Literal["screen", "ebook", "printer"] = "screen"
    tab_selected: str = "Selected Files"
    tab_options: List[str] = field(
        default_factory=lambda: ["Selected Files", "Compress Files"]
    )
    is_join: bool = field(default_factory=bool)

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
        e.page.shared_preferences.set("theme", self.theme_mode) # type: ignore

    def set_quality(self, e: ft.Event[ft.Dropdown] | None):
        self.quality = e.control.value  # type: ignore

    def tab_changed(self, e: ft.Event[ft.TabBar]):
        self.tab_selected = self.tab_options[e.data] # type: ignore

    def compressed_tab_move(self):
        self.tab_selected = self.tab_options[1]

    def select_file_remove(self, e: ft.Event[ft.IconButton], file: SelectedFile):
        self.selected_files.remove(file)

    def compressed_file_remove(self, e: ft.Event[ft.IconButton], file_path: str):
        self.compressed_file_paths.pop(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)

    def handle_join_change(self, e: ft.Event[ft.Switch]):
        self.is_join = e.control.value

    def select_pages(self, e: ft.Event[ft.TextButton], idx: int, pages: list[PageObject]):
        self.selected_files[idx].pages = pages


@dataclass
class SidebarState:
    pb: ft.ProgressBar = ft.ProgressBar(value=0)

    def update_progress(self, comp: int, all: int):
        self.pb.value = comp / all
        self.pb.update()
