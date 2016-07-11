# -*- coding: utf-8 -*-

from peewee import *


class DatabaseHelper(object):
    pandoraDB = SqliteDatabase('pandora_movies.db')

    @staticmethod
    def initialize():
        DatabaseHelper.pandoraDB.connect()
        DatabaseHelper.pandoraDB.create_tables([Movie], safe = True)

    @staticmethod
    def destroy():
        DatabaseHelper.pandoraDB.close()


class Movie(Model):
    url = CharField()
    title = CharField()
    publishYear = CharField()
    country = CharField()
    classification = CharField()
    language = CharField()
    doubanScore = CharField()
    imdbScore = CharField()
    size = CharField()
    duration = CharField()
    introduction = TextField()
    downloadUrl = TextField() # some download url is fucking long, so use text
    thunderTarget = TextField()
    date = DateField()
    downloaded = BooleanField()

    def toJson(self):
        json = {}
        json['url'] = self.url
        json['title'] = self.title
        json['publishYear'] = self.publishYear
        json['country'] = self.country
        json['classification'] = self.classification
        json['language'] = self.language
        json['doubanScore'] = self.doubanScore
        json['imdbScore'] = self.imdbScore
        json['size'] = self.size
        json['duration'] = self.duration
        json['introduction'] = self.introduction
        json['downloadUrl'] = self.downloadUrl
        json['thunderTarget'] = self.thunderTarget
        json['date'] = str(self.date.year) + str(self.date.month) + str(self.date.day)
        json['downloaded'] = self.downloaded

        return json


    class Meta:
        database = DatabaseHelper.pandoraDB

