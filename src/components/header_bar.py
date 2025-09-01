#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from typing import Callable, Optional
from utils.constants import APP_TITLE

from utils.constants import APP_TITLE


class HeaderBar(Gtk.Box):
    """Top header bar with title, search, and global actions."""

    def __init__(self,
                 on_open_dir: Callable[[], None],
                 on_random: Optional[Callable[[], None]] = None,
                 on_prefs: Optional[Callable[[], None]] = None,
                 on_search_changed: Optional[Callable[[str], None]] = None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.set_css_classes(["header-box"])
        
        # Title
        title = Gtk.Label(label=APP_TITLE)
        title.set_css_classes(["title-label"])
        title.set_halign(Gtk.Align.START)
        self.append(title)

        # Spacer
        self.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))

        # Search
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search wallpapers...")
        self.search_entry.set_css_classes(["search-entry"])
        if on_search_changed is not None:
            self.search_entry.connect("changed", lambda e: on_search_changed(e.get_text()))
        self.search_entry.set_hexpand(True)
        self.append(self.search_entry)

        # Buttons
        open_btn = Gtk.Button(label="Open Dir")
        open_btn.connect("clicked", lambda *_: on_open_dir())
        self.append(open_btn)

        if on_random is not None:
            random_btn = Gtk.Button(label="Random")
            random_btn.connect("clicked", lambda *_: on_random())
            self.append(random_btn)

        if on_prefs is not None:
            prefs_btn = Gtk.Button(label="Preferences")
            prefs_btn.connect("clicked", lambda *_: on_prefs())
            self.append(prefs_btn)
