#!/usr/bin/env python3
"""Minimal Preferences dialog (theme + resize only)."""

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from typing import Callable, Dict, Any

from styles.themes import THEMES


class PreferencesDialog(Gtk.Dialog):
    """Preferences dialog exposing theme and resize settings."""

    def __init__(self, parent, config: Dict[str, Any], on_save: Callable[[Dict[str, Any]], None]):
        super().__init__(title="Preferences", transient_for=parent, modal=True)
        self.config = config.copy()
        self.on_save = on_save
        self.set_default_size(200, 200)
        self.set_resizable(False)
        self._build_ui()

    def _build_ui(self):
        box = self.get_content_area()
        box.set_spacing(14)
        for side in (box.set_margin_top, box.set_margin_bottom, box.set_margin_start, box.set_margin_end):
            side(16)

        grid = Gtk.Grid(column_spacing=16, row_spacing=12)
        box.append(grid)

        # Theme
        grid.attach(Gtk.Label(label="Theme:", css_classes=["prefs-label"]), 0, 0, 1, 1)
        self.theme_combo = Gtk.ComboBoxText()
        for theme_id, theme_data in THEMES.items():
            self.theme_combo.append(theme_id, theme_data["name"])
        self.theme_combo.set_active_id(self.config.get("theme", "catppuccin"))
        grid.attach(self.theme_combo, 1, 0, 1, 1)

        # Resize
        grid.attach(Gtk.Label(label="Default Resize:", css_classes=["prefs-label"]), 0, 1, 1, 1)
        self.resize_combo = Gtk.ComboBoxText()
        for mode in ("crop", "fit", "stretch"):
            self.resize_combo.append(mode, mode.capitalize())
        self.resize_combo.set_active_id(self.config.get("default_resize", "crop"))
        grid.attach(self.resize_combo, 1, 1, 1, 1)

        # Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        btn_box.set_halign(Gtk.Align.CENTER)
        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect("clicked", lambda *_: self.close())
        save_btn = Gtk.Button(label="Save")
        save_btn.set_css_classes(["apply-btn"])
        save_btn.connect("clicked", self._on_save)
        btn_box.append(cancel_btn)
        btn_box.append(save_btn)
        box.append(btn_box)

    def _on_save(self, *_):
        self.config["theme"] = self.theme_combo.get_active_id()
        self.config["default_resize"] = self.resize_combo.get_active_id()
        self.on_save(self.config)
        self.close()
