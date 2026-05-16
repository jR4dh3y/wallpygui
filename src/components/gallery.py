#!/usr/bin/env python3
"""Gallery component for displaying wallpaper thumbnails."""

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Pango
from pathlib import Path
import threading
from typing import Callable, Optional

from utils.constants import SUPPORTED_EXTS
from utils.wallpaper_utils import generate_cached_thumbnail


class Gallery(Gtk.Box):
    """Gallery component displays thumbnails."""
    
    def __init__(self, on_thumbnail_selected: Optional[Callable[[str], None]] = None,
                 on_thumbnail_double_clicked: Optional[Callable[[str], None]] = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_vexpand(True)

        self.on_thumbnail_selected = on_thumbnail_selected
        self.on_thumbnail_double_clicked = on_thumbnail_double_clicked

        self.loading = False
        self.thumbnail_threads = []
        self.search_text = ""
        self.selected_child: Optional[Gtk.FlowBoxChild] = None
        self._thumb_queue = []  # list of (Path, Gtk.Image)
        self._thumb_workers = 0
        self._max_thumb_workers = 2  # adjustable
        self._load_generation = 0
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_vexpand(True)
        scroll.set_css_classes(["gallery-scroll"])
        
        self.flow = Gtk.FlowBox()
        self.flow.set_valign(Gtk.Align.START)
        self.flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flow.set_min_children_per_line(3)
        self.flow.set_max_children_per_line(8)
        self.flow.set_row_spacing(10)
        self.flow.set_column_spacing(10)
        self.flow.set_margin_top(10)
        self.flow.set_margin_bottom(10)
        self.flow.set_margin_start(10)
        self.flow.set_margin_end(10)
        self.flow.set_homogeneous(True)
        
        scroll.set_child(self.flow)
        self.append(scroll)
        
        self.spinner = Gtk.Spinner()
        self.spinner.set_visible(False)
        self.append(self.spinner)
    
    def load_directory(self, directory: str):
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            print(f"Directory not found: {directory}")
            return

        self._load_generation += 1
        generation = self._load_generation
        self._thumb_queue.clear()
        self._clear_flowbox()
        self.spinner.set_visible(True)
        self.spinner.start()
        self.loading = True
        
        def scan_worker():
            try:
                files = [p for p in path.iterdir() if p.suffix.lower() in SUPPORTED_EXTS]
                # Show a quick initial unsorted batch to reduce perceived delay
                head, tail = files[:30], files[30:]
                for fp in head:
                    if not self.loading or generation != self._load_generation:
                        break
                    GLib.idle_add(self._add_thumbnail, fp, generation)
                tail.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                for fp in tail:
                    if not self.loading or generation != self._load_generation:
                        break
                    GLib.idle_add(self._add_thumbnail, fp, generation)
            except Exception as e:
                GLib.idle_add(print, f"Gallery Error: {e}")
            finally:
                if generation == self._load_generation:
                    GLib.idle_add(self.spinner.stop)
                    GLib.idle_add(self.spinner.set_visible, False)
                    GLib.idle_add(self._loading_done)

        threading.Thread(target=scan_worker, daemon=True).start()
        
    def set_filter(self, query: str):
        self.search_text = (query or "").lower().strip()
        self._apply_filter()

    def _add_thumbnail(self, filepath: Path, generation: int):
        """Create a thumbnail entry quickly, then load image asynchronously."""
        if generation != self._load_generation:
            return False

        img = Gtk.Image()
        img.set_pixel_size(160)
        img.set_size_request(170, 106)
        # Placeholder icon until loaded
        if filepath.suffix.lower() in {".mp4", ".mkv", ".mov"}:
            img.set_from_icon_name("media-playback-start")
        else:
            img.set_from_icon_name("image-x-generic")

        label = Gtk.Label(label=filepath.name)
        label.set_css_classes(["thumb-label"])
        label.set_halign(Gtk.Align.CENTER)
        label.set_wrap(False)
        label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        label.set_max_width_chars(20)
        label.set_lines(1)

        child_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        child_box.set_css_classes(["thumbnail-box"])
        child_box.set_size_request(178, 136)
        child_box.set_halign(Gtk.Align.CENTER)
        child_box.append(img)
        child_box.append(label)

        child = Gtk.FlowBoxChild()
        child.set_child(child_box)
        child.filepath = str(filepath)
        child.inner_box = child_box
        child.add_controller(self._make_click_controller(child))
        self.flow.append(child)

        self._thumb_queue.append((filepath, img, generation))
        self._maybe_start_thumb_worker()
        return False

    def _maybe_start_thumb_worker(self):
        if self._thumb_workers >= self._max_thumb_workers or not self._thumb_queue:
            return
        filepath, img, generation = self._thumb_queue.pop(0)
        if generation != self._load_generation:
            self._maybe_start_thumb_worker()
            return
        self._thumb_workers += 1

        def worker(fp=filepath, image=img):
            try:
                thumb_path = generate_cached_thumbnail(fp, width=170, height=106)
                if thumb_path and generation == self._load_generation:
                    GLib.idle_add(self._set_image_from_file, image, thumb_path, generation)
            except Exception:
                if generation == self._load_generation:
                    GLib.idle_add(lambda im=image: im.set_from_icon_name("image-missing"))
            finally:
                def done():
                    self._thumb_workers -= 1
                    self._maybe_start_thumb_worker()
                    return False
                GLib.idle_add(done)

        threading.Thread(target=worker, daemon=True).start()
        self._maybe_start_thumb_worker()

    def _set_image_from_file(self, image: Gtk.Image, path: str, generation: int):
        if generation == self._load_generation:
            image.set_from_file(path)
        return False
    
    def _make_click_controller(self, child):
        gesture = Gtk.GestureClick()
        def on_press(gesture, n_press, x, y):
            if n_press == 1:
                self._select_child(child)
                if self.on_thumbnail_selected:
                    self.on_thumbnail_selected(child.filepath)
            elif n_press == 2:
                self._select_child(child)
                if self.on_thumbnail_double_clicked:
                    self.on_thumbnail_double_clicked(child.filepath)
        gesture.connect("pressed", on_press)
        return gesture

    def _select_child(self, child: Gtk.FlowBoxChild):
        try:
            if self.selected_child and hasattr(self.selected_child, 'inner_box'):
                old_box = self.selected_child.inner_box
                classes = list(old_box.get_css_classes())
                if "selected-thumb" in classes:
                    classes.remove("selected-thumb")
                    old_box.set_css_classes(classes)
        except Exception:
            pass

        # Apply selection style to new child
        try:
            inner = getattr(child, 'inner_box', None)
            if inner is not None:
                classes = list(inner.get_css_classes())
                if "selected-thumb" not in classes:
                    classes.append("selected-thumb")
                    inner.set_css_classes(classes)
            self.selected_child = child
        except Exception:
            self.selected_child = child

    def select_random(self, rng) -> Optional[str]:
        visible_children = []
        child = self.flow.get_first_child()
        while child is not None:
            if child.get_visible() and hasattr(child, "filepath"):
                visible_children.append(child)
            child = child.get_next_sibling()

        if not visible_children:
            return None

        selected = rng.choice(visible_children)
        self._select_child(selected)
        return selected.filepath
    
    def _clear_flowbox(self):
        try:
            child = self.flow.get_first_child()
            while child is not None:
                next_child = child.get_next_sibling()
                self.flow.remove(child)
                child = next_child
        except AttributeError:
            pass
    
    def _apply_filter(self):
        query = self.search_text
        child = self.flow.get_first_child()
        while child is not None:
            try:
                box = child.get_child()
                label_child = box.get_first_child()
                if label_child and hasattr(label_child, 'get_next_sibling'):
                    label_child = label_child.get_next_sibling()
                if label_child and hasattr(label_child, 'get_text'):
                    name = label_child.get_text().lower()
                    child.set_visible(query in name if query else True)
            except (AttributeError, TypeError):
                child.set_visible(True)
            child = child.get_next_sibling()
    
    def _loading_done(self):
        self.loading = False
