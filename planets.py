"""
planets.py
==========
Defines all solar system bodies: Sun, 8 planets, and Saturn's ring.
Each planet has realistic relative sizes, orbit radii, speeds, and colours.

Data is intentionally scaled for visual appeal, not strict astrophysical accuracy.
"""

from ursina import *
import math

# ─────────────────────────────────────────────
#  Planet Data
#  Keys: name, radius, orbit_radius, orbit_speed,
#        rotation_speed, color, tilt, ring (optional)
# ─────────────────────────────────────────────
PLANET_DATA = [
    {
        "name": "Mercury",
        "radius": 0.35,
        "orbit_radius": 6,
        "orbit_speed": 4.74,
        "rotation_speed": 0.017,
        # Mid gray-brown — ancient cratered rock, no atmosphere, raw minerals
        # OLD: rgb(169,169,169)   NEW: rgb(158,142,126)  Hex: #9E8E7E
        "color": color.rgb(158, 142, 126),
        "tilt": 0.03,
        "description": "Smallest planet. Closest to the Sun.\nSurface temp: -180°C to 430°C\nDay length: 59 Earth days",
    },
    {
        "name": "Venus",
        "radius": 0.87,
        "orbit_radius": 9,
        "orbit_speed": 3.50,
        "rotation_speed": -0.004,
        # Sulphur yellow — thick CO2 + sulphuric acid cloud layers
        # OLD: rgb(230,200,120)   NEW: rgb(226,201,126)  Hex: #E2C97E
        "color": color.rgb(226, 201, 126),
        "tilt": 177.4,
        "description": "Hottest planet. Thick CO₂ atmosphere.\nSurface temp: ~465°C\nDay length: 243 Earth days",
    },
    {
        "name": "Earth",
        "radius": 0.92,
        "orbit_radius": 13,
        "orbit_speed": 2.98,
        "rotation_speed": 1.0,
        # Ocean blue — dominant colour of the blue marble from space
        # OLD: rgb(70,130,180)   NEW: rgb(27,108,168)  Hex: #1B6CA8
        "color": color.rgb(27, 108, 168),
        "tilt": 23.5,
        "description": "Our home. Only known planet with life.\nSurface temp: -88°C to 58°C\nDay length: 24 hours",
    },
    {
        "name": "Mars",
        "radius": 0.53,
        "orbit_radius": 18,
        "orbit_speed": 2.41,
        "rotation_speed": 0.97,
        # Iron oxide red — Fe2O3 dust covering the entire surface
        # OLD: rgb(188,74,60)   NEW: rgb(160,64,42)  Hex: #A0402A
        "color": color.rgb(160, 64, 42),
        "tilt": 25.2,
        "description": "The Red Planet. Has the tallest volcano.\nSurface temp: -87°C to -5°C\nDay length: 24h 37min",
    },
    {
        "name": "Jupiter",
        "radius": 3.5,
        "orbit_radius": 30,
        "orbit_speed": 1.31,
        "rotation_speed": 2.4,
        # Band tan — average of cream zones + dark orange-brown belts
        # OLD: rgb(210,170,120)   NEW: rgb(212,169,106)  Hex: #D4A96A
        "color": color.rgb(212, 169, 106),
        "tilt": 3.1,
        "description": "Largest planet. Great Red Spot storm.\nMass: 318x Earth\nDay length: 9h 55min",
    },
    {
        "name": "Saturn",
        "radius": 3.0,
        "orbit_radius": 43,
        "orbit_speed": 0.97,
        "rotation_speed": 2.2,
        # Golden band — pale cream body with warm gold banding
        # OLD: rgb(210,190,130)   NEW: rgb(212,188,112)  Hex: #D4BC70
        "color": color.rgb(212, 188, 112),
        "tilt": 26.7,
        "ring": True,
        "description": "Has stunning ring system made of ice & rock.\nDensity: less than water\nDay length: 10h 33min",
    },
    {
        "name": "Uranus",
        "radius": 1.8,
        "orbit_radius": 57,
        "orbit_speed": 0.68,
        "rotation_speed": -1.4,
        # Ice blue — methane absorbs red wavelengths, reflects cyan-blue
        # OLD: rgb(135,206,215)   NEW: rgb(126,204,224)  Hex: #7ECCE0
        "color": color.rgb(126, 204, 224),
        "tilt": 97.8,
        "description": "Rotates on its side. Ice giant.\nSurface temp: -224°C\nDay length: 17h 14min",
    },
    {
        "name": "Neptune",
        "radius": 1.7,
        "orbit_radius": 70,
        "orbit_speed": 0.54,
        "rotation_speed": 1.5,
        # Deep cobalt blue — richer/darker than Uranus, unknown atmospheric absorber
        # OLD: rgb(63,84,186)   NEW: rgb(28,80,176)  Hex: #1C50B0
        "color": color.rgb(28, 80, 176),
        "tilt": 28.3,
        "description": "Windiest planet. Speeds up to 2100 km/h.\nFarthest from Sun\nDay length: 16h 6min",
    },
]


