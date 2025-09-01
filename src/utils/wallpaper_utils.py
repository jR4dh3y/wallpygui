#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from typing import Optional
import getpass

from utils.constants import CACHE_DIR


def restore() -> str:
    """Restore the last used wallpaper path."""
    file_path = os.path.expanduser("~/.cache/wallpaper")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            wallpaper = file.read().strip()
            return wallpaper
    return ""


def no_stdout(cmd: list) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def spawn(cmd: list) -> subprocess.Popen:
    """Launch a long-running process detached from the parent without waiting.

    Stdout/stderr are suppressed, and the process starts a new session so it
    won't terminate with the parent.
    """
    return subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


_USER_TAG = getpass.getuser() or "user"


def generate_thumbnail(video: str) -> str:
    """Generate thumbnail for video file."""
    thumb_path = f"/tmp/wallgui-{_USER_TAG}-thumbnail.png"
    if Path(thumb_path).exists():
        os.remove(thumb_path)
    no_stdout(["ffmpeg", "-i", video, "-vf", "thumbnail", "-frames:v", "1", thumb_path])
    return thumb_path


def use_swww(img_path: str, resize: str = "crop") -> None:
    """Set wallpaper using swww."""
    subprocess.run(["pkill", "mpvpaper"])
    # Ensure swww daemon is running; if not, initialize it
    try:
        probe = subprocess.run(["swww", "query"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if probe.returncode != 0:
            no_stdout(["swww", "init"])
    except Exception:
        # Best-effort: continue to try setting the image
        pass
    no_stdout([
        "swww",
        "img",
        "--filter",
        "Lanczos3",
        "--resize",
        resize,
        "--transition-duration",
        "1",
        "--transition-type",
        "center",
        img_path,
    ])


def use_mpv(img_path: str) -> None:
    """Set video wallpaper using mpvpaper, supporting Hyprland and Niri."""
    import json

    def get_outputs() -> list[dict]:
        # Try Hyprland
        try:
            hypr_json = subprocess.check_output(["hyprctl", "monitors", "-j"], text=True)
            hypr_outputs = json.loads(hypr_json)
            results = []
            for o in hypr_outputs:
                name = o.get("name") or o.get("id") or o.get("description")
                w = o.get("width") or (o.get("size", {}).get("width"))
                h = o.get("height") or (o.get("size", {}).get("height"))
                if name and w and h:
                    results.append({"name": name, "width": int(w), "height": int(h)})
            if results:
                return results
        except Exception:
            pass

        # Try Niri
        try:
            niri_json = subprocess.check_output(["niri", "msg", "-j", "outputs"], text=True)
            data = json.loads(niri_json)
            arr = data.get("outputs", data if isinstance(data, list) else [])
            results = []
            for o in arr:
                name = o.get("name") or o.get("connector") or o.get("id")
                w = (
                    o.get("width")
                    or (o.get("rect", {}).get("w"))
                    or (o.get("current-mode", {}).get("width"))
                    or (o.get("mode", {}).get("width"))
                    or (o.get("mode", {}).get("size", {}).get("width"))
                )
                h = (
                    o.get("height")
                    or (o.get("rect", {}).get("h"))
                    or (o.get("current-mode", {}).get("height"))
                    or (o.get("mode", {}).get("height"))
                    or (o.get("mode", {}).get("size", {}).get("height"))
                )
                if name and w and h:
                    results.append({"name": name, "width": int(w), "height": int(h)})
            if results:
                return results
        except Exception:
            pass

        return []

    outputs = get_outputs()
    width = min(o["width"] for o in outputs) if outputs else None
    height = min(o["height"] for o in outputs) if outputs else None

    result = subprocess.check_output([
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=s=x:p=0",
        img_path,
    ], text=True).strip()

    v_width, v_height = map(int, result.split("x"))

    video = img_path
    if width and v_width > width:
        scaled = f"/tmp/wallgui-{_USER_TAG}-scaled.mp4"
        no_stdout([
            "ffmpeg",
            "-y",
            "-i",
            img_path,
            "-vf",
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            scaled,
        ])
        video = scaled

    if outputs:
        for o in outputs:
            # Use non-blocking spawn; mpvpaper is long-running
            spawn(["mpvpaper", "-s", "-o", "no-audio loop", o["name"], video])
    else:
        # Fallback: try all outputs if compositor detection failed
        spawn(["mpvpaper", "-s", "-o", "no-audio loop", "*", video])


def set_wallpaper(img_path: str, resize: str = "crop") -> None:
    """Apply wallpaper depending on type (image/video)."""
    file_type = subprocess.check_output([
        "file", "-b", "--mime-type", img_path
    ], text=True).strip()

    if not os.getenv("WAL_BACKEND"):
        os.environ["WAL_BACKEND"] = "haishoku"

    if file_type.startswith("image/"):
        use_swww(img_path, resize)
    elif file_type.startswith("video/"):
        generate_thumbnail(img_path)  # still produce a thumb (cache) but ignore colors
        use_mpv(img_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    no_stdout(["hyprctl", "reload"])
    # External colorscheme command removed

    # Save current wallpaper path
    with open(os.path.expanduser("~/.cache/wallpaper"), "w") as file:
        file.write(img_path)


def generate_cached_thumbnail(filepath: Path, size: int = 200) -> Optional[str]:
    """Generate and cache thumbnail for a file."""
    try:
        if filepath.suffix.lower() in {".mp4", ".mkv", ".mov"}:
            # Video thumbnail
            thumb_path = CACHE_DIR / f"{filepath.stem}_thumb.png"
            if (not thumb_path.exists()) or (thumb_path.stat().st_mtime < filepath.stat().st_mtime):
                no_stdout([
                    "ffmpeg", "-y", "-i", str(filepath), 
                    "-vf", "thumbnail,scale=320:-1", 
                    "-frames:v", "1", str(thumb_path)
                ])
            return str(thumb_path)
        else:
            # Image thumbnail - return path for GTK to handle scaling
            return str(filepath)
    except Exception as e:
        print(f"Failed to generate thumbnail for {filepath}: {e}")
        return None
