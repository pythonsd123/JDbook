# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbookItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    b_name = scrapy.Field()
    b_href = scrapy.Field()
    s_name = scrapy.Field()
    s_href = scrapy.Field()
    img = scrapy.Field()
    book_href = scrapy.Field()
    publisher = scrapy.Field()
    publish_date = scrapy.Field()
    price = scrapy.Field()

