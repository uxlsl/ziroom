# -*- coding: utf-8 -*-
import scrapy


class ZSpider(scrapy.Spider):
    name = 'z'
    allowed_domains = ['gz.ziroom.com']

    def start_requests(self):
        url = 'http://gz.ziroom.com/z/nl/z3.html?p={}'
        for page in range(1,51):
            yield scrapy.Request(url.format(page), self.parse_list)

    def parse_list(self, response):
        urls = response.css('#houseList > li > div.txt > h3 > a::attr(href)').getall()
        urls = [response.urljoin(url) for url in urls]
        for url in urls:
            yield scrapy.Request(url, self.parse_detail)

    def parse_detail(self, response):
        for i in response.css('.greatRoommate li'):
            roommate = {
                '来源': response.url,
                '性别': i.css('li::attr(class)').get(),
                '房间号': i.css('.user_top p::text').get(),
                '星座': i.css('.sign::text').get(),
                '职业': i.css('p.jobs > span.ellipsis::text').get(),
                '入住时间': i.css('.user_bottom p::text').get().strip(),
                '状态': i.css('.tags::text').get(),
            }
            yield roommate
