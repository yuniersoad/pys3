import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import ssl

from utils import *

dirname = os.path.dirname(__file__)
ROOT_DIR = os.path.join(dirname, '../test_root')
TEMPLATE_PATH = os.path.join(dirname, 'templates')

define("sslcert", default=None, help="Path to ssl certificate")
define("sslkey", default=None, help="Path to ssl key")
define("root", default=ROOT_DIR, help="Path to root folder") 

class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        print (self.request)

    def get(self):
        self.set_header('Content-Type', 'application/XML')
        self.render("bucket_list.xml", buckets=get_buckets(options.root))

class BucketHandler(tornado.web.RequestHandler):
    def prepare(self):
        print (self.request)

    def get(self, bucket):
        print (bucket)
        prefix = self.request.query_arguments["prefix"][0].decode("utf-8")
        print (prefix)
        self.set_header('Content-Type', 'application/XML')
        self.render("object_list.xml", bucket = bucket,objects=get_objects(options.root, bucket, prefix))

    def delete(self, bucket):
        delete_bucket(options.root, bucket)
        self.set_status(204)

class ObjectsHandler(tornado.web.RequestHandler):
    def prepare(self):
        print (self.request)

    def get(self, bucket, path):
        full_path = os.path.join(options.root, bucket, path)
        with open(full_path, 'rb') as f:
            while 1:
                data = f.read(16384)
                if not data: break
                self.write(data)
        self.finish()

    def delete(self, bucket, path):
        delete_object(options.root, bucket, path)
        self.set_status(204)

if __name__ == '__main__':
     options.parse_command_line()

     with_ssl = not(options.sslcert is None) and not(options.sslkey is None)
     ssl_ctx = None
     if with_ssl:
	     ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	     ssl_ctx.load_cert_chain(options.sslcert, options.sslkey)

     application = tornado.web.Application(
      [
       (r'/', MainHandler), 
       (r'/(.*)/', BucketHandler),
       (r'/(.*)/(.*)', ObjectsHandler),
      ],
      template_path=TEMPLATE_PATH)

     http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_ctx)
     http_server.listen(443 if with_ssl else 8080)
     tornado.ioloop.IOLoop.instance().start()

