import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import jieba
from typing import List
import re
import warnings

warnings.filterwarnings('ignore')


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

# @@@@@@@@@ 文本向量化 @@@@@@@@@@@@@
# gram 数
GRAM = 1
filter_data = pd.read_csv('../sentimate-analysis/static/results_no_metadata.csv', lineterminator="\n")
filter_data = filter_data[filter_data['label'].isin([5, 6])]
stop_words = open('./stopwords.txt', 'r', encoding='utf-8').read().split('\n')
contents = filter_data['content']
corpus = []
for content in contents:
  content = str(content)
  if content.strip() and len(content) > 3:
    corpus.append(content)

vectorizer = TfidfVectorizer(
  stop_words=stop_words, decode_error='ignore', ngram_range=(GRAM, GRAM),
  max_df=0.8, min_df=5, sublinear_tf=True, tokenizer=chinese_tokenizer, max_features=1000
)
X = vectorizer.fit_transform(corpus)



# @@@@@@@@@@@@@@ LDA 主题建模 @@@@@@@@@@@@@@@@
N_TOPICS = 3
N_TOP_WORDS = 20
lda = LatentDirichletAllocation(
  n_components=N_TOPICS,
  max_iter=50,
  learning_method='batch',
  learning_offset=50,
  doc_topic_prior=0.1,
  topic_word_prior=0.01,
  random_state=42
)
lda.fit(X)

def print_top_words(model, feature_names, n_top_words):
  """打印每个主题下权重较高的关键词"""
  for topic_idx, topic in enumerate(model.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-n_top_words - 1:-1]]))

# 获取词汇表
feature_names = vectorizer.get_feature_names_out()
print_top_words(lda, feature_names, N_TOP_WORDS)
perplexity = lda.perplexity(X)
print(f'Perplexity: {perplexity}')


