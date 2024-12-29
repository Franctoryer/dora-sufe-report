import pandas as pd
from tqdm import tqdm

sufe_data = pd.read_csv('../datasets/sufe_data.csv')
filter_data = sufe_data[(len(sufe_data['content']) > 3) & (sufe_data['topic_id'] != 24)]
# 保存数据
print(filter_data)
filter_data.to_csv('../datasets/filter_data.csv', index=False, encoding='utf-8-sig')