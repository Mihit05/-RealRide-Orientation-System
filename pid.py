class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.setpoint = setpoint

        self.prev_error = 0.0
        self.integral = 0.0

        # Anti-windup limit
        self.integral_limit = 100

    def update(self, measurement, dt):
        error = self.setpoint - measurement

        # Proportional
        P = self.kp * error

        # Integral
        self.integral += error * dt
        self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)
        I = self.ki * self.integral

        # Derivative
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        D = self.kd * derivative

        # Save error
        self.prev_error = error

        # Total output
        output = P + I + D

        return output