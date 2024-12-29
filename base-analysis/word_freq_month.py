import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import time
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import jieba
import re
from typing import List
import json
from tqdm import tqdm


# 定义自定义分词器，使用 jieba 进行分词
def chinese_tokenizer(text: str) -> List[str]:
  words = jieba.lcut(text)
  filter_words = []
  for word in words:
    word = word.strip()
    word = re.sub(r'[a-zA-Z0-9]', '', word)
    if len(word) <= 1:
      continue
    filter_words.append(word)
  return filter_words


filter_data = pd.read_csv('../datasets/filter_data.csv')
stop_words = open('./stopwords.txt', 'r', encoding='utf-8').read().split('\n')
start_idx = 0
GRAM = 2
# 用于存储每个月份的关键词
monthly_keywords = {}
# 遍历每个月份
for month in tqdm(range(1, 13)):
  start = False
  corpus = []
  for idx, row in filter_data.iloc[start_idx:].iterrows():
    create_time = row['create_time']  # 发帖时间
    content: str = row['content']  # 帖子内容
    time_tuple = time.gmtime(create_time)
    create_month = time_tuple.tm_mon
    if create_month == month:
      content = str(content)
      if content.strip() and len(content) > 3:
        corpus.append(content)
    # 只会遍历到对应年份
    if not start and create_month == month:
      start = True
    if start and create_month != month:
      start_idx = idx
      break
  vectorizer = TfidfVectorizer(
    stop_words=stop_words, decode_error='ignore', ngram_range=(GRAM, GRAM),
    max_df=0.8, min_df=5, sublinear_tf=True, tokenizer=chinese_tokenizer
  )
  X = vectorizer.fit_transform(corpus)
  feature_names = vectorizer.get_feature_names_out()
  feature_names = [name.replace(' ', '') for name in feature_names]
  # 获取每个词语的平均 TF-IDF 值
  tfidf_sum = X.sum(axis=0).A1  # 按列求和，得到每个词语的总 TF-IDF 值
  tfidf_avg = tfidf_sum / X.shape[0]  # 计算每个词语的平均 TF-IDF 值
  
  # 将 (词, 平均 TF-IDF值) 组成元组
  tfidf_scores = list(zip(feature_names, tfidf_avg))
  # 提取每个月份的前 N 个高 TF-IDF 关键词
  N = 20  # 每个月份提取前 10 个关键词
  top_n_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:N]
  kws_map = { kw[0] :kw[-1] for kw in top_n_keywords }
  monthly_keywords[month] = kws_map

with open(f'word_freq_{GRAM}.json', 'w', encoding='utf-8') as json_file:
  json.dump(monthly_keywords, json_file, indent=4, ensure_ascii=False)
 