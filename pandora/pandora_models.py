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
        json['date'] = '{0:04d}-{1:02d}-{2:02d}'.format(self.date.year, self.date.month, self.date.day)
        json['downloaded'] = self.downloaded

        return json

    def isBetterThan(self, another):
        # Use a balance to weigh two object, if another has a field which self not, increment balance
        # if another lack of a field which self has, decrement balance
        # finally, if balance > 0, means another is better than self
        balance = 0
        if len(another.publishYear) > len(self.publishYear):
            balance += 1
        else:
            balance -= 1
        if len(another.country) > len(self.country):
            balance += 1
        else:
            balance -= 1
        if len(another.classification) > len(self.classification):
            balance += 1
        else:
            balance -= 1
        if len(another.language) > len(self.language):
            balance += 1
        else:
            balance -= 1
        if len(another.doubanScore) > len(self.doubanScore):
            balance += 1
        else:
            balance -= 1
        if len(another.imdbScore) > len(self.imdbScore):
            balance += 1
        else:
            balance -= 1
        if len(another.size) > len(self.size):
            balance += 1
        else:
            balance -= 1
        if len(another.duration) > len(self.duration):
            balance += 1
        else:
            balance -= 1

        return balance > 0

    def updateWith(self, another):
        self.url = another.url
        self.title = another.title
        self.publishYear = another.publishYear
        self.country = another.country
        self.classification = another.classification
        self.language = another.language
        self.doubanScore = another.doubanScore
        self.imdbScore = another.imdbScore
        self.size = another.size
        self.duration = another.duration
        self.introduction = another.introduction
        self.downloadUrl = another.downloadUrl
        self.thunderTarget = another.thunderTarget


    class Meta:
        database = DatabaseHelper.pandoraDB

