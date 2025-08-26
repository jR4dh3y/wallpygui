#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from typing import Optional

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


def generate_colors(img_path: str) -> None:
    return


def generate_thumbnail(video: str) -> str:
    """Generate thumbnail for video file."""
    thumb_path = f"/tmp/{os.getlogin()}-thumbnail.png"
    if Path(thumb_path).exists():
        os.remove(thumb_path)
    no_stdout(["ffmpeg", "-i", video, "-vf", "thumbnail", "-frames:v", "1", thumb_path])
    return thumb_path


def use_swww(img_path: str, resize: str = "crop") -> None:
    """Set wallpaper using swww."""
    subprocess.run(["pkill", "mpvpaper"])
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
    """Set video wallpaper using mpvpaper."""
    import json

    outputs = json.loads(subprocess.check_output(["hyprctl", "monitors", "-j"]))
    width = min(output["width"] for output in outputs)
    height = min(output["height"] for output in outputs)

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
    if v_width > width:
        scaled = f"/tmp/{os.getlogin()}-scaled.mp4"
        no_stdout([
            "ffmpeg",
            "-i",
            img_path,
            "-vf",
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            scaled,
        ])
        video = scaled
    else:
        video = img_path

    for output in outputs:
        no_stdout(["mpvpaper", "-s", "-o", "no-audio loop", output["name"], video])


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
