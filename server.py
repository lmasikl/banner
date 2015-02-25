# coding=utf-8
import csv
from random import randint
from os.path import curdir, sep
from urlparse import parse_qsl
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from banner import Banner

HOST = '127.0.0.1'
PORT = 8080

CONFIG = {
    'banners': [],
    'count': 0,
}


class Handler(BaseHTTPRequestHandler):

    def __get_category(self):
        categories = [value for k, value in parse_qsl(self.path)]
        if not categories:
            return None

        return categories[randint(0, len(categories))]

    def __get_banner(self):
        banners = CONFIG['banners']
        category = self.__get_category()
        if category is None:
            banner = banners[randint(0, CONFIG['count'])]
        else:
            same = filter(lambda x: category in x.categories, banners)
            banner = same[randint(0, len(same) - 1)]

        return banner if banner.show_count > 0 else None

    def __send(self, mime):
        f = open(curdir + sep + self.path)
        self.send_response(200)
        self.send_header('Content-type', mime)
        self.end_headers()
        result = f.read()
        if mime == 'text/html':
            banner = None
            while banner is None:
                banner = self.__get_banner()

            result = result.format(image_url=banner.image_url)

        self.wfile.write(result)
        f.close()

    def do_GET(self):
        mime = 'text/html'
        if self.path == '/' or self.path.startswith('/?'):
            self.path = 'index.html'

        try:
            send_replay = False
            if self.path.endswith('.html'):
                send_replay = True
            elif self.path.endswith('.jpg'):
                mime = 'image/jpg'
                send_replay = True

            if send_replay:
                self.__send(mime)

        except IOError:
            self.send_error(404, 'Page not found: {0}'.format(self.path))


def read_config(file_path='config.csv'):
    with open(file_path, 'rb') as csv_file:
        lines = csv.reader(csv_file, delimiter=';')
        CONFIG['banners'] = [Banner(line) for line in lines]
        CONFIG['count'] = len(CONFIG['banners']) - 1


def run_server():
    read_config()
    server = HTTPServer((HOST, PORT), Handler)
    try:
        print('Server started on port: {0}'.format(PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server stopped')
        server.socket.close()


if __name__ == '__main__':
    run_server()