# wallgui

Modern GTK4 wallpaper manager with image, video, favorites, history, themes, and auto‑cycle support.

## Features (core)
- Gallery + preview
- Favorites & history
- Image & video wallpapers (swww / mpvpaper)
- Auto cycle & random pick
- Themeable UI + color scheme generation (wallust)

## Dependencies
Required: gtk4 python python-gobject swww mpvpaper wallust ffmpeg
Optional: hyprland (for hyprctl integration)

## Run from source
```bash
git clone https://github.com/jr4dh3y/wallgui.git
cd wallgui
python3 wallgui.py
```

## AUR (Arch)
Incoming packages:
- wallgui (build from source)
- wallgui-bin (prebuilt binary)

## Config files
Stored in: ~/.cache/wallgui/
- config.json / history.json / favorites.json

## License
MIT – see LICENSE.

