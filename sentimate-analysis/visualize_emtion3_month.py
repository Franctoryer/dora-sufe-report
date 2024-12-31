import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 将 10 位时间戳转换为对应的月份
def timestamp_to_month(timestamp: int) -> int:
    """
    将 10 位 Unix 时间戳转换为对应的月份。
    
    参数:
    - timestamp (int): 10 位 Unix 时间戳（单位为秒）。
    
    返回:
    - int: 月份的数字表示（1 到 12）。
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.month

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

# 情感类别映射
category_map = {
    '悲伤': '消极',
    '失望': '消极',
    '讨厌': '消极',
    '平和': '中性',
    '疑惑': '中性',
    '开心': '积极',
    '期待': '积极'
}

# 将情感标签映射为情感类别
df['category'] = df['tag'].map(category_map)

# 按月份和情感类别分组，并统计每个月每种类别的总情感数量
monthly_categories = df.groupby(['month', 'category']).size().unstack(fill_value=0)

# 计算每个月的总情感数量
monthly_total = monthly_categories.sum(axis=1)

# 计算每个月各情感类别的占比
monthly_categories_percentage = monthly_categories.div(monthly_total, axis=0) * 100

# 选择一个 colormap，例如 'Set2' 或 'Pastel1'
cmap = plt.get_cmap('Set2')  # 你可以尝试其他 colormap，如 'Pastel1', 'Paired' 等
colors = [cmap(i) for i in range(len(monthly_categories_percentage.columns))]

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 绘制堆叠条形图
fig, ax = plt.subplots(figsize=(12, 6))

# 使用 stackplot 绘制堆叠图
ax.stackplot(monthly_categories_percentage.index, 
             [monthly_categories_percentage[col] for col in monthly_categories_percentage.columns],
             labels=monthly_categories_percentage.columns, 
             colors=colors)

for month, row in monthly_categories_percentage.iterrows():
    cumulative_percentage = 0
    for category, percentage in row.items():
        if not np.isnan(percentage):
            ax.annotate(f'{percentage:.1f}%', 
                        xy=(month, cumulative_percentage + percentage / 2), 
                        xytext=(0, 0), 
                        textcoords='offset points', 
                        ha='center', 
                        va='center', 
                        color='black', 
                        fontsize=10,
                        fontname='Arial'
                      )
        cumulative_percentage += percentage
# 设置图表标题和标签
ax.set_title('每月各情感类别的占比分布', fontsize=16)
ax.set_xlabel('月份', fontsize=14)
ax.set_ylabel('情感类别占比 (%)', fontsize=14)

# 添加图例
ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

# 自定义月份标签
month_names = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)

# 显示图表
plt.tight_layout()
plt.savefig("./static/每个月的情感分布（三种）.pdf")
plt.show()