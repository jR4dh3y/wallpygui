# wallgui

Modern GTK4 wallpaper manager with fast directory browsing, search, and support for image and video wallpapers.

## Features
- Gallery view with async thumbnail loading
- Set image wallpapers via swww (Wayland)
- Set video wallpapers via mpvpaper (Hyprland/Niri)
- Themeable UI (Catppuccin and others)

![wallgui-screenshot](/assets/app.png)

## Dependencies
Required: gtk4, python, python-gobject, swww, mpvpaper, ffmpeg
Optional: hyprland or niri (for monitor detection), wallust (for colorscheme, not invoked by default)

## Run from source
```bash
git clone https://github.com/jR4dh3y/wallpygui.git
cd wallpygui
python3 wallgui.py
```

## Config
Files are stored in `~/.cache/wallgui/`:
- `config.json`

## Packaging
See `PKGBUILD` for Arch packaging. A prebuilt spec is available via `wallgui.spec`.

## License
MIT – see `LICENSE`.

