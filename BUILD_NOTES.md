# WallpyGUI v0.0.2 Build Notes

## Release Date

2026-06-02

## Summary

This patch release fixes wallpaper switching between image and video backgrounds.
Video wallpapers now respect the selected resize mode, and image wallpapers restart
the `awww` daemon reliably after a video wallpaper has stopped it.

## Changes

- Apply `Crop`, `Fit`, and `Stretch` resize modes to video wallpapers.
- Generate cached, monitor-sized video files for resize-aware `mpvpaper` playback.
- Stop the existing `awww` image layer before applying a video wallpaper.
- Restart `awww-daemon` directly before applying image wallpapers when needed.
- Wait for `awww` to accept commands and retry image wallpaper application.
- Fail image application explicitly when `awww` cannot apply the wallpaper.

## Dependencies

Required runtime dependencies remain unchanged:

- `gtk4`
- `python`
- `python-gobject`
- `awww`
- `mpvpaper`
- `ffmpeg`

## Verification

```bash
python -m compileall -q src
```

## Packaging

The release source archive is available from:

```text
https://github.com/jR4dh3y/wallpygui/archive/refs/tags/v0.0.2.tar.gz
```
