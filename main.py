"""
3D Solar System Simulator
=========================
Entry point for the Solar System Simulator built with Ursina Engine.
Run this file to launch the simulation.
"""

from ursina import *
from gesture_control import GestureController
from planets import create_solar_system, update_planets
from camera_controller import SolarCameraController
from star_background import create_star_field
import ui_overlay


# ─────────────────────────────────────────────
# App Initialisation
# ─────────────────────────────────────────────
app = Ursina(
    title='3D Solar System Simulator',
    borderless=False,
    fullscreen=False,
    size=(1280,720),
    vsync=True,
)

window.color = color.black
window.fps_counter.enabled = True
window.exit_button.visible = False


# ─────────────────────────────────────────────
# Gesture Controller
# ─────────────────────────────────────────────
gesture = GestureController()


# ─────────────────────────────────────────────
# Lighting
# ─────────────────────────────────────────────
sun_light = PointLight(shadows=True)
sun_light.position = Vec3(0,0,0)
sun_light.color = color.white

ambient = AmbientLight()
ambient.color = Color(0.08,0.08,0.12,1)


# ─────────────────────────────────────────────
# Scene
# ─────────────────────────────────────────────
star_field = create_star_field(count=2500, radius=900)

planet_entities, sun_entity = create_solar_system()


# ─────────────────────────────────────────────
# Camera Controller
# ─────────────────────────────────────────────
camera_controller = SolarCameraController()


# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
hud = ui_overlay.create_hud()


# ─────────────────────────────────────────────
# Simulation State
# ─────────────────────────────────────────────
paused = False
time_scale = 1.0
selected_planet = None


# ─────────────────────────────────────────────
# Input
# ─────────────────────────────────────────────
def input(key):

    global paused, time_scale, selected_planet

    if key == 'escape':
        application.quit()

    if key == 'space':
        paused = not paused
        ui_overlay.update_pause_state(hud, paused)

    if key == '+' or key == '=':
        time_scale = min(time_scale * 1.5, 50.0)
        ui_overlay.update_speed(hud, time_scale)

    if key == '-':
        time_scale = max(time_scale / 1.5, 0.05)
        ui_overlay.update_speed(hud, time_scale)

    if key == 'r':
        camera_controller.reset()

    # Planet selection
    if key == 'left mouse down':

        hit = raycast(
            camera.world_position,
            camera.forward,
            distance=1000,
            ignore=[camera_controller]
        )

        if hit.hit and hasattr(hit.entity, 'planet_data'):

            selected_planet = hit.entity
            camera_controller.set_target(hit.entity)

            ui_overlay.show_planet_info(
                hud,
                hit.entity.planet_data
            )

        else:

            selected_planet = None
            camera_controller.clear_target()
            ui_overlay.hide_planet_info(hud)


# ─────────────────────────────────────────────
# Update Loop
# ─────────────────────────────────────────────
def update():

    global paused

    # Gesture update
    gesture.update()

    # If hand detected → gesture camera
    if gesture.is_hand_detected():

        rot_x, rot_y = gesture.get_rotation()

        camera.rotation_x = rot_x
        camera.rotation_y = rot_y
        camera.z = gesture.get_zoom()

    # Otherwise normal camera controller
    else:
        camera_controller.update()

    # Planet motion
    if not paused:
        update_planets(planet_entities, time.dt * time_scale)

    # Rotate starfield slowly
    star_field.rotation_y += time.dt * 0.005


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────
app.run()