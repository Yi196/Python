import matplotlib.pyplot as plt
import numpy as np

# 生成示例数据
categories = ['Category 1', 'Category 2', 'Category 3']
time_periods = ['Time 1', 'Time 2', 'Time 3', 'Time 4']
values = np.random.randint(1, 10, size=(len(categories), len(time_periods)))

# 创建图表对象和子图对象
fig, ax = plt.subplots()

# 设置柱状图的宽度
bar_width = 0.2

# 绘制柱状图
for i, category in enumerate(categories):
    x = np.arange(len(time_periods)) + i * bar_width
    ax.bar(x, values[i], width=bar_width, label=category)

# 设置 x 轴刻度和标签
ax.set_xticks(np.arange(len(time_periods)) + bar_width * (len(categories) - 1) / 2)
ax.set_xticklabels(time_periods)

# 设置图例
ax.legend()

# 展示图表
plt.show()