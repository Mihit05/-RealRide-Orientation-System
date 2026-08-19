from visualize import BikeVisualizer
from kalman import KalmanFilter
import time
import math
import serial
from pid import PIDController
from Speedometer import Speedometer


ser = serial.Serial('COM7', 115200, timeout=1)  # change port
time.sleep(2)  # allow ESP32 reset

# Initialize
viz = BikeVisualizer()
kf_roll = KalmanFilter()
kf_pitch = KalmanFilter()
pid = PIDController(kp=3, ki=0.1, kd=0.05, setpoint=0)
speedo = Speedometer()

prev_time = time.time()

def accel_to_angle(ax, ay, az):
    roll = math.atan2(ay, az)
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))
    return math.degrees(roll), math.degrees(pitch)


def get_data():
    try:
        line = ser.readline().decode().strip()


        if line.startswith("S:"):
            data = line[2:]
            ax, ay, az, gx, gy, gz = map(int, data.split(","))
            return ax, ay, az, gx, gy, gz

    except:
        return None


running = True
while running:
    values = get_data()

    if values is None:
        continue

    ax, ay, az, gx, gy, gz = values
    print(values)

    # Normalize accel
    ax /= 16384.0
    ay /= 16384.0
    az /= 16384.0

    # Gyro scaling
    gx /= 131.0
    gy /= 131.0

    # Time
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time

    # Angles from accel
    roll_acc, pitch_acc = accel_to_angle(ax, ay, az)

    # Kalman filter
    roll = kf_roll.update(roll_acc, gx, dt)
    pitch = kf_pitch.update(pitch_acc, gy, dt)
    control = pid.update(roll, dt)
    velocity = speedo.update(ax, ay, az, roll, pitch, dt)
    speed_kmh = speedo.get_speed_kmh()

    print(f"Roll: {roll:.2f}, Control: {control:.2f}")

    control = pid.update(pitch, dt)   # or roll

# Clamp control
    control = max(min(control, 30), -30)

# Convert to servo angle
    servo_angle = 90 + control
    servo_angle = max(min(servo_angle, 180), 0)
    prev_servo_angle = 90
    alpha = 0.2
    servo_angle = alpha * servo_angle + (1 - alpha) * prev_servo_angle
    prev_servo_angle = servo_angle
    ser.write(f"C:{int(servo_angle)}\n".encode())
    # Visualization
    control = pid.update(pitch, dt)
    running = viz.update(roll, pitch, control, speed_kmh)
    

viz.close()