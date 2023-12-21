import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 定义机器人数量和参数
num_robots = 4
radius = 1.0
angular_velocity = 0.1

# 初始化偏航角
yaw_angles = np.zeros(num_robots)

# 初始化图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([0, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 机器人的初始位置
robot_positions = np.array([[radius * np.cos(i * 2 * np.pi / num_robots),
                             radius * np.sin(i * 2 * np.pi / num_robots),
                             0] for i in range(num_robots)])

# 绘制机器人
robots, = ax.plot([], [], [], 'bo')

# 更新函数，每个动画帧调用一次
def update(frame):
    global robot_positions, yaw_angles

    # 更新偏航角
    yaw_angles += angular_velocity

    # 更新机器人位置
    robot_positions[:, 0] = radius * np.cos(np.arange(num_robots) * 2 * np.pi / num_robots + yaw_angles)
    robot_positions[:, 1] = radius * np.sin(np.arange(num_robots) * 2 * np.pi / num_robots + yaw_angles)

    # 更新绘图数据
    robots.set_data(robot_positions[:, 0], robot_positions[:, 1])
    robots.set_3d_properties(robot_positions[:, 2])

# 创建动画
animation = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=50)

# 显示动画
plt.show()