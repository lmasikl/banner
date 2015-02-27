# coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import csv
from os.path import curdir, sep
from urlparse import parse_qsl

from banner import Banner

HOST = '127.0.0.1'
PORT = 8080

CONFIG = None


class Handler(BaseHTTPRequestHandler):

    def __send(self, mime, categories):
        f = open(curdir + sep + self.path)
        self.send_response(200)
        self.send_header('Content-type', mime)
        self.end_headers()
        result = f.read()
        if mime == 'text/html':
            banner = get_banner(parse_qsl(categories))
            result = result.format(image_url=banner.image_url)

        self.wfile.write(result)
        f.close()

    def do_GET(self):
        mime = 'text/html'
        categories = self.path
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
                self.__send(mime, categories)

        except IOError:
            self.send_error(404, 'Page not found: {0}'.format(self.path))


def get_banner(categories):
    """
    Don't understand how to use globals
    """
    if not len(CONFIG):
        return None

    # Get requested categories
    categories = set([value for k, value in categories[:]])
    # Make intersection with banners categories
    banner_intersection_length = [
        {'index': i, 'intersections': len(list(categories.intersection(b1.categories)))}
        for i, b1 in enumerate(CONFIG)
    ]
    # Sort by max intersections
    sorted_banners = sorted(
        banner_intersection_length, key=lambda b2: b2['intersections'], reverse=True
    )
    # Filter by max intersection
    max_intersection = sorted_banners[0]['intersections']
    filtered_banners = filter(lambda b: b['intersections'] == max_intersection, sorted_banners)
    # Sort by max Banner.show_count
    sorted_banners = sorted(
        filtered_banners, key=lambda b3: CONFIG[b3['index']].show_count, reverse=True
    )
    # Get first banner
    banner = CONFIG[sorted_banners[0]['index']]
    if banner.show_count == 1:
        CONFIG.pop(sorted_banners[0]['index'])

    return banner


def read_config(file_path='config.csv'):
    """
    >>> read_config('test_config.csv') #doctest: +ELLIPSIS
    [<banner.Banner object at 0x...>]
    """
    with open(file_path, 'rb') as csv_file:
        lines = csv.reader(csv_file, delimiter=';')
        config = [Banner(line) for line in lines]
    return config


def run_server():
    """
    >>> run_server()
    Server started on 127.0.0.1:8080
    Server stopped

    Didn't find how to simulate ctrl-c
    """
    server = HTTPServer((HOST, PORT), Handler)
    try:
        print('Server started on {host}:{port}'.format(host=HOST, port=PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server stopped')
        server.socket.close()


if __name__ == '__main__':
    CONFIG = read_config()
    run_server()