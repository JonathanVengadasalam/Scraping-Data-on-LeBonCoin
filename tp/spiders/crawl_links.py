# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from datetime import timedelta
from ..items import Link

MAIN = "https://www.leboncoin.fr"
MONTHS = {"nov":"11","dec":"12"}

class LinkSpider(scrapy.Spider):
    name = "link"

    start_urls = [ "https://www.leboncoin.fr/recherche/?category=2&text=bmw%20serie%201" ]

    def parse(self, response):
        item = Link()
        for res in response.xpath("//ul[@class='undefined']//li[@class='_3DFQ-']"):
            item["lien"] = MAIN + res.xpath("./a/@href").extract_first()
            item["date"] = clean_date(res.xpath(".//p[@class='mAnae']/@content").extract_first())
            yield item
        
        next_page = response.xpath("//ul[@class='_25feg']/li[last()]/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

def clean_date(stdate):
    date, time = stdate.split(", ")
    if date == "Aujourd'hui":
        date = datetime.now()
    elif date == "Hier":
        date = datetime.now() - timedelta(1)
    else:
        date = date.split(" ")
        date = datetime(datetime.now().year, MONTHS[date[1]], date[0])
    time = time.split(":")
    return str(date.day) + "/" + str(date.month) + "/" + str(date.year) + " à " + str(time[0]) + "h" + str(time[1])
