#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from typing import Callable


class FooterBar(Gtk.Box):
    """Bottom action bar with primary actions (simplified)."""

    def __init__(self, on_apply: Callable[[], None]):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.set_css_classes(["controls-box"])
        self.set_halign(Gtk.Align.FILL)
        self.set_hexpand(True)
        apply_btn = Gtk.Button(label="Apply Wallpaper")
        apply_btn.set_css_classes(["apply-btn"])
        apply_btn.set_halign(Gtk.Align.CENTER)
        apply_btn.set_hexpand(True)
        apply_btn.connect("clicked", lambda *_: on_apply())
        self.append(apply_btn)
        self.apply_btn = apply_btn

    