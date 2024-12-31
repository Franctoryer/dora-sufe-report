import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from datetime import datetime

# 将 10 位时间戳转换为对应的月份
def timestamp_to_month(timestamp: int, format_type: str = 'number') -> int:
    """
    将 10 位时间戳转换为对应的月份。
    
    参数:
    - timestamp (int): 10 位 Unix 时间戳（单位为秒）。
    - format_type (str): 输出格式类型，默认为 'number'，可选值有：
        - 'full': 返回完整的月份名称（如 "January"）
        - 'abbreviated': 返回月份的缩写（如 "Jan"）
        - 'number': 返回月份的数字表示（如 1, 2, ..., 12）
    
    返回:
    - int: 月份的数字表示。
    """
    dt = datetime.fromtimestamp(timestamp)
    if format_type == 'number':
        return dt.month
    else:
        raise ValueError("format_type 必须是 'number'")

# 读取 CSV 文件
df = pd.read_csv('./static/results_no_metadata.csv', lineterminator="\n")

# 将 create_time 列的时间戳转换为月份
df['month'] = df['create_time'].map(timestamp_to_month)

# 情感标签映射
emotion_map = {
    0: '悲伤',
    1: '失望',
    2: '讨厌',
    3: '平和',
    4: '疑惑',
    5: '开心',
    6: '期待'
}

# 将 label 列映射为中文情感标签
df['tag'] = df['label'].map(emotion_map)

# 按月份和情感标签分组，并统计每个月每种情感的数量
monthly_emotions = df.groupby(['month', 'tag']).size().unstack(fill_value=0)

# 计算每个月的总情感数量
monthly_total = monthly_emotions.sum(axis=1)

# 计算每个月各情感的占比
monthly_emotions_percentage = monthly_emotions.div(monthly_total, axis=0) * 100

# 选择一个 colormap，例如 'tab20' 或 'Set3'
cmap = cm.get_cmap('tab20')  # 你可以尝试其他 colormap，如 'Set3', 'viridis', 'plasma' 等
colors = [cmap(i) for i in np.linspace(0, 1, len(emotion_map))]

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 绘制堆叠条形图
fig, ax = plt.subplots(figsize=(12, 6))

# 使用 stackplot 绘制堆叠图
ax.stackplot(monthly_emotions_percentage.index, 
             [monthly_emotions_percentage[col] for col in monthly_emotions_percentage.columns],
             labels=monthly_emotions_percentage.columns, 
             colors=colors)

for month, row in monthly_emotions_percentage.iterrows():
    cumulative_percentage = 0
    for category, percentage in row.items():
        if not np.isnan(percentage):
            ax.annotate(f'{percentage:.1f}%', 
                        xy=(month, cumulative_percentage + percentage / 2), 
                        xytext=(0, 0), 
                        textcoords='offset points', 
                        ha='center', 
                        va='center', 
                        color='black',  # 设置字体颜色为黑色
                        fontsize=10,    # 设置字体大小为 12
                        fontname='Arial',  # 设置字体类型为黑体
                       )
        cumulative_percentage += percentage
# 设置图表标题和标签
ax.set_title('每月各情感的占比分布', fontsize=16)
ax.set_xlabel('月份', fontsize=14)
ax.set_ylabel('情感占比 (%)', fontsize=14)

# 添加图例
ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

# 显示图表
plt.tight_layout()
plt.savefig("./static/每个月的情感分布.pdf")
plt.show()