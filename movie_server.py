#!/usr/bin/env python

# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pandora.pandora_models import DatabaseHelper, Movie
import json

class MovieHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        DatabaseHelper.initialize()
        html = self.headerPart()
        html += self.readAllMovies()
        html += self.tailPart()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode(encoding='utf-8'))
        DatabaseHelper.destroy()

    def readAllMovies(self):
        movies = []
        for m in Movie.select():
            mv = m.toJson()
            td = '<tr><td style="width: 20%; align: center">' + mv['title'] + '</td>'
            td += '<td style="width: 30%; align: center">' + mv['language'] + '/' + mv['country'] + '/' + mv['classification'] + '</td>'
            td += '<td style="width: 30%; align: center">' + mv['introduction'] + '</td>'
            td += '<td style="align: center"><a href="' + mv['downloadUrl'] + '">Download Url</a></td>'
            td += '<td style="align: center"><a href="' + mv['thunderTarget'] + '">Thunder Target</a></td></tr>'
            movies.append(td)

        return ''.join(movies)

    def headerPart(self):
        return '''<!DOCTYPE html>
                <html>
                <head>
                    <title>Pandora movies</title
                    <meta charset="utf-8">
                </head>
                <body>
                    <table border="2">
                        <tr>
                            <th>Title</th>
                            <th>Meta</th>
                            <th>Introduction</th>
                            <th>Link</th>
                            <th>Thunder</th>
                        </tr>
                        <tr>'''
    def tailPart(self):
        return '''      </tr>
                    </table>
                </body>
                </html>'''

def main():
    server = HTTPServer(('', 8080), MovieHandler)
    print 'Welcome to pandora server'
    print 'Press ^C once or twice to quit'
    server.serve_forever()

if __name__ == '__main__':
    main()