#!/usr/bin/env python
#
# Copyright:
#  Noriyuki Hosaka bgnori@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from StringIO import StringIO
import cgi

from wsgiref.simple_server import make_server
from wsgiref.simple_server import demo_app
from wsgiref.handlers import SimpleHandler

from lib.httphdr import RESPONSE_HEADERS

DEFAULT_STATUS = ('200 OK',)
PROHIBTED = ('Content-Encoding', 
             'Content-Length', 
             'Transfer-Encoding')

DEFAULT_HEADER_VALUES = {
    'Content-Type':['text/plain'],
    }

def stubd(environ, start_response):
    stdout = StringIO()
    h = environ.items(); h.sort()
    for k,v in h:
        print >>stdout, k,'=',`v`
   
    method = environ["REQUEST_METHOD"]
    d = cgi.parse_qs(environ['HTTP_X_TESTING'])

    status = d.get('status', DEFAULT_STATUS)[0] #FIXME

    headers = [] 
    for h in RESPONSE_HEADERS:
      if h in PROHIBTED:
        continue
      v = d.get(h, None)
      if v is None:
        v = DEFAULT_HEADER_VALUES.get(h)
      if v is None:
        continue
      headers.append((h, v[0]))#FIXME

    start_response(status, headers)
    return [stdout.getvalue()]
   
if __name__ == "__main__":
  import sys
  import os
  import re
  from subprocess import call
  from tempfile import TemporaryFile

  PIDFILE = 'stubd.pid'

  try:
    f = open(PIDFILE, 'r')
  except:
    f = None
    pass
  if f:
    r = TemporaryFile() 
    call(['ps', 'e'], stdout=r)
    r.seek(0)
    x = r.read()
    y = f.read()
    print x
    print 'pid in pid file:', y
    mo = re.search(' *%s'%y, x)
    if mo is None:
      f.close()
      #r.close()
      print 'found stale pid file. removing.'
      os.remove(PIDFILE)

    else:
      #alive
      print 'already running'
      f.close()
      #r.close()
      sys.exit()

  f = open(PIDFILE, 'w')
  f.write('%i'%(os.getpid(),))
  f.close()

  print 'serving at %s, %i'%(sys.argv[1], int(sys.argv[2]))
  httpd = make_server(sys.argv[1], int(sys.argv[2]), stubd)
  try:
    httpd.serve_forever()
  finally:
    os.remove(PIDFILE)

