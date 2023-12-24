import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Arc
from matplotlib.patches import Circle
from matplotlib.patches import Ellipse

class Scene():
    def __init__(self, num_robots = 4, a = 2, b = 1, angular_velocity = 0.1):
        """初始化场景相关参数"""
        self.num_robots = num_robots
        self.a = a
        self.b = b
        self.radius = 1
        self.required_angular_velocity = 0.1
        self.angular_velocity = np.array(angular_velocity).repeat(num_robots)
        self.camera_yaw = [- np.pi / 20, 9 * np.pi / 20]
        # self.angular_velocity[0] += 1
        self.dt = 0.1 # 时间步长0.1s（通信频率为10Hz）
        # 初始化机器人相位
        self.robot_phases = np.arange(num_robots) * 2 * np.pi / num_robots
        self.robot_phases = np.arange(num_robots) * 0.5 * np.pi / num_robots
        # 根据相位初始化机器人的偏航角
        self.robot_yaw = self.robot_phases + np.pi / 2
        # 根据相位初始化机器人的位置
        self.get_position()
        self.init_plot()
        self.distance = np.zeros((self.num_robots, self.num_robots))

    def init_plot(self):
        """初始化图形"""
        self.fig, self.ax = plt.subplots()
        # 更改fig的窗口大小
        self.fig.set_size_inches(6, 6)
        # 初始化轨迹图
        ellipse = Ellipse(xy=(0, 0), width=2*self.a, height=2*self.b, edgecolor='r', fc='None', lw=0.5)
        self.ax.add_patch(ellipse)
        # 初始化机器人以及相机可视范围的颜色
        self.colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon'] 
        # 初始化机器人
        self.robots, = self.ax.plot([], [], 'bo')
        # print(self.robots)
        # 设置图形的范围
        self.ax.set_xlim([-3, 3])
        self.ax.set_ylim([-3, 3])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        # 初始化相机可视范围
        self.init_fov()

    def init_fov(self):
        """初始化相机可视范围"""
        # 遍历每个点，画出相应的扇形并保存对象引用
        self.fov_patches_prev = []
        for i in range(self.num_robots):
            center = self.robot_positions[i]
            start_angle = np.degrees(self.robot_yaw[i] - self.camera_yaw[0])
            end_angle = np.degrees(self.robot_yaw[i] + self.camera_yaw[1])
            radius = 2 * self.radius
            # 画扇形
            theta = np.linspace(start_angle, end_angle, 100)
            x = np.append(center[0], center[0] + radius * np.cos(np.radians(theta)))
            y = np.append(center[1], center[1] + radius * np.sin(np.radians(theta)))
            # 绘制扇形
            fov_patch = self.ax.fill(x, y, color=self.colors[i], alpha=0.5)
            self.fov_patches_prev.append(fov_patch)

    def update(self, frames):
        """更新函数，每个动画帧调用一次"""
        self.update_robots()
        self.update_fovs()

    def get_position(self):
        """根据相位计算机器人的位置"""
        self.robot_positions = np.array([self.a * np.cos(self.robot_phases), self.b * np.sin(self.robot_phases)])
        self.robot_positions = self.robot_positions.T
   
    def update_robots(self):
        """更新机器人相关参数"""
        self.update_phases()
        # self.robot_phases += self.angular_velocity * self.dt
        self.robot_yaw = self.robot_phases + np.pi / 2
        self.get_position()
        self.robots.set_data(self.robot_positions[:, 0], self.robot_positions[:, 1])
        self.calculate_distance()

    def update_phases(self):
        """Core!!!根据控制律更新相位"""
        self.calculate_distance()
        for i in range(self.num_robots):
            if self.check_visibility(i, (i+1)%self.num_robots) is False:
                continue
            distance = self.distance[i][(i+1)%self.num_robots]
            # 需要的距离为根号二倍的半径
            desired_distance = np.sqrt(2) * self.radius
            error = distance - desired_distance
            # print("error_", i, ":", error)
            self.angular_velocity[i] = 0.15 * error + self.required_angular_velocity
        self.robot_phases += self.angular_velocity * self.dt
        
    def calculate_distance(self):
        """求每个机器人之间的距离"""
        for i in range(self.num_robots):
            for j in range(self.num_robots):
                self.distance[i, j] = np.linalg.norm(self.robot_positions[i] - self.robot_positions[j])
                self.distance[j, i] = self.distance[i, j]
        # print(self.distance)

    def update_fovs(self):
        """更新相机可视范围"""
        self.clear_fovs()
        for i in range(self.num_robots):
            is_visible = self.check_visibility(i, (i+1)%self.num_robots)
            if is_visible == False:
                continue
            center = self.robot_positions[i]
            start_angle = np.degrees(self.robot_yaw[i] - self.camera_yaw[0])
            end_angle = np.degrees(self.robot_yaw[i] + self.camera_yaw[1])
            # 更新扇形
            theta = np.linspace(start_angle, end_angle, 100)
            x = np.append(center[0], center[0] + 2 * self.radius * np.cos(np.radians(theta)))
            y = np.append(center[1], center[1] + 2 * self.radius * np.sin(np.radians(theta)))
            # 绘制扇形
            fov_patch = self.ax.fill(x, y, color=self.colors[i], alpha=0.5)
            self.fov_patches_prev.append(fov_patch)

    def clear_fovs(self):
        """清除上一帧的相机可视范围"""
        for patch in self.ax.patches:
            patch.remove()
        ellipse = Ellipse(xy=(0, 0), width=2*self.a, height=2*self.b, edgecolor='r', fc='None', lw=2)
        self.ax.add_patch(ellipse)

    def check_visibility(self, robot_id_observer, robot_id_observed):
        """检查机器人robot_id_observed是否在robot_id_observer的相机可视范围内"""
        # 计算两个机器人之间的距离
        distance = np.linalg.norm(self.robot_positions[robot_id_observer] - self.robot_positions[robot_id_observed])
        # 如果距离大于相机可视范围的两倍，则不可见
        if distance > 2 * self.radius:
            return False
        # 计算两个机器人之间的夹角
        angle = np.arctan2(self.robot_positions[robot_id_observed, 1] - self.robot_positions[robot_id_observer, 1], self.robot_positions[robot_id_observed, 0] - self.robot_positions[robot_id_observer, 0])
        # 计算机器人的偏航角
        self.check_angle()
        yaw = self.robot_yaw[robot_id_observer]
        # 计算相对角度
        relative_angle = angle - yaw
        relative_angle = self.check_angle(relative_angle)
        # 如果相对角度在相机可视范围内，则可见
        if relative_angle > - self.camera_yaw[0] and relative_angle < self.camera_yaw[1]:
            return True
        else:
            return False
        
    def check_angle(self, angle = 0.0):
        for i in range(self.num_robots):
            while self.robot_yaw[i] > np.pi:
                self.robot_yaw[i] -= 2 * np.pi
            while self.robot_yaw[i] < - np.pi:
                self.robot_yaw[i] += 2 * np.pi
        if angle > np.pi:
            angle -= 2 * np.pi
        if angle < - np.pi:
            angle += 2 * np.pi
        return angle

    def visualize(self):
        anim = FuncAnimation(self.fig, self.update, frames=np.arange(0, 100), interval=30)
        plt.show()

if __name__ == '__main__':
    scene = Scene()
    scene.visualize()