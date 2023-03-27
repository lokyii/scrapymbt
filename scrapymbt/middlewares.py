# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ScrapymbtSpiderMiddleware:
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
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapymbtDownloaderMiddleware:
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
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumDownloaderMiddleware(object):

    def process_response(self, request, response, spider):
        if request.url[:45] == "http://www.cq.gov.cn/cqgovsearch/search.html?":
            spider.browser.get(request.url)

            # spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#news_list')))
            time.sleep(random.randint(2, 5))

            origin_code = spider.browser.page_source
            # 将源代码构造成为一个Response对象，并返回
            response = HtmlResponse(url=request.url, encoding='utf8', body=origin_code, request=request, status=200)
            return response

        if request.url[:31] == 'http://www.beijing.gov.cn/so/s?':
            spider.browser.get(request.url)

            # 市政府
            if request.url[:39] == 'http://www.beijing.gov.cn/so/s?tab=zcfg':
                # 按日期
                order_by_date = spider.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.toolsnav > div:nth-child(1) > a:nth-child(3)')))
                order_by_date.click()
                # 时间选择
                period_selector = spider.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.toolsul > span:nth-child(1)')))
                period_selector.click()
                # 从
                period_start = spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#stimeqsrq')))
                period_start.clear()
                period_start.send_keys(spider.start_date)
                # 至
                period_end = spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#stimejsrq')))
                period_end.clear()
                period_end.send_keys(spider.end_date)
                # 确定
                confirm = spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#zcdatebtu')))
                confirm.click()
            # 市发改委
            if request.url[:39] == 'http://www.beijing.gov.cn/so/s?tab=ssbm':
                # 按日期
                order_by_date = spider.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.toolsnav > div:nth-child(1) > a:nth-child(3)')))
                order_by_date.click()
                # 时间选择
                period_selector = spider.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#timesSpanId')))
                period_selector.click()
                # 从
                period_start = spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#utimeqsrq')))
                period_start.clear()
                period_start.send_keys(spider.start_date)
                # 至
                period_end = spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#utimejsrq')))
                period_end.clear()
                period_end.send_keys(spider.end_date)
                # 确定
                confirm = spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#datebtu')))
                confirm.click()
                time.sleep(random.randint(1, 3))
                # 北京市发展和改革委员会
                beijingfgw = spider.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#WEBSITENAME北京市发展和改革委员会')))
                beijingfgw.click()

            time.sleep(random.randint(1, 3))

            origin_code = spider.browser.page_source
            # 将源代码构造成为一个Response对象，并返回
            response = HtmlResponse(url=request.url, encoding='utf8', body=origin_code, request=request, status=200)
            return response

        return response




