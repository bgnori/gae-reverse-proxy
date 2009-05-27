

from wsgiref.simple_server import make_server
from wsgiref.simple_server import demo_app
from wsgiref.handlers import SimpleHandler
from StringIO import StringIO

def application(environ, start_response):
    stdout = StringIO()
    h = environ.items(); h.sort()
    for k,v in h:
        print >>stdout, k,'=',`v`

   
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    query = environ["QUERY_STRING"]

    start_response("200 OK", [('Content-Type','text/plain')])
    return [stdout.getvalue()]
   
httpd = make_server("", 8001, application)

if __name__ == "__main__":
  print "self testing..."
  from urllib import urlopen
  #httpd.serve_forever()
  h = urlopen("http://localhost:8001/")
  httpd.handle_request()
  h.read()

