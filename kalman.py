import numpy as np

class KalmanFilter:
    def __init__(self):
        # State
        self.angle = 0.0
        self.bias = 0.0
        
        # Covariance matrix
        self.P = np.zeros((2,2))
        
        # Noise parameters (TUNE THESE)
        self.Q_angle = 0.001
        self.Q_bias = 0.003
        self.R_measure = 0.03

    def update(self, new_angle, new_rate, dt):
        # Predict
        rate = new_rate - self.bias
        self.angle += dt * rate

        self.P[0][0] += dt * (dt*self.P[1][1] - self.P[0][1] - self.P[1][0] + self.Q_angle)
        self.P[0][1] -= dt * self.P[1][1]
        self.P[1][0] -= dt * self.P[1][1]
        self.P[1][1] += self.Q_bias * dt

        # Update
        y = new_angle - self.angle
        S = self.P[0][0] + self.R_measure

        K0 = self.P[0][0] / S
        K1 = self.P[1][0] / S

        self.angle += K0 * y
        self.bias += K1 * y

        P00_temp = self.P[0][0]
        P01_temp = self.P[0][1]

        self.P[0][0] -= K0 * P00_temp
        self.P[0][1] -= K0 * P01_temp
        self.P[1][0] -= K1 * P00_temp
        self.P[1][1] -= K1 * P01_temp

        return self.angle