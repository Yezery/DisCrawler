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
    sentiment_score = scrapy.Field()
    # 记录内容的情感倾向（例如，积极、消极、中性），这在分析用户反馈时尤其有用。
    # 可以进行情感分布分析，观察数据中是否包含大量消极或积极内容。
    category = scrapy.Field()
    # 分类字段，比如新闻、评论、教程等。可以手动添加，也可以基于模型预测。
    # 帮助分类展示内容，比如可以根据类别筛选不同类型的数据展示。
    read_count = scrapy.Field()
    collection = scrapy.Field()
    blog_digg_num = scrapy.Field()


class BossDetailItem(scrapy.Item):
    link = scrapy.Field()
    boss_name = scrapy.Field()
    boss_title = scrapy.Field()
    job_name = scrapy.Field()
    salary_desc = scrapy.Field()
    job_labels = scrapy.Field()
    skills = scrapy.Field()
    job_experience = scrapy.Field()
    job_degree = scrapy.Field()
    city_name = scrapy.Field()
    area_district = scrapy.Field()
    business_district = scrapy.Field()
    location = scrapy.Field()
    brand_name = scrapy.Field()
    brand_stage_name = scrapy.Field()
    brand_industry = scrapy.Field()
    brand_scale_name = scrapy.Field()
    welfare_list = scrapy.Field()
    crawl_time = scrapy.Field()
# {
#     "bossName": "徐女士",
#     "bossTitle": "招聘经理",
#     "jobName": "上市+dubbo方向+双休+自研产品    Java",
#     "salaryDesc": "20-30K",
#     "jobLabels": ["3-5年", "本科"],
#     "skills": [
#         "微服务架构",
#         "SpringBoot",
#         "Spring",
#         "Dubbo",
#         "SVN",
#         "GIT",
#         "Maven",
#         "Oracle",
#     ],
#     "jobExperience": "3-5年",
#     "jobDegree": "本科",
#     "cityName": "广州",
#     "areaDistrict": "黄埔区",
#     "businessDistrict": "科学城",
#     "gps": {
#         "longitude": 113.430502, "latitude": 23.163727
#     },
#     "brandName": "渠道拓展",
#     "brandStageName": "未融资",
#     "brandIndustry": "移动互联网",
#     "brandScaleName": "100-499人",
#     "welfareList": [
#         "节假日大礼包",
#         "带薪年假",
#         "工龄奖",
#         "员工旅游",
#         "开单奖金",
#         "高佣提成",
#         "补充医疗保险",
#         "五险一金",
#         "零食下午茶",
#         "节日福利",
#         "定期体检",
#     ],
# },
