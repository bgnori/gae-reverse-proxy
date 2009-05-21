#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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

import sys
import urlparse
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import memcache

cache_related = ('if_match', 'if_modified_since', 'if_none_match', 'if_range', 'if_unmodified_since')
PROHIBTED = ('Content-Length', )
PROHIBTED_IN_ENTITYLESS = PROHIBTED + ('Content-Type', )
ENTITYLESS_STATUS = (204, 205, 304)

#NETLOC = 'image.backgammonbase.com'
NETLOC = '192.168.2.64'
HOST = 'image.backgammonbase.com'
SCHEME = 'http'


class ReverseProxyHandler(webapp.RequestHandler):
  def relay_response(self, src, status):
    assert status
    self.response.set_status(status)
    for key in src.headers:
      self.response.headers[key] = src.headers[key]

    if status in ENTITYLESS_STATUS:
      for key in PROHIBTED_IN_ENTITYLESS:
        del self.response.headers[key]
    else:
      self.response.out.write(src.content)
      for key in PROHIBTED:
        del self.response.headers[key]

  def get(self):
    u = self.request.url
    scheme, netloc, path, query, fragment = urlparse.urlsplit(u)
    t = urlparse.urlunsplit((SCHEME, NETLOC, path, query, fragment))
    if_none_match = self.request.headers.get('If-None-Match', None)
    cached = memcache.get(u)
    if cached is None:
      r = urlfetch.fetch(t, 
            headers={'host': HOST}
            )
      assert r.status_code == 200
      memcache.set(u, r)
      self.relay_response(r, 200)
      return
    elif (if_none_match and
          (cached.headers['etag'] == if_none_match)):
      r = urlfetch.fetch(t, 
          headers={
#            'If-Modified-Since': cached.headers['date'],
            'If-None-Match': cached.headers['etag'],
            'host': HOST
          }
          )
      if r.status_code == 200:
        memcache.set(u, r)
        self.relay_response(r, 200)
        return
      elif r.status_code == 304:
        print 'got 304 from source'
        if if_none_match is not None:
          print 'got matching etag from client'
          self.relay_response(r, status=304)
        else:
          print 'got no etag from client'
          self.relay_response(cached, status=200)
        return
      else:
        assert False
    elif (if_none_match and 
          (cached.headers['etag'] != if_none_match)):
      r = urlfetch.fetch(t, 
            headers={'host': HOST}
            )
      assert r.status_code == 200
      memcache.set(u, r)
      self.relay_response(r, 200)
      return
    else:
      pass
    assert False


def main():
  application = webapp.WSGIApplication([('.*', ReverseProxyHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()

