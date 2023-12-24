# import os
# import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Arc
from matplotlib.patches import Circle

class Scene():
    def __init__(self, num_robots = 4, radius = 1.0, angular_velocity = 0.1):
        # 初始化场景相关参数
        self.num_robots = num_robots
        self.radius = radius
        self.angular_velocity = np.array(angular_velocity).repeat(num_robots)
        self.dt = 0.1 # 时间步长0.1s（通信频率为10Hz）
        # 初始化机器人相位
        self.robot_phases = np.arange(num_robots) * 2 * np.pi / num_robots
        # 根据相位初始化机器人的偏航角
        self.robot_yaw = self.robot_phases + np.pi / 2
        # 根据相位初始化机器人的位置
        self.get_position()
        self.init_plot()

    def init_plot(self):
        # 初始化图形
        self.fig, self.ax = plt.subplots()
        # 更改fig的窗口大小
        self.fig.set_size_inches(6, 6)
        # 初始化轨迹图
        circle = plt.Circle((0, 0), self.radius, color='gray', fill=False, linestyle='dashed')
        self.ax.add_patch(circle)
        # 初始化机器人以及相机可视范围的颜色
        self.colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon'] 
        # 初始化机器人
        self.robots, = self.ax.plot([], [], 'bo')
        # 设置图形的范围
        self.ax.set_xlim([-3, 3])
        self.ax.set_ylim([-3, 3])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        # 初始化相机可视范围
        self.init_fov()

    def init_fov(self):
        # 遍历每个点，画出相应的扇形并保存对象引用
        self.fov_patches_prev = []
        for i in range(self.num_robots):
            center = self.robot_positions[i]
            start_angle = np.degrees(self.robot_yaw[i] - np.pi / 4)
            end_angle = np.degrees(self.robot_yaw[i] + np.pi / 4)
            radius = 2 * self.radius
            # 画扇形
            theta = np.linspace(start_angle, end_angle, 100)
            x = np.append(center[0], center[0] + radius * np.cos(np.radians(theta)))
            y = np.append(center[1], center[1] + radius * np.sin(np.radians(theta)))
            # 绘制扇形
            fov_patch = self.ax.fill(x, y, color=self.colors[i], alpha=0.5)
            self.fov_patches_prev.append(fov_patch)

    def update_plot(self, frames):
        self.update_robots()
        self.update_fovs()

    def get_position(self):
        self.robot_positions = np.array([self.radius * np.cos(self.robot_phases), self.radius * np.sin(self.robot_phases)])
        self.robot_positions = self.robot_positions.T
   
    def update_robots(self):
        self.robot_phases += self.angular_velocity * self.dt
        self.robot_yaw = self.robot_phases + np.pi / 2
        self.get_position()
        self.robots.set_data(self.robot_positions[:, 0], self.robot_positions[:, 1])

    def update_fovs(self):
        self.clear_fovs()
        for i in range(self.num_robots):
            center = self.robot_positions[i]
            start_angle = np.degrees(self.robot_yaw[i] - np.pi / 6)
            end_angle = np.degrees(self.robot_yaw[i] + np.pi / 3)
            # 更新扇形
            theta = np.linspace(start_angle, end_angle, 100)
            x = np.append(center[0], center[0] + 2 * self.radius * np.cos(np.radians(theta)))
            y = np.append(center[1], center[1] + 2 * self.radius * np.sin(np.radians(theta)))
            # 绘制扇形
            fov_patch = self.ax.fill(x, y, color=self.colors[i], alpha=0.5)
            self.fov_patches_prev.append(fov_patch)

    def clear_fovs(self):
        for patch in self.ax.patches:
            patch.remove()
        circle = plt.Circle((0, 0), self.radius, color='gray', fill=False, linestyle='dashed')
        self.ax.add_patch(circle)
        self.robot_phases += self.angular_velocity * self.dt
        self.robot_yaw = self.robot_phases + np.pi / 2
        self.get_position()
        self.robots.set_data(self.robot_positions[:, 0], self.robot_positions[:, 1])
    
    def visualize(self):
        anim = FuncAnimation(self.fig, self.update_plot, frames=np.arange(0, 100), interval=10)
        plt.show()

if __name__ == '__main__':
    scene = Scene()
    scene.visualize()