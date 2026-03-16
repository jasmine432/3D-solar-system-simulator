<<<<<<< HEAD
# ☀️ 3D Solar System Simulator

A fully interactive 3D simulation of our Solar System built with **Python** and the **Ursina game engine**.  
Explore all 8 planets in real-time 3D — complete with orbits, axial rotation, Saturn's rings, a star background, and a live HUD.

---

## 🌌 Features

| Feature | Details |
|---|---|
| ☀️ The Sun | Glowing corona effect, central point light |
| 🪐 8 Planets | Mercury through Neptune with accurate relative sizes & colours |
| 🔵 Orbit Paths | Visible orbit rings for every planet |
| 💫 Star Background | 2,500 procedurally generated stars |
| 🌀 Axial Tilt | Each planet tilted at its real-world angle |
| 💍 Saturn's Ring | Translucent ring disc with inner gap |
| 🌍 Earth Atmosphere | Blue atmospheric glow |
| 📷 Free-fly Camera | WASD + mouse look + scroll zoom |
| 🎯 Planet Follow Mode | Click any planet to orbit around it |
| ℹ️ Planet Info Panel | Description, temperature, and day-length facts |
| ⏩ Time Control | Pause, speed up, and slow down simulation |

---

## 🖼️ Screenshots

> Add your own screenshots to this section after running the project!

```
screenshots/overview.png
screenshots/saturn.png
screenshots/earth.png
```

---

## 🛠️ Requirements

- Python **3.9 – 3.11** (recommended)
- pip
- Git

---

## ⚡ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/solar_system_3d.git
cd solar_system_3d
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Simulator

```bash
python main.py
```

---

## 🎮 Controls

| Key / Mouse | Action |
|---|---|
| `W A S D` | Move camera forward / left / back / right |
| `Q / E` | Move camera down / up |
| `Arrow Keys` | Move camera (alternative) |
| `Right Mouse Drag` | Look around / rotate orbit |
| `Scroll Wheel` | Zoom in / out |
| `Click Planet` | Select planet (follow mode + info panel) |
| `Click Empty Space` | Deselect planet, return to free mode |
| `R` | Reset camera to default overview |
| `Space` | Pause / Resume simulation |
| `+` / `-` | Speed up / slow down time (max 50×) |
| `Shift` | Sprint (3× movement speed) |
| `ESC` | Quit |

---

## 📁 Project Structure

```
solar_system_3d/
├── main.py               # Entry point — app loop, input, lighting
├── planets.py            # Planet data, creation, orbit & rotation
├── camera_controller.py  # Free-fly + follow camera
├── star_background.py    # Procedural star field
├── ui_overlay.py         # HUD: speed, pause, planet info
├── assets/
│   ├── textures/         # (optional) PNG texture maps
│   └── models/           # (optional) custom 3D models
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔮 Optional Improvements

- **NASA Textures** — download from [Solar System Scope](https://www.solarsystemscope.com/textures/) and apply via `texture=` on each planet entity
- **Moons** — add `Entity` children parented to each planet pivot
- **Asteroid Belt** — scatter small rocks between Mars and Jupiter
- **Realistic Orbital Physics** — use Kepler's laws for elliptical orbits
- **Sound** — add ambient space music with `Audio()`
- **VR Mode** — Ursina has basic VR support
- **Export Screenshot** — `base64.b64encode(window.screenshot())`

---

## 📜 Licence

MIT — free to use, modify, and distribute.

---

## 🙌 Credits

Built with [Ursina Engine](https://www.ursinaengine.org/) by Pokepetter.  
Planet data sourced from NASA Solar System Exploration.
=======
🌌 3D Solar System Simulator

An interactive 3D Solar System Simulator built with Python using the Ursina game engine.
This project visualizes the Sun and all eight planets with animated orbits and allows users to explore the system using both mouse controls and hand gestures detected through a webcam.

---

🚀 Features

- Real-time 3D Solar System visualization
- Sun and 8 orbiting planets
- Gesture control using MediaPipe
- Mouse camera navigation
- Dynamic star field background
- Planet selection and follow mode
- Adjustable simulation speed
- Pause / Resume planetary motion

---

🧰 Technologies Used

- Python
- Ursina Engine (3D rendering)
- OpenCV (camera input)
- MediaPipe (hand tracking)
- NumPy

---

🎮 Controls

Key / Action| Function
Mouse Drag| Rotate camera
Scroll Wheel| Zoom
W / A / S / D| Move camera
Space| Pause / Resume
+ / -| Change simulation speed
F| Follow selected planet
R| Reset camera
ESC| Exit

Gesture Controls

- Move hand → Rotate solar system
- Pinch fingers → Zoom camera

---

⚙️ Installation

Install dependencies:

pip install ursina mediapipe opencv-python numpy

---

▶️ Run the Simulator

python main.py

---

📂 Project Structure

3D_solar_simulator
│
├── main.py
├── planets.py
├── camera_controller.py
├── gesture_control.py
├── star_background.py
├── ui_overlay.py
└── textures/

---

🎯 Project Goal

This project demonstrates how computer vision and 3D graphics can be combined to create an interactive scientific visualization.

---

📜 License

no License
>>>>>>> 4a7f5145a5a52c4d594b5a33be68c7dc3de7898a
