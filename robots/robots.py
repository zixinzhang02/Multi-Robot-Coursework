import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Arc
from matplotlib.patches import Circle

class Scene():
    def __init__(self, radius, angular_velocity, fov_angle):
        self.radius = radius
        self.angular_velocity = angular_velocity
        self.fov_angle = fov_angle
        self.yaw_angles = 0
        self.robots = robots

    def update(self):
        self.yaw_angles += self.angular_velocity

    def get_position(self):
        return np.array([self.radius * np.cos(self.yaw_angles), self.radius * np.sin(self.yaw_angles)])

    def get_fov(self):
        return Arc((self.get_position()[0], self.get_position()[1]), 2 * self.radius, 2 * self.radius, theta1=np.degrees(self.yaw_angles - self.fov_angle / 2),
                    theta2=np.degrees(self.yaw_angles + self.fov_angle / 2), color='orange', alpha=0.3)
    
class robots():
    def __init__(self, position, velocity, angular_velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.acceleration = acceleration
    def get_position(self):
        return self.position
        