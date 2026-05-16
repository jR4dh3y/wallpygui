#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Pango
from pathlib import Path
from typing import Callable


class FooterBar(Gtk.Box):
    """Bottom action bar with selected item and apply controls."""

    def __init__(self, on_apply: Callable[[], None],
                 on_resize_changed: Callable[[str], None],
                 resize_mode: str = "crop"):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_css_classes(["controls-box"])
        self.set_halign(Gtk.Align.FILL)
        self.set_hexpand(True)

        self.selected_label = Gtk.Label(label="No wallpaper selected")
        self.selected_label.set_css_classes(["selected-label"])
        self.selected_label.set_halign(Gtk.Align.START)
        self.selected_label.set_hexpand(True)
        self.selected_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        self.append(self.selected_label)

        mode_label = Gtk.Label(label="Fit")
        mode_label.set_css_classes(["meta-label"])
        self.append(mode_label)

        self.resize_combo = Gtk.ComboBoxText()
        for mode, label in (("crop", "Crop"), ("fit", "Fit"), ("stretch", "Stretch")):
            self.resize_combo.append(mode, label)
        self.resize_combo.set_active_id(resize_mode)
        self.resize_combo.connect("changed", lambda c: on_resize_changed(c.get_active_id() or "crop"))
        self.append(self.resize_combo)

        apply_btn = Gtk.Button(label="Apply Wallpaper")
        apply_btn.set_css_classes(["apply-btn"])
        apply_btn.set_sensitive(False)
        apply_btn.connect("clicked", lambda *_: on_apply())
        self.append(apply_btn)
        self.apply_btn = apply_btn

    def set_selected_path(self, path: str | None):
        if path:
            self.selected_label.set_text(Path(path).name)
            self.apply_btn.set_sensitive(True)
        else:
            self.selected_label.set_text("No wallpaper selected")
            self.apply_btn.set_sensitive(False)

    def set_busy(self, busy: bool):
        self.apply_btn.set_sensitive(not busy and self.selected_label.get_text() != "No wallpaper selected")
        self.apply_btn.set_label("Applying..." if busy else "Apply Wallpaper")
