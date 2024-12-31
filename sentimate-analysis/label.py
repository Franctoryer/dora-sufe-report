# 使用大模型api贴标签，消极（悲伤、恐惧、失望、讨厌）、中性（平和，疑惑）、积极（喜欢、开心）
"""
- 0: 悲伤
- 1: 恐惧
- 2: 失望
- 3: 讨厌
- 4: 平和
- 5: 疑惑
- 6: 喜欢
- 7: 开心
- 8: 期待
"""
import pandas as pd
from dataclasses import dataclass
from threading import Lock, Thread
import csv
from openai import OpenAI
import numpy as np
from tqdm import tqdm


@dataclass
class Result:
  """所有关于帖子的数据"""
  comment_sum: int  # 评论数
  content: str      # 文本内容
  create_time: int  # 发布时间
  dun_num: int      # 蹲数
  hot: int          # 热度
  jinghua: int      # 精华
  jubao_count: int  # 举报数
  topic_id: int     # 话题id
  zan_sum: int      # 点赞数
  label: int        # 所属标签

def get_label(start: int, end: int, batch_size=20) -> None:
  process_data = sample_data.iloc[start:end + 1]
  last_idx = process_data.index[-1]
  result_batch = []
  for idx, data in process_data.iterrows():
    try:
      comment_sum = data['comment_sum']
      content = data['content']
      create_time = data['create_time']
      dun_num = data['dun_num']
      hot = data['hot']
      jinghua = data['jinghua']
      jubao_count = data['jubao_count']
      topic_id = data['topic_id']
      zan_sum = data['zan_sum']
      prompt = f"""
        你现在需要完成一个情感分类任务，我会告诉你一段文本和它对应的，你需要输出其对应的情感类型。
        现有以下9种情感类型：
          - 0: 悲伤
          - 1: 恐惧
          - 2: 失望
          - 3: 讨厌
          - 4: 平和
          - 5: 疑惑
          - 6: 喜欢
          - 7: 开心
          - 8: 期待
        注意，你只允许输出情感类型对应的数字，并且不允许有任何多余的输出。
        另外这段文本来自某个学校的校圈，如果其中出现了敏感词，请不要在意，你只需要客观地给出对应的标签数字即可。
        以下是文本内容：
        {content}
        请输出上述文本的情感类型。切记，你不允许有任何多余的输出，只要输出对应的标签数字即可。
      """
      client = OpenAI(api_key="sk-cd5a7a647c054b74a95394f38af10bbd", base_url="https://api.deepseek.com")

      response = client.chat.completions.create(
          model="deepseek-chat",
          messages=[
              {"role": "system", "content": "你现在需要完成一个情感分类任务，输入一段文本，输出它的情感类型"},
              {"role": "user", "content": prompt}
          ],
          stream=False
      )
      label = response.choices[0].message.content
      result = Result(comment_sum, content, create_time, dun_num, hot, jinghua, jubao_count, topic_id, zan_sum, label)
      result_batch.append(result)
      # 更新进度条
      pbar.update(1)
      pbar.refresh() 

    except Exception as e:
      continue
    # 分块写入
    if idx == last_idx or len(result_batch) >= batch_size:
      with LOCK:
        with open('./static/train.csv', 'a+', encoding='utf-8-sig', newline='') as f:
          writer = csv.writer(f)
          outputs = [result.__dict__.values() for result in result_batch]
          writer.writerows(outputs)
      result_batch = []



def main(thread_num=32) -> None:
  """多线程请求"""
  indexes = np.linspace(0, 30000, thread_num, endpoint=True)
  threholds = []
  threads = []
  for idx in range(len(indexes) - 1):
    left = int(indexes[idx])
    right = int(indexes[idx + 1]) - 1
    threholds.append((left, right))
  for threhold in threholds:
    t = Thread(target=get_label, args=threhold)
    t.start()
    threads.append(t)
  for t in threads:
    t.join()

  print("finished!")

  


if __name__ == '__main__':
  filter_data = pd.read_csv('../datasets/filter_data.csv')
  sample_data = filter_data.sample(n=30000, random_state=42)
  # 进度条
  pbar = tqdm(total=30000, desc='Processing', unit='ops')
  LOCK = Lock()
  with open('./static/train.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['comment_sum', 'content', 'create_time', 'dun_num', 'hot',
                    'jinghua', 'jubao_count', 'topic_id', 'zan_sum', 'label'])
  
  main()