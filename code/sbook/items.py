# -*- coding:utf-8 -*-
# @Author: Wei Yi

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TextItem(scrapy.Item):
    book_info = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    img_url = scrapy.Field()

class ImageItem(scrapy.Item):
    img_info = scrapy.Field()
    image_url = scrapy.Field()

class PicWordItem(scrapy.Item):
    image_url = scrapy.Field()
