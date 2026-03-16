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
