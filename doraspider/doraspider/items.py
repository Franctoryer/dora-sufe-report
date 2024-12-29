# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoraspiderItem(scrapy.Item):
    """帖子的每行数据，包括帖子内容及其元数据"""
    pid = scrapy.Field()            # 帖子id
    content = scrapy.Field()        # 帖子内容
    create_time = scrapy.Field()    # 创建时间
    comment_sum = scrapy.Field()    # 评论数
    dun_num = scrapy.Field()        # 蹲数
    hot = scrapy.Field()            # 热度
    jubao_count = scrapy.Field()    # 举报数
    zan_sum = scrapy.Field()        # 赞数
    jinghua = scrapy.Field()        # 是否精华
    school_id = scrapy.Field()      # 学校id
    topic_id = scrapy.Field()       # 话题id
    risky = scrapy.Field()          # 风险等级（暂未知，猜测）
    majia = scrapy.Field()          # 是否匿名
    uid = scrapy.Field()            # 用户id
    nickname = scrapy.Field()       # 用户昵称