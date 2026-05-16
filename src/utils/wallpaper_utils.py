#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from typing import Optional
import hashlib
import shutil

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


def stop_video_wallpaper() -> None:
    """Stop any existing mpvpaper process before switching wallpaper modes."""
    if shutil.which("pkill"):
        no_stdout(["pkill", "mpvpaper"])


def reload_hyprland_if_running() -> None:
    """Reload Hyprland only when this process is running inside Hyprland."""
    if os.getenv("HYPRLAND_INSTANCE_SIGNATURE") and shutil.which("hyprctl"):
        no_stdout(["hyprctl", "reload"])


def use_awww(img_path: str, resize: str = "crop") -> None:
    """Set wallpaper using awww."""
    stop_video_wallpaper()
    # Ensure awww daemon is running; if not, initialize it
    try:
        probe = subprocess.run(["awww", "query"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if probe.returncode != 0:
            no_stdout(["awww", "init"])
    except Exception:
        # Best-effort: continue to try setting the image
        pass
    no_stdout([
        "awww",
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

    stop_video_wallpaper()

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
        source = Path(img_path).resolve()
        source_stat = source.stat()
        scale_key = hashlib.sha256(
            f"{source}:{source_stat.st_mtime_ns}:{source_stat.st_size}:{width}x{height}".encode()
        ).hexdigest()
        scaled = CACHE_DIR / "scaled-videos" / f"{scale_key}.mp4"
        scaled.parent.mkdir(parents=True, exist_ok=True)
        if not scaled.exists():
            result = no_stdout([
                "ffmpeg",
                "-y",
                "-i",
                img_path,
                "-vf",
                f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
                str(scaled),
            ])
            if result.returncode != 0:
                scaled.unlink(missing_ok=True)

        if scaled.exists():
            video = str(scaled)

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
        use_awww(img_path, resize)
    elif file_type.startswith("video/"):
        use_mpv(img_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    reload_hyprland_if_running()
    # External colorscheme command removed

    # Save current wallpaper path
    with open(os.path.expanduser("~/.cache/wallpaper"), "w") as file:
        file.write(img_path)
    apply_to_hyperpaper_cfg()


def generate_cached_thumbnail(filepath: Path, size: int = 200) -> Optional[str]:
    """Generate and cache thumbnail for a file."""
    try:
        filepath = filepath.expanduser()
        stat = filepath.stat()
        cache_key = hashlib.sha256(
            f"{filepath.resolve()}:{stat.st_mtime_ns}:{stat.st_size}:{size}".encode()
        ).hexdigest()
        thumb_dir = CACHE_DIR / "thumbnails"
        thumb_dir.mkdir(parents=True, exist_ok=True)
        thumb_path = thumb_dir / f"{cache_key}.png"

        if thumb_path.exists():
            return str(thumb_path)

        filters = f"scale={size}:{size}:force_original_aspect_ratio=decrease"
        if filepath.suffix.lower() in {".mp4", ".mkv", ".mov"}:
            filters = f"thumbnail,{filters}"

        result = no_stdout([
            "ffmpeg", "-y", "-i", str(filepath),
            "-vf", filters,
            "-frames:v", "1", str(thumb_path)
        ])
        return str(thumb_path) if result.returncode == 0 and thumb_path.exists() else None
    except Exception as e:
        print(f"Failed to generate thumbnail for {filepath}: {e}")
        return None

def apply_to_hyperpaper_cfg() -> None:
    """Apply wallpaper settings to hyprlock config if it exists."""
    config_path = Path.home() / ".config" / "hypr" / "hyprlock.conf"
    wallpaper_path = restore()
    if not wallpaper_path:
        return
    if not config_path.exists():
        print("Hyprlock config not found; skipping update.")
        return
    try:
        lines = config_path.read_text().splitlines()
        updated = False
        new_lines = []

        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith("path"):
                indent = line[: len(line) - len(stripped)]
                new_lines.append(f'{indent}path = {wallpaper_path}')
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_lines.append(f'path = "{wallpaper_path}"')

        config_path.write_text("\n".join(new_lines) + "\n")
    except Exception as e:
        print(f"Failed to update hyprlock config: {e}")
