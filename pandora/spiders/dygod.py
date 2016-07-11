# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from pandora.items import PandoraItem
import re
from pandora import patterns

test = False

PATTERN_SIMPLE_TEXT = '.+\s+(.+)$'
PATTERN_SPACE_TEXT = '.+\s+.+\s+(.+)$'
PATTERN_DIGITS = '(\d+)'
PATTERN_SCORE = '.+\s+([0-9.]+)/'
PATTERN_TITLE = '.+\s+.+\s+(.+?)/'
PATTERN_INRO = u'简\s+介'

INTRO_PATTERNS = [
    {'name': 'title', 'index': 1, 'pattern': PATTERN_TITLE},
    {'name': 'publishYear', 'index': 3, 'pattern': PATTERN_DIGITS},
    {'name': 'country', 'index': 4, 'pattern': PATTERN_SPACE_TEXT},
    {'name': 'classification', 'index': 5, 'pattern': PATTERN_SPACE_TEXT},
    {'name': 'language', 'index': 6, 'pattern': PATTERN_SPACE_TEXT},
    {'name': 'doubanScore', 'index': 9, 'pattern': PATTERN_SCORE},
    {'name': 'imdbScore', 'index': 10, 'pattern': PATTERN_SCORE},
    {'name': 'size', 'index': 13, 'pattern': PATTERN_SIMPLE_TEXT},
    {'name': 'duration', 'index': 14, 'pattern': PATTERN_SPACE_TEXT}
]

class DygodSpider(scrapy.Spider):
    name = "dygod"
    allowed_domains = ["dygod.net"]
    start_urls = (
        'http://www.dygod.net/',
    )


    def parse(self, response):
        if response.status is not 200:
            print 'fuck response code is ', response.status
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.title is None:
            print 'something unexcepted happened'
            return
        movieLinks = soup.select('.co_tupian a')
        for link in movieLinks:
            detailUrl = response.urljoin(link['href'])
            yield scrapy.Request(detailUrl, callback = self.parseMovieDetail)


    def parseMovieDetail(self, response):
        if response.status is not 200:
            print 'bad response ' + response.status
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        stuff = soup.find(id = 'Zoom')
        tags = stuff.descendants
        intros = []
        links = []
        for tag in tags:
            if tag.name == 'p':
                intros.append(tag)
            if tag.name == 'td':
                links.append(tag)
        if len(links) == 0:
            print 'oops, there is no links'
            return
        # start extract content and form to object Item
        item = PandoraItem()
        item['url'] = response.url
        # extract the download link
        for lk in links:
            # lk is <td> tag
            a = lk.a
            href = a['href'].strip()
            if href is not '' and href is not '#':
                item['thunderTarget'] = href
            else:
                if 'gccvcpwj' in a:
                    item['thunderTarget'] = a['gccvcpwj']
            item['downloadUrl'] = a.string

        # extract the other information
        self.parseIntros(intros, item)
        yield item


    def parseIntros(self, intros, item):
        for record in INTRO_PATTERNS:
            item[record['name']] = self.extractField(intros[record['index']].string, record['pattern'])
        item['introduction'] = self.parseIntroduction(intros)


    def extractField(self, text, pattern):
        mc = re.search(pattern, text, re.UNICODE)
        if not mc:
            return ''
        return mc.group(1)


    def parseIntroduction(self, intros):
        index = 0
        while index < len(intros):
            text = intros[index].string
            if not text:
                index += 1
                continue
            # 如何判断这个是不是'简介'?
            mc = re.search(PATTERN_INRO, text, re.UNICODE)
            if not mc:
                index += 1
                continue
            else:
                # 找到简介了, 下一条就是简介内容
                return intros[index + 1].string.strip()