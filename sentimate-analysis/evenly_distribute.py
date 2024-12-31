import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv('./static/filter_train.csv')

# 计算每个类别的样本数量
label_counts = df['label'].value_counts()
# 只选择样本数量大于或等于 1841 的类别
valid_labels = label_counts[label_counts >= 1808].index
# 从这些类别中抽取 1841 个样本
df_sampled = df[df['label'].isin(valid_labels)].groupby('label').apply(lambda x: x.sample(n=1808, replace=False)).reset_index(drop=True)

# 分割数据集，80%作为训练集，20%作为测试集
train_df, test_df = train_test_split(df_sampled, test_size=0.2, random_state=42)
# 将训练集保存为CSV文件
train_df.to_csv('../datasets/train.csv', index=False, encoding='utf-8-sig')
# 将测试集保存为CSV文件
test_df.to_csv('../datasets/test.csv', index=False, encoding='utf-8-sig')