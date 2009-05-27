

import cgi


from wsgiref.simple_server import make_server
from wsgiref.simple_server import demo_app
from wsgiref.handlers import SimpleHandler
from StringIO import StringIO


DEFAULT_STATUS = ('200 OK',)
HTTP_HEADERS = (
    'Content-Type',
    'Expires',
    )

DEFAULT_HEADER_VALUES = {
    'Content-Type':['text/plain'],
    'Expires':['0'],
    }

def stubd(environ, start_response):
    stdout = StringIO()
    h = environ.items(); h.sort()
    for k,v in h:
        print >>stdout, k,'=',`v`
   
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    query = environ["QUERY_STRING"]
    d = cgi.parse_qs(query)

    status = d.get('status', DEFAULT_STATUS)[0] #FIXME

    headers = [] 
    for h in HTTP_HEADERS:
      v = d.get(h, None)
      if v is None:
        v = DEFAULT_HEADER_VALUES.get(h)
      if v is None:
        continue
      headers.append((h, v[0]))#FIXME

    start_response(status, headers)
    return [stdout.getvalue()]
   
httpd = make_server("", 8001, stubd)

if __name__ == "__main__":
  print "self testing..."
  from urllib import urlopen
  #httpd.serve_forever()
  h = urlopen("http://localhost:8001/")
  httpd.handle_request()
  h.read()

