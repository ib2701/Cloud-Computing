import requests
import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time
import json

PORT_NUMBER = 3000

nasa_key = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)['nasa_key']
weather_key = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)['weather_key']


def date_api(year):
    URL = "https://api.lrs.org/random-date-generator?num_dates=1&year=" + str(year)
    time1 = time.time()
    r = requests.get(url=URL)
    time2 = time.time()
    data = r.json()
    log = {"request": "GET" + URL, "response": data, "latency": str(time2 - time1)}
    f = open("date_api_log.txt", "a")
    f.write(json.dumps(log, indent=3))
    f.close()
    keys = data["data"].keys()
    for date in keys:
        return date


def weather_api(location):
    URL = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + str(weather_key)
    time1 = time.time()
    r = requests.get(url=URL)
    time2 = time.time()
    data = r.json()
    log = {"request": "GET" + URL, "response": data, "latency": str(time2 - time1)}
    f = open("weather_api_log.txt", "a")
    f.write(json.dumps(log, indent=3))
    f.close()
    return data["coord"]["lon"], data["coord"]["lat"]


def nasa_api(lat, lon, date):
    URL = "https://api.nasa.gov/planetary/earth/imagery/?lon=" + str(lon) + "&lat=" + str(lat) + "&date=" + str(date) + "&api_key=" + nasa_key
    time1 = time.time()
    r = requests.get(url=URL)
    time2 = time.time()
    data = r.json()
    log = {"request": "GET" + URL, "response": data, "latency": str(time2 - time1)}
    f = open("nasa_api_log.txt", "a")
    f.write(json.dumps(log, indent=3))
    f.close()
    return data["url"]


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "client.html"
        elif self.path.startswith("/?loc_name="):
            self._set_response()
            loc = self.path.split("=")[1]
            date = date_api(2016)
            lon, lat = weather_api(loc)
            pic = nasa_api(lat, lon, date)
            content = "<img src=" + pic + ">"
            self.wfile.write(content.encode('utf-8'))
            return
        elif self.path.startswith("/metrics"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            with open('date_api_log.txt') as json_file:
                content = str(json.load(json_file))
                content += "\n\n"
            with open('weather_api_log.txt') as json_file:
                content += str(json.load(json_file))
                content += "\n\n"
            with open('nasa_api_log.txt') as json_file:
                content += str(json.load(json_file))

            self.wfile.write(content.encode('utf-8'))
            return

        try:
            content = open(self.path).read()
        except:
            content = "File not found"
        self._set_response()
        self.wfile.write(content.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=PORT_NUMBER):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    run()




