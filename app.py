import cherrypy
import os
import sys
from os.path import abspath
import requests 
import json

# ----------ルーティング
class home:
        @cherrypy.expose
        def home(self):
                return open("input.html")


class upload_blog:
        @cherrypy.expose
        @cherrypy.tools.allow(methods=['POST'])
        # def index(self, var=None, **params):
        def upload_blog(self, myFile):
            upload_blog_path = os.path.normpath('./download')
            upload_blog_file = os.path.join(upload_blog_path, myFile.filename)
            size = 0
            with open(upload_blog_file, 'wb') as out:
                while True:
                    data = myFile.file.read(8192)
                    if not data:
                        break
                    out.write(data)
            
            file = myFile.file.read()

            out = """<html>
            <body>
                myFile length: %s<br />
                myFile filename: %s<br />
                myFile mime-type: %s
            </body>
            </html>"""

            # Although this just counts the file length, it demonstrates
            # how to read large files in chunks instead of all at once.
            # CherryPy reads the uploaded file into a temporary file;
            # myFile.file.read reads from that.
            size = 0
            while True:
                data = myFile.file.read(8192)
                if not data:
                    break
                size += len(data)





            #return out % (size, myFile.filename, myFile.content_type)
            return json.dumps({'file_data': (myFile.filename)})





# ----------ルーティング実行
d = cherrypy.dispatch.RoutesDispatcher()
d.connect('home', '/', controller=home(), action='home')
d.connect('upload_blog', '/upload_blog', controller=upload_blog(), action='upload_blog')





# ----------設定
CP_CONF = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('./'),
            'request.dispatch': d
            }
        }

# ----------おまじない
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8082})
    cherrypy.quickstart(home(), '/', CP_CONF)