# ─────────────────────────────────────────────
#  Orbit Trail Helper
# ─────────────────────────────────────────────
def create_orbit_ring(orbit_radius: float, color_val=None) -> Entity:
    """Draw a thin circular orbit path using line segments."""
    if color_val is None:
        color_val = color.rgba(255, 255, 255, 40)

    segments = 128
    points = []
    for i in range(segments + 1):
        angle = (i / segments) * math.tau
        x = math.cos(angle) * orbit_radius
        z = math.sin(angle) * orbit_radius
        points.append(Vec3(x, 0, z))

    orbit = Entity()
    for i in range(len(points) - 1):
        line = Entity(
            model=Mesh(vertices=[points[i], points[i + 1]],
                       mode='line', thickness=1),
            color=color_val,
            unlit=True,
        )
        line.parent = orbit
    return orbit


# ─────────────────────────────────────────────
#  Saturn Ring
# ─────────────────────────────────────────────
def create_saturn_ring(parent: Entity) -> Entity:
    """Create Saturn's iconic ring as a flat torus-like disc."""
    ring = Entity(
        parent=parent,
        model='quad',
        scale=(8.5, 8.5, 1),
        rotation_x=90,
        # Ring ice outer — pale gold  Hex: #F0E8D0
        color=color.rgba(240, 232, 208, 180),
        double_sided=True,
        unlit=True,
    )
    # Inner dark gap
    ring_inner = Entity(
        parent=parent,
        model='quad',
        scale=(5.5, 5.5, 1),
        rotation_x=90,
        color=color.rgba(0, 0, 0, 200),
        double_sided=True,
        unlit=True,
    )
    return ring


# ─────────────────────────────────────────────
#  Atmosphere Glow (simple halo)
# ─────────────────────────────────────────────
def create_atmosphere(parent: Entity, radius: float, atm_color) -> Entity:
    atm = Entity(
        parent=parent,
        model='sphere',
        scale=radius * 2.15,
        color=color.rgba(
            atm_color.r * 255,
            atm_color.g * 255,
            atm_color.b * 255,
            30,
        ),
        double_sided=True,
        unlit=True,
    )
    return atm


# ─────────────────────────────────────────────
#  Sun
# ─────────────────────────────────────────────
def create_sun() -> Entity:
    """Create the Sun with a glow halo effect."""
    sun = Entity(
        name='Sun',
        model='sphere',
        scale=5,
        # Photosphere golden yellow  Hex: #FFD700
        color=color.rgb(255, 215, 0),
        unlit=True,
        collider='sphere',
    )
    sun.planet_data = {
        "name": "Sun",
        "description": "The star at the center of our Solar System.\nAge: ~4.6 billion years\nSurface temp: ~5,500°C\nDiameter: 1.39 million km",
    }

    # Outer corona glow
    corona = Entity(
        parent=sun,
        model='sphere',
        scale=1.25,
        # Solar orange corona  Hex: #FFA500
        color=color.rgba(255, 165, 0, 80),
        double_sided=True,
        unlit=True,
    )
    corona2 = Entity(
        parent=sun,
        model='sphere',
        scale=1.55,
        # Deep outer corona  Hex: #FF6B00
        color=color.rgba(255, 107, 0, 30),
        double_sided=True,
        unlit=True,
    )
    return sun


# ─────────────────────────────────────────────
#  Planet Factory
# ─────────────────────────────────────────────
def create_planet(data: dict) -> Entity:
    """Create a single planet entity with orbit pivot, body, and optional ring."""

    # Orbit pivot — rotates to drive the orbital motion
    orbit_pivot = Entity(name=f"{data['name']}_pivot")

    # Planet body parented to pivot, offset by orbit radius
    planet = Entity(
        parent=orbit_pivot,
        name=data['name'],
        model='sphere',
        scale=data['radius'] * 2,
        x=data['orbit_radius'],
        color=data['color'],
        collider='sphere',
    )

    # Store metadata on the entity for UI / camera
    planet.planet_data = data
    planet.orbit_pivot = orbit_pivot
    planet.orbit_angle = 0.0
    planet.orbit_radius = data['orbit_radius']
    planet.orbit_speed = data['orbit_speed']
    planet.rotation_speed = data['rotation_speed']
    planet.body_tilt = data['tilt']

    # Apply axial tilt
    planet.rotation_z = data['tilt']

    # Atmosphere on Earth only
    if data['name'] == 'Earth':
        # Earth atmosphere — real pale blue  Hex: #7EC8E3
        create_atmosphere(planet, data['radius'], color.rgb(126, 200, 227))

    # Saturn ring
    if data.get('ring'):
        create_saturn_ring(planet)

    # Surface detail: add latitude/longitude lines as a wireframe overlay
    wire = Entity(
        parent=planet,
        model='wireframe_sphere' if load_model('wireframe_sphere') else None,
        scale=1.02,
        color=color.rgba(255, 255, 255, 20),
        unlit=True,
    )

    return planet


# ─────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────
def create_solar_system():
    """Instantiate the Sun, all planets, and orbit rings. Returns (planets, sun)."""
    sun = create_sun()
    planets = []

    for data in PLANET_DATA:
        # Orbit ring (visual guide)
        create_orbit_ring(data['orbit_radius'])
        # Planet entity
        planet = create_planet(data)
        # Stagger starting positions so they don't all begin at the same angle
        import random
        planet.orbit_pivot.rotation_y = random.uniform(0, 360)
        planets.append(planet)

    return planets, sun


def update_planets(planets: list, dt: float):
    """
    Called every frame from main.py.
    dt is already scaled by time_scale.
    """
    for planet in planets:
        # Orbital revolution — rotate the pivot around Y axis
        planet.orbit_pivot.rotation_y += planet.orbit_speed * dt

        # Axial self-rotation
        planet.rotation_y += planet.rotation_speed * dt * 30
