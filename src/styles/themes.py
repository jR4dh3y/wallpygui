#!/usr/bin/env python3
"""Theme definitions for the wallpaper manager application."""

THEMES = {
    "catppuccin": {
        "name": "Catppuccin",
        "colors": {
            "bg": "#1e1e2e",
            "bg_alt": "#181825",
            "bg_soft": "#313244",
            "fg": "#cdd6f4",
            "fg_dim": "#a6adc8",
            "accent": "#cba6f7",
            "accent_alt": "#f9e2af",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "error": "#f38ba8",
            "border": "#45475a",
            "border_alt": "#585b70"
        }
    },
    "dracula": {
        "name": "Dracula",
        "colors": {
            "bg": "#282a36",
            "bg_alt": "#1e1f29",
            "bg_soft": "#44475a",
            "fg": "#f8f8f2",
            "fg_dim": "#6272a4",
            "accent": "#bd93f9",
            "accent_alt": "#ffb86c",
            "success": "#50fa7b",
            "warning": "#ffb86c",
            "error": "#ff5555",
            "border": "#6272a4",
            "border_alt": "#44475a"
        }
    },
    "nord": {
        "name": "Nord",
        "colors": {
            "bg": "#2e3440",
            "bg_alt": "#242933",
            "bg_soft": "#3b4252",
            "fg": "#eceff4",
            "fg_dim": "#d8dee9",
            "accent": "#88c0d0",
            "accent_alt": "#ebcb8b",
            "success": "#a3be8c",
            "warning": "#ebcb8b",
            "error": "#bf616a",
            "border": "#4c566a",
            "border_alt": "#5e81ac"
        }
    },
    "gruvbox": {
        "name": "Gruvbox",
        "colors": {
            "bg": "#282828",
            "bg_alt": "#1d2021",
            "bg_soft": "#3c3836",
            "fg": "#ebdbb2",
            "fg_dim": "#928374",
            "accent": "#b8bb26",
            "accent_alt": "#fabd2f",
            "success": "#98971a",
            "warning": "#fabd2f",
            "error": "#cc241d",
            "border": "#504945",
            "border_alt": "#665c54"
        }
    },
    "tokyonight": {
        "name": "Tokyo Night",
        "colors": {
            "bg": "#1a1b26",
            "bg_alt": "#16161e",
            "bg_soft": "#24283b",
            "fg": "#c0caf5",
            "fg_dim": "#7982a9",
            "accent": "#bb9af7",
            "accent_alt": "#f7768e",
            "success": "#9ece6a",
            "warning": "#e0af68",
            "error": "#f7768e",
            "border": "#414868",
            "border_alt": "#565a6e"
        }
    }
}


def get_theme_css(theme_name: str = "catppuccin") -> str:
    """Generate CSS for the specified theme using a safe template formatter."""
    theme = THEMES.get(theme_name, THEMES["catppuccin"])
    c = theme["colors"]
    return """
    .main-window {{
        background: {bg};
        border-radius: 0px;
        color: {fg};
        border: 1px solid {border};
        padding: 16px;
    }}

    .title-label {{
        font-size: 28px;
        font-weight: bold;
        color: {accent};
    }}

    .preview-frame {{
        border-radius: 0px;
        border: 2px solid {accent};
        background: {bg_alt};
        margin-bottom: 12px;
        padding: 12px;
    }}

    .path-entry, .dir-entry, .search-entry {{
        border-radius:0px;
        padding: 8px 12px;
        background: {bg_soft};
        color: {fg};
        border: 1px solid {border};
        font-size: 13px;
    }}

    .path-entry:focus, .dir-entry:focus, .search-entry:focus {{
        border-color: {accent};
        background: {bg_soft};
    }}

    button {{
        background: {bg_soft};
        color: {fg};
        border-radius: 0px;
        font-weight: 600;
        padding: 8px 16px;
        border: 1px solid {border};
        transition: all 0.2s ease;
        font-size: 13px;
    }}

    button:hover {{
        background: {border_alt};
        transform: translateY(-1px);
    }}

    .apply-btn {{
        background: {success};
        color: {bg};
        font-weight: bold;
        padding: 10px 20px;
    }}

    .apply-btn:hover {{
        background: {success};
        opacity: 0.9;
    }}

    .scheme-btn {{
        background: {accent_alt};
        color: {bg};
        font-weight: bold;
        padding: 10px 20px;
    }}

    .scheme-btn:hover {{
        background: {accent_alt};
        opacity: 0.9;
    }}

    .gallery-frame {{
        border-radius: 0px;
        border: 2px dashed {border};
        background: {bg_alt};
        padding: 12px;
    }}

    .thumbnail-box {{
        background: {bg_soft};
        padding: 8px;
        border-radius: 0px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }}

    .thumbnail-box:hover {{
        background: {border_alt};
        transform: translateY(-2px);
        border-color: {accent};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}

    /* Selected thumbnail thin border */
    .selected-thumb {{
        border: 2px solid {accent};
        box-shadow: 0 0 0 2px rgba(0,0,0,0.2) inset;
    }}

    .thumb-label {{
        color: {fg};
        font-size: 11px;
        font-weight: 500;
        margin-top: 4px;
    }}

    .favorite-row {{
        color: {accent_alt};
        font-weight: 600;
    }}

    .history-list, .fav-list {{
        background: transparent;
        border-radius: 0px;
    }}

    .history-list row, .fav-list row {{
        padding: 6px 8px;
        border-radius: 0px;
        margin: 2px 0;
        transition: background 0.2s ease;
    }}

    .history-list row:hover, .fav-list row:hover {{
        background: {bg_soft};
    }}

    .prefs-label {{
        color: {fg};
        font-weight: 500;
    }}

    switch {{
        background: {bg_soft};
        border-radius: 0px;
    }}

    switch slider {{
        background: {border_alt};
        border-radius: 0px;
    }}

    switch:checked {{
        background: {success};
    }}

    .section-label {{
        color: {accent};
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 8px;
    }}

    .info-label {{
        color: {fg_dim};
        font-size: 12px;
    }}

    .error-label {{
        color: {error};
        font-weight: 500;
    }}

    .success-label {{
        color: {success};
        font-weight: 500;
    }}

    .header-box {{
        background: {bg_alt};
        border-radius: 0px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid {border};
    }}

    .controls-box {{
        background: {bg_alt};
        border-radius: 0px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid {border};
    }}
    """.format(**c)
