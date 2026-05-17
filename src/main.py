#!/usr/bin/env python3
"""GTK wallpaper manager application."""

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
from pathlib import Path
import random
import threading

from utils.constants import APP_ID, APP_TITLE
from utils.storage import StorageManager
from utils.wallpaper_utils import set_wallpaper, restore
from styles.themes import get_theme_css
from components.gallery import Gallery
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
            self.window.set_default_size(1040, 680)
            self.window.set_resizable(True)
            self.window.set_css_classes(["main-window"])
            
            self._apply_theme()
            self._setup_main_layout()
            self.gallery.load_directory(str(self.current_dir))
        
        self.window.present()
    
    def _setup_main_layout(self):
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        container.set_margin_top(0)
        container.set_margin_start(0)
        container.set_margin_end(0)
        container.set_margin_bottom(0)
        self.window.set_child(container)

        self.header = HeaderBar(
            on_open_dir=self._on_open_dir,
            on_random=self._on_random_wallpaper,
            on_search_changed=lambda q: self.gallery.set_filter(q)
        )
        container.append(self.header)

        self.gallery = Gallery(
            on_thumbnail_selected=self._on_gallery_selected,
            on_thumbnail_double_clicked=self._on_gallery_double_clicked
        )
        container.append(self.gallery)

        self.footer = FooterBar(
            on_apply=lambda: self._on_apply_wallpaper(self._selected_path or "", self.resize_var),
            on_resize_changed=self._on_resize_changed,
            resize_mode=self.resize_var,
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
        if hasattr(self, "footer"):
            self.footer.set_selected_path(path)
    
    def _on_gallery_double_clicked(self, path: str):
        self._selected_path = path
        if hasattr(self, "footer"):
            self.footer.set_selected_path(path)
        self._on_apply_wallpaper(path, self.resize_var)

    def _on_resize_changed(self, mode: str):
        self.resize_var = mode

    def _on_random_wallpaper(self):
        path = self.gallery.select_random(random)
        if path:
            self._selected_path = path
            if hasattr(self, "footer"):
                self.footer.set_selected_path(path)
            self._on_apply_wallpaper(path, self.resize_var)
    
    def _on_apply_wallpaper(self, path: str, resize: str):
        if not path or not Path(path).exists():
            print(f"[wallpygui] File not found: {path}")
            return

        # Disable the button and show progress while applying to avoid UI freeze
        if hasattr(self, "footer") and getattr(self.footer, "apply_btn", None):
            self.footer.set_busy(True)

        def worker():
            success = True
            try:
                set_wallpaper(path, resize)
            except Exception as e:
                success = False
                print(f"[wallpygui] Error applying wallpaper: {e}")
            finally:
                # Re-enable controls on the GTK main loop
                GLib.idle_add(self._on_apply_wallpaper_done, success)

        threading.Thread(target=worker, daemon=True).start()

    def _on_apply_wallpaper_done(self, success: bool):
        if hasattr(self, "footer") and getattr(self.footer, "apply_btn", None):
            self.footer.set_busy(False)
        if success:
            self._update_component_states()
        return False
    
def main():
    app = WallpaperApp()
    return app.run(None)


if __name__ == "__main__":
    main()
