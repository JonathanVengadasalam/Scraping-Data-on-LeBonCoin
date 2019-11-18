# -*- coding: utf-8 -*-
import os
import csv
import scrapy
from ..items import Data

MAIN = "https://www.leboncoin.fr"

FOLDER = "C:/Users/Home-PC/Desktop/scrapy/tp/linkd.csv"

ATTRIBUTES = ["Marque","Modèle","Année-modèle","Kilométrage","Mise en circulation","Carburant",\
    "Boîte de vitesse","Couleur","Puissance fiscale","Puissance DIN","Nombre de place(s)",\
    "Type de véhicule","Permis","Soumis à LOA/LLD"]

KEYS = {"Marque":"marque","Modèle":"modele","Année-modèle":"annee","Kilométrage":"kilometrage",\
    "Mise en circulation":"mise_en_circulation","Carburant":"carburant","Boîte de vitesse":"boite",\
    "Couleur":"couleur","Puissance fiscale":"puissancef","Puissance DIN":"puissanced",\
    "Nombre de place(s)":"place","Type de véhicule":"typev","Permis":"permis","Soumis à LOA/LLD":"loalld"}

def get_urls(folder, main):
        res = []
        if os.path.exists(folder):
            with open(folder) as csvfile:
                links = csv.reader(csvfile, delimiter=',')
                for link in list(links)[1:]:
                    res.append(main + link[0])
        return res

class DataSpider(scrapy.Spider):
    name = "data"

    start_urls = get_urls(FOLDER, MAIN)

    def parse(self, response):
        item = Data()
        item["nom"] = response.xpath("//h1[@class='dgtty']/text()").extract_first()
        item["prix"] = response.xpath("//div[@class='eVLNz']//span/text()").extract_first()
        item["date"] = response.xpath("//div[@class='_14taM']/div[last()]/text()").extract_first()

        for res in response.xpath("//div[@class='_2B0Bw _1nLtd']"):
            tmp = res.xpath(".//div[@class='_3-hZF']/text()").extract_first()
            if tmp in ATTRIBUTES:
                item[KEYS[tmp]] = res.xpath(".//div[@class='_3Jxf3']/text()").extract_first()
        
        sttmp = ""
        for res in response.xpath("//span[@class='content-CxPmi']//text()").extract():
            sttmp += res + chr (9774)
        item["description"] = sttmp

        sttmp = ""
        for res in response.xpath("//div[@class='_1aCZv']/span//text()").extract():
            sttmp += res + chr (9774)
        item["adresse"] = sttmp
        
        yield item
