# WallpyGUI

Modern GTK4 wallpaper manager for Wayland desktops, built for fast browsing, search, image wallpapers, and video wallpapers on Niri and Hyprland.

![WallpyGUI screenshot](assets/app.png)

## Features

- Gallery view with async thumbnail loading
- Search wallpapers by filename
- Set image wallpapers via `awww`
- Set video wallpapers via `mpvpaper`
- Works well on Niri and Hyprland
- Themeable UI (Catppuccin and others)

## Dependencies

Required: `gtk4`, `python`, `python-gobject`, `awww`, `mpvpaper`, `ffmpeg`

Optional: `hyprland` or `niri` for monitor detection, `wallust` for colorscheme workflows.

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

See `PKGBUILD` for Arch packaging.

## License

MIT - see `LICENSE`.
