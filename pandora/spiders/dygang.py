# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from pandora.items import PandoraItem
import re
from pandora import patterns

test = False

PATTERN_MAP = {
    'title': u'译\s+名\s+(.+)$',
    'country': u'国\s+家\s+(.+)$',
    'classification': u'类\s+别\s+(.+)$',
    'language': u'语\s+言\s+(.+)$',
    'publishYear': u'上映日期\s+(.+)$',
    'doubanScore': u'豆瓣评分\s+([0-9.]+)',
    'imdbScore': u'IMDb评分\s+([0-9.]+)',
    'duration': u'片\s+长\s+(.+)$'
}

class DygodSpider(scrapy.Spider):
    name = "dygang"
    allowed_domains = ["dygang.com"]
    start_urls = (
        'http://www.dygang.com/',
    )


    def parse(self, response):
        if response.status is not 200:
            print 'fuck response code is ', response.status
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.title is None:
            print 'something unexcepted happened'
            return
        movieLinks = soup.find_all('a', class_ = 'c2')
        for link in movieLinks:
            detailUrl = link['href']
            if detailUrl is not '':
                yield scrapy.Request(detailUrl, callback=self.parseMovieDetail)

    def parseMovieDetail(self, response):
        if response.status is not 200:
            print 'shit response code is ', response.status
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        movieInfo = soup.find_all(id = 'dede_content')
        if len(movieInfo) is not 1:
            print 'Warning, you should fix your dygang spider'
        tags = movieInfo[0].descendants
        intros = []
        links = []
        for t in tags:
            if t.name == 'p':
                intros.append(t)
            if t.name == 'td':
                links.append(t)
        if len(links) == 0:
            print 'Oops, no link target, skip this page'
            return

        # parse the links
        item = PandoraItem()
        item['url'] = response.url
        for lk in links:
            if lk.a is not None:
                url = lk.a['href'].strip()
                if url is not '' and not url.startswith('http'):
                    item['downloadUrl'] = url
                    item['thunderTarget'] = url
                    break
        # The meta info
        index = 0
        for p in intros:
            index += 1
            if not p.text:
                continue
            text = p.text.strip()
            if not text:
                continue
            self.extractMetaInfo(text, item)
            break

        index -= 1
        # now the introduction
        while index < len(intros):
            if not intros[index].text:
                index += 1
                continue
            text = intros[index].text.strip()
            if not text:
                index += 1
                continue
            m = re.search(patterns.PATTERN_INRO, text, re.UNICODE)
            if m is not None:
                item['introduction'] = intros[index + 1].text.strip()
                break

            index += 1

        item['size'] = ''
        if 'downloadUrl' not in item.keys() and 'thunderTarget' not in item.keys():
            # this is not a downloadable item, because now links, skip it
            return

        if 'downloadUrl' not in item.keys():
            item['downloadUrl'] = item['thunderTarget']
        if 'thunderTarget' not in item.keys():
            item['thunderTarget'] = item['downloadUrl']

        yield item

    def extractMetaInfo(self, text, item):
        lines = text.split('\n')
        for ln in lines:
            for key in PATTERN_MAP.keys():
                mc = re.search(PATTERN_MAP[key], ln, re.UNICODE)
                if mc is not None:
                    item[key] = mc.group(1)