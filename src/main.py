#!/usr/bin/env python3
"""GTK wallpaper manager application."""

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from pathlib import Path
from typing import Optional  # noqa: F401 (future use)

from utils.constants import APP_ID, APP_TITLE
from utils.storage import StorageManager
from utils.wallpaper_utils import set_wallpaper, restore
from styles.themes import get_theme_css
from components.gallery import Gallery
from components.preferences_dialog import PreferencesDialog
from components.header_bar import HeaderBar
from components.footer_bar import FooterBar


class WallpaperApp(Gtk.Application):
    """Application root."""
    
    def __init__(self):
        super().__init__(application_id=APP_ID)
        self.window = None

        self.config = StorageManager.load_config()
        self.current_dir = Path(restore()).parent if restore() else Path.home()
        self.resize_var = self.config.get("default_resize", "crop")
    
    def do_activate(self):
        """Create and present main window"""
        if not self.window:
            self.window = Gtk.ApplicationWindow(application=self)
            self.window.set_title(APP_TITLE)
            self.window.set_default_size(1200, 800)
            self.window.set_resizable(True)
            self.window.set_css_classes(["main-window"])
            
            self._apply_theme()
            self._setup_main_layout()
            self.gallery.load_directory(str(self.current_dir))
        
        self.window.present()
    
    def _setup_main_layout(self):
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        container.set_margin_top(16)
        container.set_margin_start(16)
        container.set_margin_end(16)
        container.set_margin_bottom(16)
        self.window.set_child(container)

        self.header = HeaderBar(
            on_open_dir=self._on_open_dir,
            on_prefs=self.show_preferences,
            on_search_changed=lambda q: self.gallery.set_filter(q)
        )
        container.append(self.header)

        self.gallery = Gallery(
            on_thumbnail_selected=self._on_gallery_selected,
            on_thumbnail_double_clicked=self._on_gallery_double_clicked
        )
        container.append(self.gallery)

        self.footer = FooterBar(
            on_apply=lambda: self._on_apply_wallpaper(self._selected_path or "", self.resize_var)
        )
        container.append(self.footer)
        self._selected_path = None
        self._update_component_states()
    
    def _on_open_dir(self, *args):
        dialog = Gtk.FileChooserNative.new(
            "Select Directory",
            self.window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            "_Open",
            "_Cancel",
        )
        self._open_dir_dialog = dialog

        def on_response(dlg, response):
            if response == Gtk.ResponseType.ACCEPT:
                file = dlg.get_file()
                if file:
                    directory = file.get_path()
                    self.current_dir = Path(directory)
                    self.gallery.load_directory(directory)
            dlg.destroy()
            self._open_dir_dialog = None

        dialog.connect("response", on_response)
        dialog.show()
    
    def _apply_theme(self):
        theme_name = self.config.get("theme", "catppuccin")
        css = get_theme_css(theme_name)
        
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode())
        
        Gtk.StyleContext.add_provider_for_display(
            self.window.get_display(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
    
    def _update_component_states(self):
        pass

    def _on_gallery_selected(self, path: str):
        self._selected_path = path
    
    def _on_gallery_double_clicked(self, path: str):
        self._selected_path = path
        self._on_apply_wallpaper(path, self.resize_var)
    
    def _on_apply_wallpaper(self, path: str, resize: str):
        if not path or not Path(path).exists():
            print(f"[wallgui] File not found: {path}")
            return

        try:
            set_wallpaper(path, resize)
            self._update_component_states()

        except Exception as e:
            print(f"[wallgui] Error applying wallpaper: {e}")
    
    def _on_preferences_save(self, new_config: dict):
        self.config = new_config
        StorageManager.save_config(new_config)
        self._apply_theme()
        self.resize_var = new_config.get("default_resize", "crop")
    
    def show_preferences(self):
        dialog = PreferencesDialog(
            parent=self.window,
            config=self.config,
            on_save=self._on_preferences_save
        )
        dialog.show()


def main():
    app = WallpaperApp()
    return app.run(None)


if __name__ == "__main__":
    main()
