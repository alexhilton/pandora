#!/usr/bin/env bash

spiders="dygod dygang dy2018"

for spdr in $spiders; do
    scrapy crawl $spdr
done
