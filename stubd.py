

from wsgiref.simple_server import make_server
from wsgiref.simple_server import demo_app
from wsgiref.handlers import SimpleHandler

class etagHandler(SimpleHandler):
  pass
class pngHandler(SimpleHandler):
  pass
class jpegHandler(SimpleHandler):
  pass

#application = webapp.WSGIApplication([('/etag', etagHandler),
#                                      ('/png', pngHandler),
#                                      ('/jpeg', jpegHandler)],
#                                         )
#httpd = make_server("localhost", 8001, application)
httpd = make_server("", 8001, demo_app)

if __name__ == "__main__":
  print "starting ..."
  httpd.serve_forever()

