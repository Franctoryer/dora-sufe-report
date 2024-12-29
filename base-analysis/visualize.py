import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

# 选择一个 colormap，例如 'tab20' 或 'Set3'
cmap = cm.get_cmap('tab20')  # 你可以尝试其他 colormap，如 'Set3', 'viridis', 'plasma' 等
# 根据关键词数量生成颜色
colors = [cmap(i) for i in np.linspace(0, 1, 20)]

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 加载 JSON 文件
with open('./word_freq_2.json', 'r', encoding='utf-8') as f:
    monthly_keywords = json.load(f)

# 设置图形大小
plt.figure(figsize=(12, 8))

# 定义月份顺序
months = list(monthly_keywords.keys())

# 遍历每个月份
for i, month in enumerate(months):
    # 获取当前月份的关键词及其 TF-IDF 值
    keywords = monthly_keywords[month]
    
    # 按 TF-IDF 值从大到小排序
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=False)
    
    # 提取关键词和对应的 TF-IDF 值
    labels, values = zip(*sorted_keywords)
    
    # 计算每个关键词的累计高度（用于堆叠）
    cumulative_heights = np.cumsum(values) - values
    
    # 生成堆叠条形图
    for j, (label, value, cum_height, color) in enumerate(zip(labels, values, cumulative_heights, colors)):
        plt.bar(i, value, bottom=cum_height, label=label, alpha=0.7, color=color)
        
        # 在每个块上标注关键词
        plt.text(i, cum_height + value / 2, label, ha='center', va='center', fontsize=8)

# 设置 x 轴标签为月份
plt.xticks(range(len(months)), months)
plt.xlabel('月份')
plt.ylabel('TF-IDF 权重')
plt.title('各个月份关键词的 TF-IDF', fontsize=16, fontweight='bold')

# 不显示图例
plt.legend().set_visible(False)

# 显示图形
plt.tight_layout()
plt.savefig('gram2.pdf', bbox_inches='tight')
plt.show()