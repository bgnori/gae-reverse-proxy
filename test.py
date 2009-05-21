import unittest

from webtest import TestApp

from google.appengine.ext import webapp
from google.appengine.api import memcache
from main import ReverseProxyHandler

#class CCTest(unittest.TestCase):


class HandlerTest(unittest.TestCase):
  def setUp(self):
    self.app = TestApp(
                   webapp.WSGIApplication([('.*', ReverseProxyHandler)],
                                       debug=True)
                   )
  def tearDown(self):
    memcache.flush_all()
    del self.app

  def test_contenttype_png(self):
    response = self.app.get(('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=png'),
                     status=200
                     )
    assert response.headers['Content-Type'] == 'image/png'

  def test_contenttype_jpeg(self):
    response = self.app.get(('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=jpeg'),
                     status=200
                     )
    assert response.headers['Content-Type'] == 'image/jpeg'

  def test_status200(self):
    response = self.app.get(('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=png'),
                     status=200
                     )
    if response.headers['Content-Type'].startswith('text/html'):
      print response
      #print dir(response)
      print len(response.body)
    print response.status
    print response.headers
    assert response.headers['Content-Type'] == 'image/png'

  def test_etag_match(self):
    response = self.app.get(('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=png'),
                     status=200
                      )
    print 'first response (populated memcache)'
    print response.status
    print response.headers
    print response.headers['etag']
    assert response.headers['Content-Type'] == 'image/png'
    response = self.app.get(('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=png'),
                     headers={
                        'If-None-Match': response.headers['etag'],
                          },
                     )
    print 'second response'
    print response.status
    print response.headers
    assert response.status.startswith('304')

  def test_etag_mismatch(self):
    response = self.app.get(('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=png'),
                     status=200
                      )
    print 'first response (populated memcache)'
    print response.status
    print response.headers
    assert response.headers['Content-Type'] == 'image/png'
    response = self.app.get(('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=png'),
                     headers={
                        'If-None-Match': 'some_thing_invalid'
                          },
                     )
    print 'second response'
    print response.status
    print response.headers
    assert response.status.startswith('200')

