import math

class Speedometer:
    def __init__(self):
        self.velocity = 0.0   # m/s

        # Tunable parameters
        self.deadband = 0.2        # m/s^2 (noise threshold)
        self.damping = 0.99        # drift reduction
        self.max_speed = 50.0      # safety clamp (m/s)

    # =====================
    # REMOVE GRAVITY
    # =====================
    def remove_gravity(self, ax, ay, az, roll, pitch):
        g = 9.81

        roll = math.radians(roll)
        pitch = math.radians(pitch)

        ax_g = -g * math.sin(pitch)
        ay_g = g * math.sin(roll) * math.cos(pitch)
        az_g = g * math.cos(roll) * math.cos(pitch)

        ax_lin = ax * 9.81 - ax_g
        ay_lin = ay * 9.81 - ay_g
        az_lin = az * 9.81 - az_g

        return ax_lin, ay_lin, az_lin

    # =====================
    # UPDATE SPEED
    # =====================
    def update(self, ax, ay, az, roll, pitch, dt):
        # Remove gravity
        ax_lin, ay_lin, az_lin = self.remove_gravity(ax, ay, az, roll, pitch)

        # Choose forward axis (assume X-axis forward)
        acc_forward = ax_lin

        # Deadband to remove noise
        if abs(acc_forward) < self.deadband:
            acc_forward = 0

        # Integrate velocity
        self.velocity += acc_forward * dt

        # Apply damping (reduces drift)
        self.velocity *= self.damping

        # Clamp velocity
        self.velocity = max(min(self.velocity, self.max_speed), -self.max_speed)

        return self.velocity

    # =====================
    # GET SPEED IN KM/H
    # =====================
    def get_speed_kmh(self):
        return self.velocity * 3.6