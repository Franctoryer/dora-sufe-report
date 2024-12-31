import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('./static/filter_train.csv')
# 设置绘图风格
sns.set(style="whitegrid")
# 获取原始标签并排序（如果需要）
labels = ['悲伤', '恐惧', '失望', '讨厌', '平和', '疑惑', '喜欢', '开心', '期待']
df['tag'] = df['label'].map(lambda x: labels[x])

# 计算每个类别的频数
label_counts = df['label'].value_counts()
# 找到最小的频数值
min_count = label_counts.min()

# 绘制直方图
plt.figure(figsize=(8, 6))  # 设置图形大小
# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

sns.countplot(x='tag', data=df, palette='viridis')

# 添加标题和标签
plt.title('样本的情感类型分布', fontsize=16, fontweight=900)
plt.xlabel('情感类型', fontweight='bold')
plt.ylabel('频数', fontweight='bold')
# 在频数最小的地方绘制水平线
plt.axhline(y=min_count, color='r', linestyle='--', linewidth=1)

# 添加水平线的注释
plt.text(3.8, min_count + 50, f'{min_count}', ha='left', va='bottom', color='r', fontweight=900)


plt.savefig('./static/hist.pdf')
# 显示图形
plt.show()