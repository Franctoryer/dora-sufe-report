import pandas as pd


original_data = pd.read_csv('../datasets/original_data.csv')
sufe_data = original_data[original_data['school_id'] == 16]
sufe_data.to_csv('../datasets/sufe_data.csv', index=False, encoding='utf-8-sig')