import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
from PIL import Image
import numpy as np

# 加载掩码图像并转换为二值图像
# mask_image = imread("./static/mask2.png")
mask_image = np.array(Image.open("./static/mask4.jpeg"))
print(mask_image)
# 加载 JSON 文件
with open('./static/word_freq_total_1.json', 'r', encoding='utf-8') as f:
  tfidf_data = json.load(f)

# 创建 WordCloud 对象
wordcloud = WordCloud(
    height=1500,
    width=1500,
    background_color='white',  # 设置背景颜色为白色
    max_words=100,       # 设置显示的最大单词数量
    colormap='viridis',  # 设置颜色调色板（可以选择其他 colormap）
    font_path='simhei.ttf',  # 如果需要显示中文，指定中文字体路径（可选）
)

wordcloud.fit_words(tfidf_data)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud)
plt.axis('off')  # 关闭坐标轴
wordcloud.to_file('./static/wordcloud.png')
plt.show()