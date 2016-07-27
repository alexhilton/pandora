#!/usr/bin/env python

import sys
sys.path.insert(0, '/Users/alexhilton/Documents/pandora/')
from pandora.items import PandoraItem

fields = [
    'url',
    'title',
    'publishYear',
    'country',
    'classification',
    'language',
    'doubanScore',
    'imdbScore',
    'size',
    'duration',
    'introduction',
    'downloadUrl',
    'thunderTarget'
]

for f in fields:
    print 'self.' + f + ' = another.' + f