import asyncio
import time
import scrapy
from scrapy.http import Response
from playwright.async_api import Page

from search_scrapy.pipelines import CSDNScrapyPipeline

from ..utils.fake_agent import get_android_agent
from ..utils.nlp_transformers import get_sentiment
from ..utils.convert import convert_to_number, convert_to_timestamp
import re


class WebsiteScrapySpider(scrapy.Spider):
    start_urls = ["https://blog.csdn.net/"]
    name = "csdn_website_scrapy"
    custom_settings = {
        'ITEM_PIPELINES': {
          'search_scrapy.pipelines.CSDNScrapyPipeline':300,
        }
    }
    # 初始化一个集合来存储所有链接
    all_links = set()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={"playwright": True, "playwright_include_page": True},
                headers={
                    "User-Agent": get_android_agent(),
                    "Accept-Language": "zh-CN,zh;q=0.9",
                },
                callback=self.parse_first,
                errback=self.errback_close_page,
            )

    async def parse_first(self, response: Response):
        page: Page = response.meta.get("playwright_page")
        if page is None:
            self.logger.error("Playwright page object not found in response meta!")
            return

        # 无限滚动并抓取内容
        has_more_content = True  # 标记是否有新内容
        last_height = await page.evaluate("() => document.body.scrollHeight")

        while has_more_content:
            # 执行滚动到页面底部
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(5000)  # 等待2秒，确保内容加载完成

            # 获取滚动后新的页面高度
            new_height = await page.evaluate("() => document.body.scrollHeight")

            # 如果页面高度没有变化，说明没有新内容加载，停止滚动
            if new_height == last_height:
                has_more_content = False
            else:
                last_height = new_height
            # 使用正则表达式匹配以 https://blog.csdn.net/*/article 开头的链接
            pattern = r"https://blog\.csdn\.net/.+/article"
            # 获取新的 'active-blog' 中的 <a> 标签
            a_tags = await page.query_selector_all(".blog-recom-item a")
            # await page.wait_for_selector('#get-collection', timeout=60000)
            for a_tag in a_tags:
                link = await a_tag.get_attribute("href")  # 获取 href 属性
                if link and re.match(pattern, link):
                    # 只添加新的链接到集合，避免重复
                    if link not in self.all_links:
                        # 休眠 2秒
                        await asyncio.sleep(2)
                        self.all_links.add(link)
                        yield scrapy.Request(
                            url=link,
                            meta={
                                "playwright": True,
                                "playwright_include_page": True,
                                "link": link,
                            },
                            headers={
                                "User-Agent": get_android_agent(),
                                "Accept-Language": "zh-CN,zh;q=0.9",
                            },
                            callback=self.parse_second,
                            errback=self.errback_close_page,
                        )
              

    async def parse_second(self, response: Response):
        link = response.meta.get("link")
        page: Page = response.meta.get("playwright_page")
        # 等待页面加载
        await page.wait_for_load_state("networkidle")

        # 获取博客标题
        blog_text = await get_init_text(page,"#articleContentId > span.tit")

        # 获取博客观看次数
        read_count = await get_init_text(page,
            "#article > div.creat-time-box > div > p:nth-child(1) > span"
        )

        # 获取博客创建时间
        create_time = await get_init_text(page,
            "#article > div.creat-time-box > span.creat-time > span"
        )

        # 获取点赞数
        span_count = await get_init_text(page,
            "#operate > div.clearfix.content-box > div.like-btn.operate_heart.operate_common.floatL > span > span.count"
        )

        # 获取收藏数
        collection_count = await get_init_text(page,
            "#operate > div.clearfix.content-box > div.collect-btn.operate_add.operate_common.floatL > span > span.count"
        )

        # 获取博客分类
        categorys_tmp = await page.query_selector_all(
            "#operate > div.search-tag-box > a"
        )
        categorys = []
        for category in categorys_tmp:
            category_name = await category.inner_text()
            categorys.append(category_name)

        # 计算情感得分
        sentiment_score = get_sentiment(blog_text)
        yield {
                "link": link,
                "text": blog_text,
                "crawl_time": int(time.time()),
                "create_time": convert_to_timestamp(create_time),
                "sentiment_score": sentiment_score,
                "category": categorys,
                "read_count": convert_to_number(read_count),
                "collection": convert_to_number(collection_count),
                "blog_digg_num": convert_to_number(span_count),
            }
        
        await page.close()

    async def errback_close_page(self, failure):
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()


async def get_init_text(page: Page, selector: str):
    tag = await page.query_selector(selector)
    return await tag.inner_text() if tag else "N/A"
