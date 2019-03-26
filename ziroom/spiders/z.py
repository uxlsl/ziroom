# -*- coding: utf-8 -*-
import scrapy


class ZSpider(scrapy.Spider):
    name = "z"
    allowed_domains = ["gz.ziroom.com"]

    def start_requests(self):
        url = "http://gz.ziroom.com/z/nl/z3.html"
        yield scrapy.Request(url, self.parse_tag)

    def parse_tag(self, response):
        "解出地铁线url"
        for a in response.css(".con .tag a"):
            if a.css("::text").get() == "全部":
                continue
            url = response.urljoin(a.css("::attr('href')").get())
            req = scrapy.Request(url, self.parse_list)
            req.meta["page"] = 1
            req.meta["url"] = url
            yield req

    def parse_list(self, response):
        urls = response.css("#houseList > li > div.txt > h3 > a::attr(href)").getall()
        urls = [response.urljoin(url) for url in urls]
        try:
            cur_page = int(response.css('#page > a.active::text').get())
            if cur_page != response.meta['page']:
                # 已以到底
                return
        except TypeError:
            return
        if urls:
            for url in urls:
                yield scrapy.Request(url, self.parse_detail)
            page = int(response.meta["page"]) + 1
            url = response.meta["url"]
            req =  scrapy.Request("{}?p={}".format(url, page), self.parse_list)
            req.meta["page"] = page
            req.meta["url"] = url
            yield req

    def parse_detail(self, response):
        for i in response.css(".greatRoommate li"):
            roommate = {
                "来源": response.url,
                "性别": i.css("li::attr(class)").get(),
                "房间号": i.css(".user_top p::text").get(),
                "星座": i.css(".sign::text").get(),
                "职业": i.css("p.jobs > span.ellipsis::text").get(),
                "入住时间": i.css(".user_bottom p::text").get().strip(),
                "状态": i.css(".tags::text").get(),
            }
            yield roommate
