# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Data(scrapy.Item):
    # define the fields for your item here like:
    prix = scrapy.Field()
    date = scrapy.Field()
    adresse = scrapy.Field()
    marque = scrapy.Field()
    modele = scrapy.Field()
    carburant = scrapy.Field()
    couleur = scrapy.Field()
    boite = scrapy.Field()
    kilometrage = scrapy.Field()
    annee = scrapy.Field()
    annee_mois = scrapy.Field()
    puissancef = scrapy.Field()
    puissanced = scrapy.Field()
    place = scrapy.Field()
    porte = scrapy.Field()
    loalld = scrapy.Field()
    typev = scrapy.Field()
    permis = scrapy.Field()
    description = scrapy.Field()
    lien = scrapy.Field()
    pro = scrapy.Field()
    temps = scrapy.Field()

class Link(scrapy.Item):
    # define the fields for your item here like:
    lien = scrapy.Field()
    date = scrapy.Field()
