import scrapy
from ..items import DoraspiderItem

class PostSpider(scrapy.Spider):
    name = "post"
    allowed_domains = ["www.dolacc.cn"]
    # 爬取2024-1-1 ~ 2024-12-27的所有帖子及其相关信息（发帖人、点赞数、评论数、举报书、蹲数等）
    # id ~ (793759, 2125509)
    start_urls = [f"https://cdn.dolacc.com/api/wxPostv2/visitPostCdn?pId={num}&nocache=-1&orderType=0&freshkey=0" for num in range(793759, 2125509)]


    def parse(self, response):
        """处理响应"""
        json_data = response.json()['data']['postDtl']
        item = DoraspiderItem()
        item['pid'] = json_data['id']   # 帖子id
        item['content'] = json_data['name'].replace('\n', '') # 帖子内容
        item['create_time'] = json_data['createtime']   # 发布时间
        item['comment_sum'] = json_data['commentsum'] # 评论个数
        item['dun_num'] = json_data['dunnum'] # 蹲数
        item['hot'] = json_data['hot'] # 热度
        item['jubao_count'] = json_data['jubaocount'] # 举报数
        item['zan_sum'] = json_data['zansum'] # 点赞数
        item['jinghua'] = json_data['jinghua']  # 是否精华
        item['majia'] = json_data['majia'] # 是否匿名
        item['school_id'] = json_data['school_id']  # 学校id（上财是16）
        item['topic_id'] = json_data['topic_id']    # 话题id
        item['risky'] = json_data['risky']  # 风险程度
        # --------- 用户相关 ----------
        item['uid'] = json_data['user']['id']   # 用户id
        item['nickname'] = json_data['user']['nickname']    # 用户昵称
        # 返回对象
        yield item