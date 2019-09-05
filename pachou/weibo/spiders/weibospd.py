# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from weibo.items import WeiboItem

from scrapy.pipelines.images import ImagesPipeline


class WeibospdSpider(scrapy.Spider):
    name = 'weibospd'
    allowed_domains = ['www.umei.cc']
    # start_urls = ['http://www.umei.cc/meinvtupian/meinvxiezhen/1.htm']
    base_url = 'https://www.mn52.com/rihanmeinv/'


    def start_requests(self):
        base_url = 'http://www.umei.cc/meinvtupian/meinvxiezhen/1.htm'
        yield scrapy.Request(base_url, callback=self.parse)


    def parse(self, response):
        test = response.xpath("//img/@src").extract()
        for item in test:
            myitem = WeiboItem()  # 实例化item相当于定义一个类
            myitem['image_urls'] = item
            yield myitem
        urls = response.xpath("//div[@class='TypeList']/ul/li/a/@href").extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.item_parse)
        urls = response.xpath("//div[@class='TypeList_2']/ul/li/a/@href").extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.item_parse)
        next_link = response.xpath("//div[@class='NewPages']/ul//a/@href").extract()
        next_text = response.xpath("//div[@class='NewPages']/ul//a/text()").extract()
        if next_text[len(next_text) - 2] == "下一页":
            yield scrapy.Request("http://www.umei.cc/meinvtupian/meinvxiezhen/" + next_link[len(next_link) - 2], callback=self.parse)
        return test
    def item_parse(self,response):
        imgs = response.xpath("//img/@src").extract()
        for item in imgs:
            myitem = WeiboItem()  # 实例化item相当于定义一个类
            myitem['image_urls'] = item
            yield myitem
        next_link = response.xpath("//div[@class='NewPages']/ul//a/@href").extract()
        if next_link[len(next_link) - 1] != '#':
            yield scrapy.Request("http://www.umei.cc/meinvtupian/meinvxiezhen/" + next_link[len(next_link) - 1],
                                 callback=self.item_parse)
        return imgs
