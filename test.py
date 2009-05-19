import unittest

from webtest import TestApp

from google.appengine.ext import webapp
from main import ReverseProxyHandler

#class CCTest(unittest.TestCase):


app = TestApp(webapp.WSGIApplication([('.*', ReverseProxyHandler)],
                                       debug=True)
                                       )
#class HandlerTest(unittest.TestCase):
#  pass

def test_contenttype():
  response = app.get('/image'
                     '?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA'
                     '&height=300'
                     '&width=400'
                     '&css=minimal'
                     '&format=png')
  assert response.headers['Content-Type'] == 'image/png'


