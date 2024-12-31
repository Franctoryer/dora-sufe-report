import pandas as pd


df = pd.read_csv('./static/results_no_metadata.csv', lineterminator="\n")
mp = {
  0: '悲伤',
  1: '失望',
  2: '讨厌',
  3: '平和',
  4: '疑惑',
  5: '开心',
  6: '期待'
}

def convert(label: int) -> str:
  return mp[label]

df['label'] = df['label'].map(convert)
print(df)
df.to_csv('./result.csv', index=False, encoding='utf-8-sig')