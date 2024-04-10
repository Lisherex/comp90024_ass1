import matplotlib.pyplot as plt
import numpy as np


def time_to_seconds_v2(time_str):
    # 分割分钟和秒数，去除末尾的 's'
    minutes, seconds = time_str[:-1].split('m')
    # 转换并计算总秒数
    total_seconds = int(minutes) * 60 + float(seconds)
    return total_seconds

# 应用更新后的函数
times = [
    ("12m35.522s", "11m55.540s", "0m34.497s"),
    ("1m40.652s", "12m30.288s", "0m37.451s"),
    ("1m49.381s", "6m49.639s", "0m20.072s")
]

# 转换所有时间为秒
converted_times = [(time_to_seconds_v2(real), time_to_seconds_v2(user), time_to_seconds_v2(sys)) for real, user, sys in times]



# 设置字体大小
plt.rcParams.update({'font.size': 8})

# 数据：1Node1Core, 1Node8Core, 2Node8Core 的 real, user, sys 时间（以秒为单位）
times_seconds = {
    "1Node1Core": {"real": converted_times[0][0], "user": converted_times[0][1], "sys": converted_times[0][2]},
    "1Node8Core": {"real": converted_times[1][0], "user": converted_times[1][1], "sys": converted_times[1][2]},
    "2Node8Core": {"real": converted_times[2][0], "user": converted_times[2][1], "sys": converted_times[2][2]}
}

# 配置
configurations = list(times_seconds.keys())
time_types = ['real', 'user', 'sys']
n_groups = len(configurations)

# 创建一个数据列表，每个配置一个列表
real_times = [times_seconds[config]['real'] for config in configurations]
user_times = [times_seconds[config]['user'] for config in configurations]
sys_times = [times_seconds[config]['sys'] for config in configurations]

# 转换为 NumPy 数组以便于操作
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8

# 绘制 bar 图
fig, ax = plt.subplots()
bar1 = ax.bar(index, real_times, bar_width, alpha=opacity, label='Real')
bar2 = ax.bar(index + bar_width, user_times, bar_width, alpha=opacity, label='User')
bar3 = ax.bar(index + 2*bar_width, sys_times, bar_width, alpha=opacity, label='Sys')

# 设置图表标题和坐标轴标签
ax.set_xlabel('Configuration')
ax.set_ylabel('Time (h:m:s)')
ax.set_title('Performance Comparison')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(configurations)
ax.legend()

# 函数将秒转换为时分秒格式
def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{}h:{}m:{}s".format(int(h), int(m), int(s))

# 设置 y 轴标签格式为时分秒
ax.set_yticklabels([format_time(tick) for tick in ax.get_yticks()])

# 为每个 bar 添加时分秒格式的时间标签
def add_time_labels(bars):
    for bar in bars:
        height = bar.get_height()
        label = format_time(height)
        ax.annotate(label,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=0)

add_time_labels(bar1)
add_time_labels(bar2)
add_time_labels(bar3)

# 显示图表
plt.tight_layout()
plt.show()
