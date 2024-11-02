# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CsdnArticleItem(scrapy.Item):
    link = scrapy.Field()
    text = scrapy.Field()
    crawl_time = scrapy.Field()
    create_time = scrapy.Field()
    # 记录数据的抓取时间，方便做时间趋势分析。
    # 可以用于查看数据的变化趋势、更新频率，或比较不同时间段内的数据差异。
    sentiment_score=scrapy.Field()
    # 记录内容的情感倾向（例如，积极、消极、中性），这在分析用户反馈时尤其有用。
    # 可以进行情感分布分析，观察数据中是否包含大量消极或积极内容。
    category=scrapy.Field()
    # 分类字段，比如新闻、评论、教程等。可以手动添加，也可以基于模型预测。
    # 帮助分类展示内容，比如可以根据类别筛选不同类型的数据展示。
    read_count=scrapy.Field()
    collection=scrapy.Field()
    blog_digg_num=scrapy.Field()