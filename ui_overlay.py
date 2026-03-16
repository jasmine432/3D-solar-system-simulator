"""
ui_overlay.py
=============
Builds and manages the 2D HUD overlaid on the 3D scene.

HUD components
--------------
  Top-left    : Title + controls cheatsheet
  Bottom-left : Simulation speed indicator
  Bottom-right: Pause/Running state badge
  Center-right: Planet info panel (visible when a planet is selected)
"""

from ursina import *
from ursina.prefabs.panel import Panel


# ─────────────────────────────────────────────────────────────────────
#  Colour constants
# ─────────────────────────────────────────────────────────────────────
C_BG      = color.rgba(0, 0, 0, 160)
C_TEXT    = color.rgba(220, 220, 255, 240)
C_TITLE   = color.rgba(255, 200, 50, 255)
C_DIM     = color.rgba(160, 160, 200, 180)
C_ACCENT  = color.rgba(80, 200, 255, 240)
C_PAUSE   = color.rgba(255, 80, 80, 240)
C_RUN     = color.rgba(80, 255, 130, 240)


def _make_text(txt, pos, scale=1, col=None, parent=None):
    col = col or C_TEXT
    return Text(
        txt,
        position=pos,
        scale=scale,
        color=col,
        parent=parent or camera.ui,
        background=False,
    )


# ─────────────────────────────────────────────────────────────────────
#  Public: create_hud
# ─────────────────────────────────────────────────────────────────────
def create_hud() -> dict:
    """Create all HUD widgets. Returns a dict of references for later updates."""
    hud = {}

    # ── Title ─────────────────────────────────────────────────────────
    hud['title'] = _make_text(
        '☀  3D Solar System Simulator',
        pos=(-0.84, 0.46),
        scale=1.1,
        col=C_TITLE,
    )

    # ── Controls legend ───────────────────────────────────────────────
    controls = (
        'WASD / Arrows  Move\n'
        'Right Drag      Look\n'
        'Scroll          Zoom\n'
        'Click Planet    Follow\n'
        'R               Reset Cam\n'
        'Space           Pause\n'
        '+  /  -         Speed\n'
        'ESC             Quit'
    )
    hud['controls'] = _make_text(
        controls,
        pos=(-0.84, 0.38),
        scale=0.75,
        col=C_DIM,
    )

    # ── Speed display (bottom-left) ───────────────────────────────────
    hud['speed_label'] = _make_text(
        'Speed:  1.00×',
        pos=(-0.84, -0.44),
        scale=0.9,
        col=C_ACCENT,
    )

    # ── Pause badge (bottom-right) ────────────────────────────────────
    hud['state_badge'] = _make_text(
        '▶  RUNNING',
        pos=(0.60, -0.44),
        scale=0.9,
        col=C_RUN,
    )

    # ── Planet info panel (hidden by default) ─────────────────────────
    hud['info_panel'] = Entity(
        parent=camera.ui,
        model='quad',
        scale=(0.34, 0.30),
        position=(0.65, 0.18),
        color=C_BG,
        enabled=False,
    )
    hud['info_name'] = _make_text(
        '',
        pos=(0.50, 0.30),
        scale=1.05,
        col=C_TITLE,
    )
    hud['info_name'].enabled = False

    hud['info_body'] = _make_text(
        '',
        pos=(0.50, 0.22),
        scale=0.78,
        col=C_TEXT,
    )
    hud['info_body'].enabled = False

    hud['info_hint'] = _make_text(
        'Click empty space to deselect',
        pos=(0.50, 0.04),
        scale=0.68,
        col=C_DIM,
    )
    hud['info_hint'].enabled = False

    return hud


# ─────────────────────────────────────────────────────────────────────
#  Update helpers
# ─────────────────────────────────────────────────────────────────────
def update_speed(hud: dict, speed: float):
    hud['speed_label'].text = f'Speed:  {speed:.2f}×'


def update_pause_state(hud: dict, paused: bool):
    if paused:
        hud['state_badge'].text  = '⏸  PAUSED'
        hud['state_badge'].color = C_PAUSE
    else:
        hud['state_badge'].text  = '▶  RUNNING'
        hud['state_badge'].color = C_RUN


def show_planet_info(hud: dict, planet_data: dict):
    hud['info_panel'].enabled = True
    hud['info_name'].enabled  = True
    hud['info_body'].enabled  = True
    hud['info_hint'].enabled  = True

    hud['info_name'].text = f"[ {planet_data['name']} ]"
    hud['info_body'].text = planet_data.get('description', '')


def hide_planet_info(hud: dict):
    hud['info_panel'].enabled = False
    hud['info_name'].enabled  = False
    hud['info_body'].enabled  = False
    hud['info_hint'].enabled  = False
