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

import time
from urllib import urlencode
import unittest
#from subprocess import call

from webtest import TestApp

from google.appengine.ext import webapp
from google.appengine.api import memcache
from util import Epoch_to_rfc1123
from proxy import HandlerFactory

#FIXME 
#  this test code expects that http://image.backgammonbase.com as the orogin server.


class HandlerTest(unittest.TestCase):
  def setUp(self):
    self.app = TestApp(
                   webapp.WSGIApplication([('.*', HandlerFactory(
                                                    'http',
                                                    'localhost:8001',
                                                    '')
                   
                                                  )],
                                       debug=True)
                   )

  def tearDown(self):
    memcache.flush_all()
    del self.app

  def test_status200_vanilla(self):
    response = self.app.get(
        '/',
        headers={
            'X-Testing': urlencode({
                 'status': '200 OK',
                }),
        },
        )
    print response.status
    print response.headers
    assert response.status.startswith('200')

  def test_status200_Expire(self):
    expires = Epoch_to_rfc1123(time.time() + 1000)
    response = self.app.get(
        '/',
        headers={
            'X-Testing': urlencode({
                 'status': '200 OK',
                 'Expires':expires,
                }),
        },
        status=200)
    print response.status
    print response.headers
    assert response.status.startswith('200')

  def test_contenttype_jpeg(self):
    response = self.app.get(
        '/',
        headers={
            'X-Testing': urlencode({
                 'status': '200 OK',
                 'Content-Type': 'image/jpeg',
                }),
        },
        )
    print response.status
    print response.headers
    assert response.headers['Content-Type'] == 'image/jpeg'
    assert response.status.startswith('200')

  def test_etagless_client(self):
    expires = Epoch_to_rfc1123(time.time() + 1000)
    response = self.app.get(
        '/',
        headers={
            'X-Testing': urlencode({
                'status': '200 OK',
                'Expires':expires,
                'ETag': '1'
                }),
        },
        status=200)
    print 'first response (populated memcache)'
    print response.status
    print response.headers
    assert response.status.startswith('200')

    response = self.app.get(
        '/',
        headers={
            'X-Testing': urlencode({
                'status': '200 OK',
                'Expires':expires,
                'ETag': '2'
                }),
        },
        status=200)
    print 'second response'
    print response.status
    print response.headers
    assert response.status.startswith('200')

  def test_etag_match(self):
    expires = Epoch_to_rfc1123(time.time() + 1000)
    response = self.app.get(
        '/',
        headers={
            'X-Testing': urlencode({
                'status': '200 OK',
                'Expires':expires,
                'ETag': '1'
                }),
        },
        )
    print 'first response (populated memcache)'
    print response.status
    print response.headers
    print response.headers['etag']
    assert response.status.startswith('200')

    response = self.app.get(
        '/',
        headers={
            'If-None-Match': response.headers['etag'],
            'X-Testing': urlencode({
                'status': '304 OK',
                'Expires':expires,
                'ETag': '1'
                }),
        },
        )
    print 'second response'
    print response.status
    print response.headers
    assert response.status.startswith('304')

  def test_etag_mismatch(self):
    expires = Epoch_to_rfc1123(time.time() + 1000)
    response = self.app.get(
        '/',
        headers={
            'X-Testing': urlencode({
                'status': '200 OK',
                'Expires':expires,
                'ETag': '1'
                }),
        },
        status=200)
    print 'first response (populated memcache)'
    print response.status
    print response.headers
    print response.headers['etag']
    assert response.status.startswith('200')

    response = self.app.get(
        '/',
        headers={
            'If-None-Match': 'some_thing_invalid',
            'X-Testing': urlencode({
                'status': '200 OK',
                'Expires':expires,
                'ETag': '1'
                }),
        },
        )
    print 'second response'
    print response.status
    print response.headers
    assert response.status.startswith('200')

