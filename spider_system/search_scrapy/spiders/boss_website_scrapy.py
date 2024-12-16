import asyncio
from multiprocessing import process
import re
import time
import scrapy
from scrapy.http import Response
from playwright.async_api import Page, ElementHandle

from search_scrapy.utils.proxy import get_proxy
from ..utils.fake_agent import get_window_agent

from asyncio import Queue


class WebsiteScrapySpider(scrapy.Spider):
    base_url = "https://www.zhipin.com"
    start_urls = ["https://www.zhipin.com/?ka=header-home-logo"]
    name = "boss_website_scrapy"
    job = ""
    data_queue = Queue()
    custom_settings = {
        "ITEM_PIPELINES": {
            "search_scrapy.pipelines.BOSSScrapyPipeline": 300,
        }
    }
    # 初始化一个集合来存储所有链接
    all_links = set()

    def __init__(self, *args, **kwargs):
        super(WebsiteScrapySpider, self).__init__(*args, **kwargs)
        _job = kwargs.get("job")
        _city = kwargs.get("city")
        _start_urls = kwargs.get("start_urls")
        if _job:
            self.job = _job
        if _city:
            self.city = _city
        if _start_urls:
            self.start_urls = _start_urls

    def start_requests(self):
        for url in self.start_urls:
            proxy = get_proxy()  # 从代理池获取代理
            yield scrapy.Request(
                url=url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "proxy": f"http://{proxy}",  # 设置代理
                },
                headers={
                    "User-Agent": get_window_agent(),
                    "Accept-Language": "zh-CN,zh;q=0.9",
                },
                callback=self.parse_first,
                errback=self.errback_close_page,
            )

    async def parse_first(self, response):
        page: Page = response.meta.get("playwright_page")
        if page is None:
            self.logger.error("Playwright page object not found in response meta!")
            return

        # 定义响应处理函数
        async def handle_response(response):
            url_pattern = re.compile(
                r"https://www\.zhipin\.com/wapi/zpgeek/search/joblist\.json"
            )
            if url_pattern.search(response.url) and response.status == 200:
                json_data = await response.json()  # 获取 JSON 数据
                job_list = json_data["zpData"]["jobList"]
                # 提取并合并数据
                await extract_and_yield_items(job_list)

        async def extract_and_yield_items(job_list):
            tags = await page.query_selector_all(".job-list-box > li ")
            for index, job in enumerate(job_list):
                if index >= len(tags):
                    break  # 防止超出范围
                tag = tags[index]

                # 获取链接
                a = await tag.query_selector(".job-card-body.clearfix > a")
                link = await a.get_attribute("href")
                full_link = self.base_url + link

                # 获取经纬度，检查是否存在
                gps = job.get("gps", {})
                longitude = gps.get("longitude") if gps else None
                latitude = gps.get("latitude") if gps else None
                # 获取其他信息
                item = {
                    "link": full_link,
                    "boss_name": job["bossName"],
                    "boss_title": job["bossTitle"],
                    "job_name": await get_init_text(
                        a, ".job-title.clearfix > .job-name"
                    ),
                    "salary_desc": await get_init_text(
                        a, ".job-info.clearfix > .salary"
                    ),
                    "job_labels": job["jobLabels"],
                    "skills": job["skills"],
                    "job_experience": job["jobExperience"],
                    "job_degree": job["jobDegree"],
                    "city_name": job["cityName"],
                    "area_district": job["areaDistrict"],
                    "business_district": job["businessDistrict"],
                    "location": (
                        [longitude, latitude] if longitude and latitude else None
                    ),
                    "brand_name": await get_init_text(
                        tag,
                        ".job-card-body.clearfix > .job-card-right > .company-info > .company-name > a",
                    ),
                    "brand_stage_name": job["brandStageName"],
                    "brand_industry": job["brandIndustry"],
                    "brand_scale_name": job["brandScaleName"],
                    "welfare_list": job["welfareList"],
                    "create_time": int(time.time()),
                }
                await self.data_queue.put(item)

        # 监听响应
        page.on("response", handle_response)

        # 页面交互逻辑
        await page.wait_for_selector(".search-form-con > .ipt-wrap > input")
        await page.wait_for_selector(".btn.btn-search")
        await page.wait_for_selector(".nav-city > .nav-city-box > .switchover-city")

        change_city_btn = await page.query_selector(
            ".nav-city > .nav-city-box > .switchover-city"
        )
        await change_city_btn.click()
        await page.wait_for_selector(".city-query-input > .city-current")
        await page.fill(".city-query-input > .city-current", self.city, timeout=2000)
        choose_city_li_a = await page.query_selector(
            ".city-query-input > .dropdown-list > li:nth-child(1) > a"
        )
        await choose_city_li_a.click()
        await page.wait_for_timeout(2000)
        await page.fill(".search-form-con > .ipt-wrap > input", self.job, timeout=2000)
        await page.wait_for_timeout(2000)
        submit_button = await page.query_selector(".btn.btn-search")
        await submit_button.click()

        # 继续翻页并保持处理
        for i in range(1, 10):  # 根据需要调整循环
            await page.wait_for_selector(".options-pages a")
            next_page = await page.query_selector(f".options-pages a:nth-child({i})")
            await next_page.click()

            # 这里可以根据需要添加额外的处理，比如等待新页面加载
            await asyncio.sleep(5)  # 等待新数据加载

        # 在主逻辑中，持续获取数据
        while not self.data_queue.empty():
            item = await self.data_queue.get()
            yield item

    async def errback_close_page(self, failure):
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()


async def get_init_text(element: ElementHandle, selector: str):
    tag = await element.query_selector(selector)
    return await tag.inner_text() if tag else "N/A"
