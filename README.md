# 🐍 Hand-Controlled Slither Game – ICSG 🎮

>This is a Python-based Snake (Slither) Game controlled entirely by **hand gestures** using **MediaPipe**, **OpenCV**, and **Pygame**. The game leverages computer vision to track your hand in real-time and moves the snake accordingly.

---

## 📽️ About the Project

This is a **gesture-controlled Slither Game**, where your **index finger** acts as the controller! The game combines:

- **Real-time hand tracking** via `MediaPipe`
- **Custom gesture detection** using `OpenCV`
- **Pygame-based snake logic** and rendering

Instead of keyboard keys, the snake moves in the direction of your **index finger**, making the game more interactive and immersive.


## 🎮 How to Play

- 🖐️ Use your **index finger** to control the snake's head.
- 🍎 Eat the food to grow longer.
- 💥 Avoid colliding with yourself!
- ⛔ If the hand goes out of frame, the game pauses/stops.

---

## ✨ Features

- 🖐️ Track your index finger in real-time
- 🟩 Green dot on tracked finger tip (for visual feedback)
- 🐍 Classic snake growth mechanics
- 🍎 Random blinking food
- 🧠 Speed increases after every 5 foods eaten
- 🏁 Real-time score and speed display
- 💀 Game over when snake hits wall or itself
- 🎨 Colorful snake with pseudo 3D design

---

## 🛠️ Requirements

Make sure you have Python 3.7+ installed.

Install the required libraries:
```bash
pip install opencv-python mediapipe pygame

## 🧠 Tech Stack

| Tool         | Role                     |
|--------------|---------------------------|
| Python       | Core programming          |
| OpenCV       | Webcam handling & drawing |
| MediaPipe    | Hand tracking             |
| Pygame       | Game rendering & logic    |
| Threading    | Parallel hand tracking    |

---




