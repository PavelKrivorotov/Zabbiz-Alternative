import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from . import settings
from . import database
from . import sql


class HttpServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Instance')
        self.end_headers()

    def do_GET(self):
        if self.path == settings.PATH_TO_GET_PREVIOUS_3_HOURS_JVM_MEMORY_DATA:
            try:
                instance = self.headers.get('Instance', 'None-Instance')
                
                data = sql.get_jvm_memory_objects(instance)
                output = {
                    'labels': [item[1] for item in data],
                    'values': [item[0] for item in data]
                }

                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()

                self.wfile.write(bytes(json.dumps(output), 'utf-8'))

            except Exception as e:
                self.send_response(400)
                self.wfile.write(bytes(json.dumps({"Bad request": f"{e}"}), 'utf-8'))

    def do_POST(self):
        if self.path == settings.PATH_TO_SEND_JVM_MEMORY_DATA:
            try:
                content_len = int(self.headers.get('Content-Length'))
                raw = self.rfile.read(content_len)

                sql.create_jvm_memory_object(raw)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"Insertion": f"{content_len}"}), 'utf-8'))

            except Exception as e:
                self.send_response(400)
                self.wfile.write(bytes(json.dumps({"Insertion": f"{e}"}), 'utf-8'))


def start_up():
    httpd = HTTPServer((settings.LISTEN_HOST, settings.LISTEN_PORT), HttpServer)
    database.init_db()

    try:
        print(
            '\nThe server is runing on {} and listen {} port:\n'.format(
                settings.LISTEN_HOST,
                settings.LISTEN_PORT
            )
        )
        httpd.serve_forever()
    except Exception as e:
        raise ValueError('Sturt Up error!', e)
    finally:
        httpd.shutdown()
        database.close_db()
