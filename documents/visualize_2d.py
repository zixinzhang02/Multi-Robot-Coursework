import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.animation import FuncAnimation

# 定义机器人数量和参数
num_robots = 4
radius = 1.0
angular_velocity = 0.1
fov_angle = np.pi / 2  # Field of view angle

# 初始化偏航角
yaw_angles = np.zeros(num_robots)

# 初始化图形
fig, ax = plt.subplots()
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')

# 机器人的初始位置
robot_positions = np.array([[radius * np.cos(i * 2 * np.pi / num_robots),
                             radius * np.sin(i * 2 * np.pi / num_robots)] for i in range(num_robots)])

# 添加虚线框
circle = plt.Circle((0, 0), radius, color='gray', fill=False, linestyle='dashed')
ax.add_patch(circle)

# 绘制机器人
robots, = ax.plot([], [], 'bo')

# 添加相机的可视范围
fov_patches_prev = [Arc((robot_positions[i, 0], robot_positions[i, 1]), 2 * radius, 2 * radius, theta1=np.degrees(yaw_angles[i] - fov_angle / 2),
                theta2=np.degrees(yaw_angles[i] + fov_angle / 2), color='orange', alpha=0.3) for i in range(yaw_angles.shape[0])]
# 更新函数，每个动画帧调用一次
def update(frame):
    global robot_positions, yaw_angles, fov_patches_prev, fov_patched_now

    # 更新偏航角
    yaw_angles += angular_velocity

    # 更新机器人位置
    robot_positions[:, 0] = radius * np.cos(np.arange(num_robots) * 2 * np.pi / num_robots + yaw_angles)
    robot_positions[:, 1] = radius * np.sin(np.arange(num_robots) * 2 * np.pi / num_robots + yaw_angles)

    # 更新相机的可视角度
    fov_patches_now = [Arc((robot_positions[i, 0], robot_positions[i, 1]), 2 * radius, 2 * radius, theta1=np.degrees(yaw_angles[i] - fov_angle / 2),
                theta2=np.degrees(yaw_angles[i] + fov_angle / 2), color='orange', alpha=0.3) for i in range(yaw_angles.shape[0])]
    for fov_patch in fov_patches_now:
        ax.add_patch(fov_patch)
    for patch in ax.patches:
        if patch in fov_patches_prev:
            patch.remove()
    fov_patches_prev = fov_patches_now
    
    # 更新绘图数据
    robots.set_data(robot_positions[:, 0], robot_positions[:, 1])

# 创建动画
animation = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=10)

# 显示动画
plt.show()
