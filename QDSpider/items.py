# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Join


class QdBookListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novelId = scrapy.Field()#小说ID
    novelName = scrapy.Field()#小说名字
    novelLink = scrapy.Field()#小说链接
    novelAuthor = scrapy.Field()#小说作者
    novelType = scrapy.Field()#小说类型
    novelStatus = scrapy.Field()#小说状态
    novelWords = scrapy.Field()#小说字数
    novelImageUrl = scrapy.Field()#小说图片

class QdBookDetailItem(scrapy.Item):
    novelId = scrapy.Field()#小说ID
    novelLabel = scrapy.Field()#小说标签
    novelClick = scrapy.Field(
        output_processor=Join()
    )#点击
    novelComm = scrapy.Field(
        output_processor=Join()
    )#推荐
    novelComment = scrapy.Field()#评论数

