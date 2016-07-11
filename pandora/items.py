# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from pandora_models import Movie
from datetime import date

class PandoraItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    publishYear = scrapy.Field()
    country = scrapy.Field()
    classification = scrapy.Field()
    language = scrapy.Field()
    doubanScore = scrapy.Field()
    imdbScore = scrapy.Field()
    size = scrapy.Field()
    duration = scrapy.Field()
    introduction = scrapy.Field()
    downloadUrl = scrapy.Field()
    thunderTarget = scrapy.Field()


    def downloadable(self):
        # if 'downloadUrl' is not empty, we think this item is downloadable
        return self['downloadUrl'].strip() is not ''


    def toMovie(self):
        movie = Movie(downloadUrl = self['downloadUrl'],
                     thunderTarget = self['thunderTarget'])
        if 'url' in self.keys():
            movie.url = self['url']
        else:
            movie.url = ''
        if 'title' in self.keys():
            movie.title = self['title']
        else:
            movie.title = ''
        if 'publishYear' in self.keys():
            movie.publishYear = self['publishYear']
        else:
            movie.publishYear = ''
        if 'country' in self.keys():
            movie.country = self['country']
        else:
            movie.country = ''
        if 'classification' in self.keys():
            movie.classification = self['classification']
        else:
            movie.classification = ''
        if 'language' in self.keys():
            movie.language = self['language']
        else:
            movie.language = ''
        if 'doubanScore' in self.keys():
            movie.doubanScore = self['doubanScore']
        else:
            movie.doubanScore = ''
        if 'imdbScore' in self.keys():
            movie.imdbScore = self['imdbScore']
        else:
            movie.imdbScore = ''
        if 'size' in self.keys():
            movie.size = self['size']
        else:
            movie.size = ''
        if 'duration' in self.keys():
            movie.duration = self['duration']
        else:
            movie.duration = ''
        if 'introduction' in self.keys():
            movie.introduction = self['introduction']
        else:
            movie.introduction = ''

        movie.date = date.today()
        movie.downloaded = False
        return movie