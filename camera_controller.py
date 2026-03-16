"""
camera_controller.py
====================
Implements a flexible 3D camera for the Solar System Simulator.

Modes
-----
FREE        – WASD fly-through, right-click drag to look, scroll to dolly
FOLLOW      – Camera orbits around a selected planet; scroll to zoom

Key Bindings (handled in main.py input() + here)
-----------
Right Mouse Drag  – Rotate camera
WASD              – Strafe/Forward/Back in FREE mode
Scroll            – Zoom / dolly
F                 – Toggle FREE / FOLLOW
R                 – Reset to default position
"""

from ursina import *


class SolarCameraController(Entity):
    """
    Custom camera controller. Attach to scene; call .update() each frame.
    """

    # ── Tuning constants ──────────────────────────────────────────────
    MOVE_SPEED      = 20.0    # units/sec in FREE mode
    LOOK_SENS       = 40.0    # degrees/sec per normalised mouse delta
    ZOOM_SPEED      = 8.0     # dolly units per scroll tick
    FOLLOW_DISTANCE = 12.0    # default orbit distance in FOLLOW mode
    MIN_ZOOM        = 2.0
    MAX_ZOOM        = 600.0
    SMOOTHING       = 8.0     # lerp factor for smooth camera motion

    def __init__(self):
        super().__init__()
        self.mode = 'FREE'
        self.target_entity = None

        # Internal state
        self._yaw   = 0.0
        self._pitch = -20.0
        self._zoom  = self.FOLLOW_DISTANCE
        self._target_zoom = self._zoom

        # Velocity for smooth free-fly
        self._vel = Vec3(0, 0, 0)

        self._reset_position = Vec3(0, 30, -80)
        camera.position   = self._reset_position
        camera.rotation_x = 15

        # Lock default Ursina mouse sensitivity (we handle it ourselves)
        mouse.locked = False

    # ── Public API ────────────────────────────────────────────────────

    def set_target(self, entity: Entity):
        """Switch to FOLLOW mode, orbiting around `entity`."""
        self.target_entity = entity
        self.mode = 'FOLLOW'
        self._zoom = self.FOLLOW_DISTANCE * max(entity.scale_x, 3)
        self._target_zoom = self._zoom

    def clear_target(self):
        """Return to FREE mode."""
        self.target_entity = None
        self.mode = 'FREE'

    def reset(self):
        """Snap camera back to default overview position."""
        self.clear_target()
        camera.position = self._reset_position
        camera.rotation = Vec3(15, 0, 0)
        self._yaw   = 0.0
        self._pitch = -20.0
        self._zoom  = self.FOLLOW_DISTANCE

    # ── Frame Update ──────────────────────────────────────────────────

    def update(self):
        dt = time.dt
        self._handle_zoom()

        if self.mode == 'FOLLOW' and self.target_entity:
            self._follow_update(dt)
        else:
            self._free_update(dt)

    # ── Zoom (shared) ─────────────────────────────────────────────────

    def _handle_zoom(self):
        scroll= held_keys['scroll up'] - held_keys['scroll down']
        if scroll != 0:
            camaera.z+=scroll*5

    # ── FOLLOW mode ───────────────────────────────────────────────────

    def _follow_update(self, dt: float):
        """Orbit camera around the selected planet."""
        # Right-click drag to rotate orbit
        if mouse.right:
            self._yaw   += mouse.velocity[0] * self.LOOK_SENS * 60 * dt
            self._pitch -= mouse.velocity[1] * self.LOOK_SENS * 60 * dt
            self._pitch  = clamp(self._pitch, -89, 89)

        # Compute spherical orbit position relative to target
        target_pos = self.target_entity.world_position
        yaw_rad    = math.radians(self._yaw)
        pitch_rad  = math.radians(self._pitch)

        offset = Vec3(
            self._zoom * math.cos(pitch_rad) * math.sin(yaw_rad),
            self._zoom * math.sin(pitch_rad),
            self._zoom * math.cos(pitch_rad) * math.cos(yaw_rad),
        )

        desired_pos = target_pos + offset
        camera.position = lerp(camera.position, desired_pos,
                               time.dt * self.SMOOTHING)
        camera.look_at(target_pos, up=Vec3(0, 1, 0))

    # ── FREE mode ─────────────────────────────────────────────────────

    def _free_update(self, dt: float):
        """WASD fly-cam with right-click look."""
        # ── Look ──────────────────────────────────────────────────────
        if mouse.right:
            mouse.locked = True
            self._yaw   += mouse.velocity[0] * self.LOOK_SENS * 60 * dt
            self._pitch -= mouse.velocity[1] * self.LOOK_SENS * 60 * dt
            self._pitch  = clamp(self._pitch, -89, 89)
            camera.rotation = Vec3(self._pitch, self._yaw, 0)
        else:
            mouse.locked = False

        # ── Dolly (scroll) ────────────────────────────────────────────
        # Move forward/back along view axis on scroll in free mode
        scroll = held_keys['scroll up'] - held_keys['scroll down']  
        if scroll:
            camera.position += camera.forward * scroll * self.ZOOM_SPEED

        # ── Translate ─────────────────────────────────────────────────
        speed = self.MOVE_SPEED * (3 if held_keys['shift'] else 1)
        move  = Vec3(0, 0, 0)

        if held_keys['w'] or held_keys['up arrow']:
            move += camera.forward
        if held_keys['s'] or held_keys['down arrow']:
            move -= camera.forward
        if held_keys['a'] or held_keys['left arrow']:
            move -= camera.right
        if held_keys['d'] or held_keys['right arrow']:
            move += camera.right
        if held_keys['q'] or held_keys['page down']:
            move -= Vec3(0, 1, 0)
        if held_keys['e'] or held_keys['page up']:
            move += Vec3(0, 1, 0)

        # Smooth velocity
        target_vel = move.normalized() * speed if move.length() else Vec3(0)
        self._vel  = lerp(self._vel, target_vel, dt * self.SMOOTHING)
        camera.position += self._vel * dt
