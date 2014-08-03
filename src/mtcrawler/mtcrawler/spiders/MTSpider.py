# -*- coding: utf-8 -*-
import time
import urlparse

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http.request import Request

from mtcrawler.items import MTCrawlerItem

ROOT_PAGE = "http://www.my_site.com/"
SLEEP_TIME = 1

class MTSpider(BaseSpider):
    name = "mtcrawler"
    allowed_domains = ["my_site.com"]
    start_urls = [ ROOT_PAGE ]
    already_crawled = set()

    def get_page_id(self, url):
        params = urlparse.parse_qs(urlparse.urlparse(url).query)
        sample_name = "_"
        if params.has_key("Sample"):
            sample_name = params["Sample"][0]
        elif params.has_key("sample"):
            sample_name = params["sample"][0]
        type_name = "_"
        if params.has_key("Type"):
            type_name = params["Type"][0]
        elif params.has_key("type"):
            type_name = params["type"][0]
        return "::".join([sample_name, type_name])
        
    def parse(self, response):
        selector = Selector(response)
        for sel in selector.select("//a"):
            title = sel.xpath("text()").extract()
            if len(title) == 0: continue
            url = sel.xpath("@href").extract()
            if len(url) == 0: continue
            if "sample.asp" in url[0] or "browse.asp" in url[0]:
                child_url = url[0]
                if not child_url.startswith(ROOT_PAGE):
                    child_url = ROOT_PAGE + child_url
                page_id = self.get_page_id(child_url)
                if page_id in self.already_crawled:
                    continue
                self.already_crawled.add(page_id)
                yield Request(child_url, self.parse)
        # now download the file if it is a sample
        if "sample.asp" in response.url:
            item = MTCrawlerItem()
            item["link"] = response.url
            item["body"] = selector.select("//html").extract()[0]
            page_ids = self.get_page_id(response.url).split("::")
            item["sample_name"] = page_ids[0]
            item["type_name"] = page_ids[1]
            yield item
        time.sleep(SLEEP_TIME)
        
