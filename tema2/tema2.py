import sqlite3
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

PORT_NUMBER = 3000
conn = sqlite3.connect('musicDB.db')
c = conn.cursor()


def song_exists(song, genre, artist):
    c.execute('SELECT * from songs where song = "{}" and genre = "{}" and artist = "{}"'.format(song, genre, artist))
    result = c.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def song_name_exists(song):
    c.execute('SELECT * from songs where song = "{}"'.format(song))
    result = c.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def song_genre_exists(genre):
    c.execute('SELECT * from songs where genre = "{}"'.format(genre))
    result = c.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def song_artist_exists(artist):
    c.execute('SELECT * from songs where artist = "{}"'.format(artist))
    result = c.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def convert_to_json(rows):
    dictionary = dict()
    for row in rows:
        dictionary[row[0]] = {"Name": row[1], "Genre": row[2], "Artist": row[3]}
    return json.dumps(dictionary)


def convert_message_to_json(message):
    return json.dumps({"Message": message})


class S(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/?song="):
            song = self.path.split("=")[1]
            try:
                c.execute('SELECT * from songs where song = "{}"'.format(song))
                result = c.fetchall()
                if len(result) == 0:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Song not found"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = convert_to_json(result)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Song could not be returned."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return
        elif self.path.startswith("/?genre="):
            genre = self.path.split("=")[1]
            try:
                c.execute('SELECT * from songs where genre = "{}"'.format(genre))
                result = c.fetchall()
                if len(result) == 0:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Genre not found"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = convert_to_json(result)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Songs could not be returned."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return
        elif self.path.startswith("/?artist="):
            artist = self.path.split("=")[1]
            try:
                c.execute('SELECT * from songs where artist = "{}"'.format(artist))
                result = c.fetchall()
                if len(result) == 0:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Artist not found"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = convert_to_json(result)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Songs could not be returned."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return

    def do_POST(self):
        path = self.path.split("/?", 1)[1]
        parameters = str(path).split("&")
        if len(parameters) == 3:
            song = parameters[0].split("=")[1]
            genre = parameters[1].split("=")[1]
            artist = parameters[2].split("=")[1]

            c.execute('SELECT max(id) from songs')
            result = c.fetchall()
            id = int(result[0][0])
            id = id + 1

            try:
                if not song_exists(song, genre, artist):
                    c.execute('INSERT into songs values ("{id}", "{song}", "{genre}", "{artist}")'.format(id=id, song=song, genre=genre, artist=artist))
                    conn.commit()
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Song " + song + " by " + artist + " has been added succesfully to your database."
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(409)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Song already exists in the database."
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Song could not be added to the database."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return
        elif len(parameters) == 4:
            song = parameters[0].split("=")[1]
            genre = parameters[1].split("=")[1]
            artist1 = parameters[2].split("=")[1]
            artist2 = parameters[3].split("=")[1]

            c.execute('SELECT max(id) from songs')
            result = c.fetchall()
            id = int(result[0][0])
            id1 = id + 1
            id2 = id + 2

            try:
                if not song_exists(song, genre, artist1) and not song_exists(song, genre, artist2):
                    c.execute('INSERT into songs values ("{id}", "{song}", "{genre}", "{artist}")'.format(id=id1, song=song, genre=genre, artist=artist1))
                    conn.commit()
                    c.execute('INSERT into songs values ("{id}", "{song}", "{genre}", "{artist}")'.format(id=id2, song=song, genre=genre, artist=artist2))
                    conn.commit()
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Song " + song + " by " + artist1 + " and " + artist2 + " has been added succesfully to your database."
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(409)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Song already exists in the database."
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Song could not be added to the database."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return

    def do_PUT(self):
        if self.path.startswith("/?song="):
            path = self.path.split("/?", 1)[1]
            parameters = str(path).split("&")
            song = parameters[0].split("=")[1]
            new_atist = parameters[1].split("=")[1]
            try:
                if song_name_exists(song):
                    print("!!!")
                    c.execute('UPDATE songs SET artist="{}" WHERE song = "{}"'.format(new_atist, song))
                    conn.commit()
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Artist to song " + song + " was changed to " + new_atist
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Song was not changed"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Song could not be changed."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return
        elif self.path.startswith("/?artist="):
            path = self.path.split("/?", 1)[1]
            parameters = str(path).split("&")
            artist = parameters[0].split("=")[1]
            new_genre = parameters[1].split("=")[1]
            try:
                if song_artist_exists(artist):
                    print("!!!")
                    c.execute('UPDATE songs SET genre="{}" WHERE artist = "{}"'.format(new_genre, artist))
                    conn.commit()
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Genre to artist " + artist + " was changed to " + new_genre
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Songs could not be changed."
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Songs were changed."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return

    def do_DELETE(self):
        if self.path.startswith("/?song="):
            song = self.path.split("=")[1]
            try:
                c.execute('SELECT * from songs where song = "{}"'.format(song))
                result = c.fetchall()
                if len(result) == 0:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Song not found."
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    c.execute('DELETE from songs where song = "{}"'.format(song))
                    conn.commit()
                    content = "Song was deleted successfully"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Song could not be returned."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return
        elif self.path.startswith("/?genre="):
            genre = self.path.split("=")[1]
            try:
                c.execute('SELECT * from songs where genre = "{}"'.format(genre))
                result = c.fetchall()
                if len(result) == 0:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Genre not found"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    c.execute('DELETE from songs where genre = "{}"'.format(genre))
                    conn.commit()
                    content = "Songs were deleted successfully"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Songs could not be returned."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return
        elif self.path.startswith("/?artist="):
            artist = self.path.split("=")[1]
            try:
                c.execute('SELECT * from songs where artist = "{}"'.format(artist))
                result = c.fetchall()
                if len(result) == 0:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    content = "Artist not found"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    c.execute('DELETE from songs where artist = "{}"'.format(artist))
                    conn.commit()
                    content = "Songs were deleted successfully"
                    content = convert_message_to_json(content)
                    self.wfile.write(content.encode('utf-8'))
                    return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                content = "Songs could not be returned."
                content = convert_message_to_json(content)
                self.wfile.write(content.encode('utf-8'))
                return


def run(server_class=HTTPServer, handler_class=S, port=PORT_NUMBER):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    httpd.serve_forever()
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    run()
