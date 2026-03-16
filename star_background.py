"""
star_background.py
==================
Generates a dense procedural star field by randomly placing small sphere
entities on the surface of a large invisible sphere.

Stars vary in:
  - Size      (tiny to small)
  - Brightness (dim to bright white/blue-white)
  - A handful of coloured stars (red giants, blue giants) for realism
"""

from ursina import *
import random
import math


def create_star_field(count: int = 2000, radius: float = 800) -> Entity:
    """
    Spawn `count` star points distributed uniformly on a sphere of `radius`.
    Returns a parent Entity so the caller can rotate the whole field.
    """
    parent = Entity(name='StarField', unlit=True)

    # Star colour palette — weighted toward white
    palette = (
        [color.white]         * 60 +   # most stars are white
        [color.rgb(200, 220, 255)] * 20 +  # blue-white
        [color.rgb(255, 240, 200)] * 12 +  # yellow-white
        [color.rgb(255, 200, 150)] * 5  +  # orange
        [color.rgb(255, 120, 80)]  * 3     # red giants
    )

    for _ in range(count):
        # Uniform random point on sphere surface (Marsaglia method)
        while True:
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            z = random.uniform(-1, 1)
            d = x*x + y*y + z*z
            if 0.0001 < d <= 1.0:
                break
        d = math.sqrt(d)
        pos = Vec3(x / d, y / d, z / d) * radius

        star_size = random.uniform(0.08, 0.55)
        star_color = random.choice(palette)

        # Dim stars slightly for depth illusion
        brightness = random.uniform(0.4, 1.0)
        sc = color.rgba(
            int(star_color.r * 255 * brightness),
            int(star_color.g * 255 * brightness),
            int(star_color.b * 255 * brightness),
            255,
        )

        star = Entity(
            parent=parent,
            model='sphere',
            scale=star_size,
            position=pos,
            color=sc,
            unlit=True,
        )

    return parent
