# RealRide — Real-Time Bike Orientation & Telemetry System

RealRide reads live accelerometer/gyroscope data from an **ESP32 + MPU6050** mounted on a bike, fuses it into stable roll/pitch angles with a **Kalman filter**, derives a control signal with a **PID controller**, estimates forward speed from linear acceleration, and renders everything in a live **pygame** dashboard. A standalone simulator is included so the pipeline can be tested without hardware.

## Features

- **Sensor fusion** — Kalman filter combines accelerometer angle estimates with gyroscope rate data to produce smooth, drift-corrected roll and pitch (`kalman.py`)
- **PID control loop** — converts filtered roll/pitch into a bounded control/servo output (`pid.py`)
- **Speed estimation** — removes the gravity component from raw acceleration and integrates it to estimate forward velocity in km/h (`Speedometer.py`)
- **Live visualization** — a pygame dashboard shows bike tilt, control arrow, and speed in real time (`visualize.py`)
- **Two ESP32 link options** — serial/USB (`main.py`) or Wi-Fi socket (`Esp32MPUdata.py`)
- **Hardware-free testing** — a small pygame playground for exercising the visualization/physics logic without a live sensor (`virtualbikesim.py`)

## Architecture

```
ESP32 + MPU6050  --(serial or Wi-Fi)-->  main.py
                                            │
                             ┌──────────────┼───────────────┐
                             ▼              ▼                ▼
                        kalman.py       pid.py         Speedometer.py
                       (roll/pitch)   (control out)     (speed est.)
                             │              │                │
                             └──────────────┴────────────────┘
                                            ▼
                                     visualize.py
                                 (live pygame dashboard)
```

## Repository structure

```
.
├── main.py              # Main loop: reads ESP32 over serial, runs the full pipeline
├── Esp32MPUdata.py       # Alternative Wi-Fi (socket) reader for the ESP32 — standalone/experimental
├── kalman.py             # Kalman filter for roll/pitch estimation
├── pid.py                # PID controller
├── Speedometer.py        # Gravity-compensated speed estimation
├── visualize.py          # pygame-based live dashboard (BikeVisualizer)
├── virtualbikesim.py      # Standalone pygame sandbox for testing physics/visuals without hardware
├── requirements.txt
└── .gitignore
```

> **Note:** this repo currently contains the PC-side Python pipeline only. ESP32 firmware (Arduino/PlatformIO code that streams `ax,ay,az,gx,gy,gz` over serial or Wi-Fi) is not yet included — see [Roadmap](#roadmap).

## Hardware

- ESP32 dev board
- MPU6050 (accelerometer + gyroscope), wired over I2C to the ESP32
- USB cable (for serial mode) and/or the ESP32 on the same Wi-Fi network (for socket mode)

The ESP32 is expected to stream lines over serial in the form:

```
S:ax,ay,az,gx,gy,gz
```

and accept servo commands back in the form:

```
C:<angle 0-180>
```

## Setup

```bash
git clone https://github.com/Mihit05/-RealRide-Orientation-System.git
cd -RealRide-Orientation-System
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

**Serial mode** (ESP32 connected over USB): edit the `COM7` port in `main.py` to match your system, then run:

```bash
python main.py
```

**Wi-Fi mode** (ESP32 connected over sockets): edit the `HOST` IP in `Esp32MPUdata.py`, then run:

```bash
python Esp32MPUdata.py
```

**No hardware available?** Try the standalone visual sandbox:

```bash
python virtualbikesim.py
```

## Roadmap

- [ ] Add ESP32 firmware (Arduino/PlatformIO) for the MPU6050 streaming + servo control
- [ ] Move hardcoded serial port / IP into a config file or CLI args
- [ ] Merge `Esp32MPUdata.py` (Wi-Fi path) into the main pipeline
- [ ] Log sensor + speed data to CSV for post-ride analysis

## License

No license has been chosen yet — all rights reserved by default until one is added.
