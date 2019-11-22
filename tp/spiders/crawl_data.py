# -*- coding: utf-8 -*-
import os
import csv
import scrapy
from ..items import Data

FOLDER = "C:/Users/Home-PC/Desktop/scrapy/tp/test.csv"

ATTRIBUTES = ["Marque","Modèle","Année-modèle","Kilométrage","Mise en circulation","Carburant",\
    "Boîte de vitesse","Couleur","Puissance fiscale","Puissance DIN","Nombre de place(s)",\
    "Nombre de portes","Type de véhicule","Permis","Soumis à LOA/LLD"]

KEYS = {"Marque":"marque","Modèle":"modele","Année-modèle":"annee","Kilométrage":"kilometrage",\
    "Mise en circulation":"annee_mois","Carburant":"carburant","Boîte de vitesse":"boite",\
    "Couleur":"couleur","Puissance fiscale":"puissancef","Puissance DIN":"puissanced",\
    "Nombre de place(s)":"place","Nombre de portes":"porte","Type de véhicule":"typev",\
    "Permis":"permis","Soumis à LOA/LLD":"loalld"}

def get_urls(folder):
    res = []
    if os.path.exists(folder):
        with open(folder,encoding='utf-8') as file:
            links = csv.DictReader(file)
            for row in links:
                res.append(row["lien"])
    return res

def get_datetime(dt):
    st = dt.split()
    date = st[0].split("/")
    time = st[2].split("h")
    return date[2] + "/" + date[1] + "/" + date[0] + "/" + time[0] + "/" + time[1]

class DataSpider(scrapy.Spider):
    name = "data"

    start_urls = get_urls(FOLDER)

    def parse(self, response):
        item = Data()
        item["prix"] = response.xpath("//div[@class='eVLNz']//span/text()").extract_first()
        item["date"] = response.xpath("//div[@class='_14taM']/div[last()]/text()").extract_first()
        item["lien"] = response.request.url

        for res in response.xpath("//div[@class='_2B0Bw _1nLtd']"):
            tmp = res.xpath(".//div[@class='_3-hZF']/text()").extract_first()
            if tmp in ATTRIBUTES:
                item[KEYS[tmp]] = res.xpath(".//div[@class='_3Jxf3']/text()").extract_first()
        
        sttmp = response.xpath("//h1[@class='dgtty']/text()").extract_first() + chr (9774)
        for res in response.xpath("//span[@class='content-CxPmi']//text()").extract():
            sttmp += res + chr (9774)
        item["description"] = sttmp

        sttmp = ""
        for res in response.xpath("//div[@class='_1aCZv']/span//text()").extract():
            if res != " ": sttmp += res + chr (9774)
        item["adresse"] = sttmp

        if response.xpath("//div[@class='_8rhn3']/span/text()").get() is not None:
            item["pro"] = 1

        item["temps"] = 0
        
        yield item
