#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/Users/alexhilton/Documents/pandora/')
from pandora.pandora_models import Movie
import json


def main():
    movies = []
    for m in Movie.select().order_by(Movie.date.desc()):
        movies.append(m.toJson())
    print 'Content-Type: application/json\n\n' + json.dumps(movies, indent = 4)

if __name__ == '__main__':
    main()
