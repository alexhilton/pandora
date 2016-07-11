# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pandora_models import DatabaseHelper
from pandora_models import Movie
from peewee import DoesNotExist

class PandoraPipeline(object):
    def open_spider(self, spider):
        DatabaseHelper.initialize()

    def close_spider(self, spider):
        DatabaseHelper.destroy()

    def process_item(self, item, spider):
        if not item.downloadable():
            return
        try:
            Movie.get(Movie.downloadUrl == item['downloadUrl'])
        except DoesNotExist:
            item.toMovie().save()