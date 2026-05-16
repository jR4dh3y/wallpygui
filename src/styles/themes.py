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
    }}

    .title-label {{
        font-size: 22px;
        font-weight: 800;
        color: {accent};
        letter-spacing: 1px;
        margin-start: 6px;
    }}

    .preview-frame {{
        border-radius: 0px;
        border: 2px solid {accent};
        background: {bg_alt};
        margin-bottom: 12px;
        padding: 12px;
    }}

    .path-entry, .dir-entry, .search-entry {{
        border-radius: 0px;
        padding: 8px 14px;
        background: {bg_soft};
        color: {fg};
        border: 1px solid {border};
        font-size: 14px;
        min-height: 20px;
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
        padding: 8px 18px;
        border: 1px solid {border};
        transition: all 0.2s ease;
        font-size: 13px;
        min-height: 20px;
    }}

    button:hover {{
        background: {border_alt};
    }}

    .apply-btn {{
        background: {accent};
        color: {bg};
        font-weight: 800;
        padding: 10px 28px;
        font-size: 14px;
        letter-spacing: 0.3px;
        min-width: 150px;
    }}

    .apply-btn:hover {{
        background: {accent};
        opacity: 0.88;
    }}

    .apply-btn:disabled {{
        opacity: 0.45;
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

    .tool-btn {{
        min-width: 110px;
        padding: 8px 18px;
        font-size: 13px;
    }}

    combobox button {{
        padding: 8px 12px;
        min-width: 100px;
        font-size: 13px;
    }}

    .gallery-frame {{
        border-radius: 0px;
        border: 1px solid {border};
        background: {bg_alt};
        padding: 0px;
    }}

    .gallery-scroll {{
        background: {bg_alt};
        border: 1px solid {border};
    }}

    flowboxchild {{
        background: transparent;
        border: none;
        border-radius: 0px;
        padding: 0px;
    }}

    flowboxchild:hover, flowboxchild:selected {{
        background: transparent;
    }}

    .thumbnail-box {{
        background: transparent;
        padding: 8px;
        border-radius: 0px;
        transition: all 0.15s ease;
        border: 2px solid transparent;
    }}

    .thumbnail-box:hover {{
        background: {bg_soft};
        border-color: {accent};
    }}

    /* Selected thumbnail */
    .selected-thumb {{
        border: 2px solid {accent};
        background: {bg_soft};
    }}

    .thumb-label {{
        color: {fg_dim};
        font-size: 12px;
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
        padding: 12px 16px;
        border: 1px solid {border};
    }}

    .controls-box {{
        background: {bg_alt};
        border-radius: 0px;
        padding: 12px 16px;
        border: 1px solid {border};
    }}

    .selected-label {{
        color: {fg};
        font-size: 14px;
        font-weight: 600;
    }}

    .meta-label {{
        color: {fg_dim};
        font-size: 13px;
        font-weight: 600;
    }}

    /* Empty state placeholder */
    .empty-label {{
        color: {fg_dim};
        font-size: 14px;
        font-weight: 500;
    }}
    """.format(**c)
