# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import asyncio
import random
from scrapy.http import Request
import requests
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class SearchScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SearchScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

import requests
from scrapy import signals
from scrapy.exceptions import IgnoreRequest

class ProxyMiddleware:
    def __init__(self):
        self.proxy_url = "https://proxy.zivye.asia/get/"
        self.delete_url = "https://proxy.zivye.asia/delete/?proxy={}"
    
    @classmethod
    def from_crawler(cls, crawler):
        # 实例化中间件
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("ProxyMiddleware initialized.")

    def get_proxy(self):
        """从代理池获取一个代理"""
        try:
            response = requests.get(self.proxy_url, timeout=5)
            proxy = response.json().get("proxy")
            return proxy
        except Exception as e:
            return None

    def delete_proxy(self, proxy):
        """从代理池删除失效代理"""
        try:
            requests.get(self.delete_url.format(proxy), timeout=5)
        except Exception as e:
            pass

    def process_request(self, request, spider):
        """为每个请求设置代理"""
        proxy = self.get_proxy()
        if proxy:
            spider.logger.info(f"Using proxy: {proxy}")
            request.meta['proxy'] = f"http://{proxy}"
        else:
            spider.logger.warning("No proxy available!")

    def process_response(self, request, response, spider):
        """处理代理返回的响应"""
        if response.status != 200:  # 如果响应码不是 200，认为代理失效
            proxy = request.meta.get('proxy')
            if proxy:
                spider.logger.warning(f"Deleting invalid proxy: {proxy}")
                self.delete_proxy(proxy.replace("http://", ""))
            raise IgnoreRequest(f"Invalid response with status {response.status}")
        return response

    def process_exception(self, request, exception, spider):
        """捕获请求异常并切换代理"""
        proxy = request.meta.get('proxy')
        if proxy:
            spider.logger.warning(f"Removing failed proxy: {proxy}")
            self.delete_proxy(proxy.replace("http://", ""))
        # 返回新的请求以重新尝试
        new_request = request.copy()
        new_request.meta['proxy'] = f"http://{self.get_proxy()}"
        return new_request

