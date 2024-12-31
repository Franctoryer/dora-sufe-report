import pandas as pd

df = pd.read_csv('./static/train.csv')
# 把恐惧和喜欢删了，因为太少了
filter_df = df[(df['label'] != 1) & (df['label'] != 6)]
result = []

def update_label(old: int) -> int:
  mp = {
    0: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    7: 5,
    8: 6
  }
  return mp[old]

for idx, row in filter_df.iterrows():
  content = str(row['content']).strip()
  if len(content) < 4:
    continue
  result.append(row)

result_df = pd.DataFrame(result)
result_df['label'] = result_df['label'].map(update_label)
result_df.to_csv('./static/filter_train.csv', index=False, encoding='utf-8-sig')