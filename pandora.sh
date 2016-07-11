#!/usr/bin/env bash

spiders="dygod dygang"

for spdr in $spiders; do
    scrapy crawl $spdr
done
