import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = pd.read_csv('./static/results_no_metadata.csv', lineterminator="\n")
labels_counts = data['label'].value_counts().sort_index()  # 确保按照情感ID排序
emotion_map = {
    0: '悲伤',
    1: '失望',
    2: '讨厌',
    3: '平和',
    4: '疑惑',
    5: '开心',
    6: '期待'
}

size = 0.3
# 将情感ID映射为中文标签
labels = [emotion_map[i] for i in labels_counts.index]

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 创建内外层值的数组
outer_labels = ['负面情绪', '中性情绪', '正面情绪']
inner_labels = labels  # 直接使用所有情感标签作为内层标签

# 根据标签顺序调整值的顺序
vals_outer = np.array([labels_counts[:3].sum(), labels_counts[3:5].sum(), labels_counts[5:].sum()])
vals_inner = labels_counts.values

# 设置颜色
tab20c = plt.get_cmap("tab20c")
outer_colors = [tab20c(i) for i in [0, 4, 8]]
inner_colors = [tab20c(i) for i in [1, 2, 3, 5, 6, 9, 10]]

fig, ax = plt.subplots()

# 定义一个自定义的 autopct 函数来设置数字字体
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%'
    return my_autopct

# 绘制外层饼图
wedges, texts, autotexts = ax.pie(vals_outer, radius=1, colors=outer_colors,
                                  wedgeprops=dict(width=size, edgecolor='w'), 
                                  autopct=make_autopct(vals_outer), pctdistance=0.85)

# 设置外层饼图中的百分比和数值的字体为 Arial
for autotext in autotexts:
    autotext.set_fontproperties({'family': 'Arial', 'size': 10})

# 绘制内层饼图
wedges, texts, autotexts = ax.pie(vals_inner, radius=1-size, colors=inner_colors,
                                  wedgeprops=dict(width=size, edgecolor='w'), 
                                  autopct=make_autopct(vals_inner), pctdistance=0.75)

# 设置内层饼图中的百分比和数值的字体为 Arial
for autotext in autotexts:
    autotext.set_fontproperties({'family': 'Arial', 'size': 10})

# 添加图例
legend_patches = []
for i, label in enumerate(outer_labels + inner_labels):
    if i < len(outer_labels):
        color = outer_colors[i]
    else:
        color = inner_colors[i - len(outer_labels)]
    legend_patches.append(plt.Rectangle((0, 0), 1, 1, fc=color))
plt.legend(legend_patches, outer_labels + inner_labels, loc='upper right', bbox_to_anchor=(1.1, 1))

# 设置图形属性
ax.set(aspect="equal", title='情感分布饼图')
plt.tight_layout()
plt.savefig('./static/pie.pdf')
# 显示图形
plt.show()