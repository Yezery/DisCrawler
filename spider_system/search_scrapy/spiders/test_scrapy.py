import scrapy
from ..utils.nlp_transformers import get_sentiment
from ..utils.fake_agent import get_android_agent
from scrapy.http import Response
from playwright.async_api import Page
class TestScrapySpider(scrapy.Spider):
    name = "test_scrapy"
    # allowed_domains = ["blog.csdn.net"]
    start_urls = [
        "https://www.zhipin.com/web/geek/job?query=&city=101281600"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={"playwright": True, "playwright_include_page": True},
                headers={
                    "User-Agent": get_android_agent(),
                    "Accept-Language": "zh-CN,zh;q=0.9",
                },
                callback=self.parse,
                errback=self.errback_close_page,
            )

    async def parse(self, response:Response):
        page:Page = response.meta.get("playwright_page")
        
       # 等待页面加载
        await page.wait_for_load_state('networkidle')
        
        # tag = await page.query_selector("#article > div.creat-time-box > div > p:nth-child(1) > span")
        # read_count = await tag.inner_text() if tag else "N/A"  # 使用 await 获取文本内容

        # tag = await page.query_selector('#article > div.creat-time-box > span.creat-time > span')
        # create_time = await tag.inner_text() if tag else "N/A"

        # tag = await page.query_selector('#operate > div.clearfix.content-box > div.like-btn.operate_heart.operate_common.floatL > span > span.count')
        # span_count = await tag.inner_text() if tag else "N/A"

        # tag = await page.query_selector('#operate > div.clearfix.content-box > div.collect-btn.operate_add.operate_common.floatL > span > span.count')
        # collection_count = await tag.inner_text() if tag else "N/A"

        # categorys_tmp =await page.query_selector_all("#operate > div.search-tag-box > a")
        # categorys = []
        # for category in categorys_tmp:
        #     category_name = await category.inner_text()
        #     categorys.append(category_name)

        # title_tmp = await page.query_selector("#articleContentId > span.tit")
        # title = await title_tmp.inner_text() if title_tmp else "N/A"
        
        
        # sentiment_score = get_sentiment("The product is really good and I like it.")
        # yield{
        #     "crawl_time": time.time(),
        #     "create_time": convert_to_timestamp(create_time),
        #     "sentiment_score": sentiment_score,
        #     "category": categorys,
        #     "read_count": read_count,
        #     "collection": collection_count,
        #     "blog_digg_num": span_count,
        # }
        

        # await page.wait_for_selector('#get-collection', timeout=60000)
        
       
    async def errback_close_page(self, failure):
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()
        self.logger.error(f"Error occurred: {failure}")

