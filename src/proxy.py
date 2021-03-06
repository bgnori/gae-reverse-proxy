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

import urlparse
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from config import NETLOC, HOST, SCHEME
from epoch  import rfc1123_to_Epoch

'''
  This list came from http://code.google.com/intl/ja/appengine/docs/webapp/responseclass.html#Disallowed_HTTP_Response_Headers
'''
PROHIBTED_BY_GAE = ('Content-Encoding', 
                    'Content-Length', 
                    'Date',
                    'Server',
                    'Transfer-Encoding')

'''
  statuses of Resopnse cannot have entity  
'''
PROHIBTED_IN_ENTITYLESS = ('Content-Type', )
ENTITYLESS_STATUS = (204, 205, 304)


def HandlerFactory(orig_scheme, orgi_netloc, orig_host):
  class ReverseProxyHandler(webapp.RequestHandler):
    def relay_response(self, src, status):
      assert status
      self.response.set_status(status)
      for key in src.headers:
        self.response.headers[key] = src.headers[key]
  
      if status in ENTITYLESS_STATUS:
        for key in PROHIBTED_IN_ENTITYLESS + PROHIBTED_BY_GAE:
          del self.response.headers[key]
      else:
        self.response.out.write(src.content)
        for key in PROHIBTED_BY_GAE:
          del self.response.headers[key]
  
    def set_cache(self, url, response):
      try:
        expires = rfc1123_to_Epoch(response.headers['expires'])
        memcache.set(url, response, time=expires)
      except (KeyError, ValueError):
        memcache.set(url, response)
  
    def get_cache(self, url):
      return memcache.get(url)
  
    def get(self):
      u = self.request.url
      scheme, netloc, path, query, fragment = urlparse.urlsplit(u)
      t = urlparse.urlunsplit((orig_scheme, orgi_netloc, path, query, fragment))
      if_none_match = self.request.headers.get('If-None-Match', None)
      cached = self.get_cache(u)
      if cached is None:
        r = urlfetch.fetch(t, 
              headers={
                'Host': orig_host,
                'X-Testing': self.request.headers.get('X-Testing', None)
              },
              )
        assert r.status_code == 200
        self.set_cache(u, r)
        self.relay_response(r, 200)
        return
  
      elif cached is not None and if_none_match is None:
        if 'etag' in cached.headers:
          r = urlfetch.fetch(t, 
              headers={
                'Host': orig_host,
                'If-None-Match': cached.headers['etag'],
                'X-Testing': self.request.headers.get('X-Testing', None)
              }
              )
        else:
          r = urlfetch.fetch(t, 
              headers={
                'Host': orig_host,
                'X-Testing': self.request.headers.get('X-Testing', None)
              }
              )
        if r.status_code == 200:
          self.set_cache(u, r)
          self.relay_response(r, 200)
          return
        elif r.status_code == 304:
          self.relay_response(cached, status=200)
          return
        else:
          assert False
  
      elif (if_none_match and
            (cached.headers['etag'] == if_none_match)):
        r = urlfetch.fetch(t, 
            headers={
  #            'If-Modified-Since': cached.headers['date'],
              'If-None-Match': cached.headers['etag'],
              'Host': orig_host,
              'X-Testing': self.request.headers.get('X-Testing', None)
            }
            )
        if r.status_code == 200:
          self.set_cache(u, r)
          self.relay_response(r, 200)
          return
        elif r.status_code == 304:
          self.relay_response(r, status=304)
          return
        else:
          assert False
      elif (if_none_match and 
            (cached.headers['etag'] != if_none_match)):
        r = urlfetch.fetch(t, 
              headers={
                'Host': orig_host,
                'X-Testing': self.request.headers.get('X-Testing', None)
              }
              )
        assert r.status_code == 200
        self.set_cache(u, r)
        self.relay_response(r, 200)
        return
      else:
        pass
      assert False
  return ReverseProxyHandler


