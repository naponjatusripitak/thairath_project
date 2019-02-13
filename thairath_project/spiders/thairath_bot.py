# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request

class ThairathBotSpider(scrapy.Spider):
    name = 'thairath_bot'
    allowed_domains = ['www.thairath.co.th']
    max_id = 1404218

     #### Pagination ####
    def start_requests(self):
        for i in range(1, self.max_id):
                yield Request('https://www.thairath.co.th/content/{}'.format(i),
                              callback=self.parse)
    #### Collect links and metadata ####
    def parse(self, response):
        json_object = json.loads(response.css("script.next-head::text").extract()[3])
        json_object2 = json.loads(response.css("script.next-head::text").extract()[2])
        type = []
        for l in json_object2['itemListElement']:
            type.append(l['item']['name'])
        scraped_info = {
            'url' : json_object['mainEntityOfPage']['@id'],
            'img' : json_object['image'],
            'title' : json_object['headline'],
            'time' : json_object['datePublished'],
            'text' : json_object['articleBody'],
            'type' : "/".join(type)
        }
        yield scraped_info
