# -*- coding: utf-8 -*-
import os
import csv
import scrapy
from datetime import datetime
from datetime import timedelta
from ..items import Link

MAIN = "https://www.leboncoin.fr"
MONTHS = {"nov":"11"}
FOLDER = "C:/Users/Home-PC/Desktop/scrapy/tp/test.csv"

def get_urls(folder):
    res = []
    if os.path.exists(folder):
        with open(folder,encoding='utf-8') as file:
            links = csv.DictReader(file)
            for row in links:
                res.append(row["lien"])
    return res

class LinkSpider(scrapy.Spider):
    name = "checker"

    start_urls = get_urls(FOLDER)

    def parse(self, response):
        item = Link()
        item["date"] = response.xpath("//div[@class='_14taM']/div[last()]/text()").extract_first()
        item["lien"] = response.request.url
        yield item
