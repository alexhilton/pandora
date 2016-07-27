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
        # Use to stat how many scraped, how many added and how many discarded.
        self.totalCount = 0
        self.added = 0
        self.notDownloadable = 0
        self.discarded = 0

        DatabaseHelper.initialize()

    def close_spider(self, spider):
        DatabaseHelper.destroy()
        self.stat(spider)

    def process_item(self, item, spider):
        self.totalCount += 1
        if not item.downloadable():
            self.notDownloadable += 1
            return
        if not item.hasMetaInfo():
            self.discarded += 1
            return

        try:
            Movie.get(Movie.downloadUrl == item['downloadUrl'])
        except DoesNotExist:
            item.toMovie().save()
            self.added += 1


    def stat(self, spider):
        if self.totalCount == 0:
            print 'Nothing is scraped for spider ' + spider.name
        print 'Spider ' + spider.name
        print '======================'
        print 'Total scrapped: ' + str(self.totalCount)
        print 'Added: ' + str(self.added)
        print 'Discarded: ' + str(self.discarded)
        print 'Not downloadable: ' + str(self.notDownloadable)
        print 'Existing: ' + str(self.totalCount - self.added - self.notDownloadable - self.discarded)