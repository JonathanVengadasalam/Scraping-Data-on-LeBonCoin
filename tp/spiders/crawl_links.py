# -*- coding: utf-8 -*-
import scrapy
from ..items import Link

class LinkSpider(scrapy.Spider):
    name = "link"

    start_urls = [ 
        "https://www.leboncoin.fr/recherche/?category=2&text=c3%20picasso%20exclusive%202010",
        "https://www.leboncoin.fr/recherche/?category=2&text=audi%20a3%202010%20phase%202&urgent=",
        "https://www.leboncoin.fr/recherche/?category=2&text=peugeot%20207%202011%2090",
        "https://www.leboncoin.fr/recherche/?category=2&text=golf%207%202012%201.6%20tdi"
         ]

    def parse(self, response):
        item = Link()
        for res in response.xpath("//ul[@class='undefined']//li[@class='_3DFQ-']"):
            item["lien"] = res.xpath("./a/@href").extract_first()
            yield item
        
        next_page = response.xpath("//ul[@class='_25feg']/li[last()]/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)