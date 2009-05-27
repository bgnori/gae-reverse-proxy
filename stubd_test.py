


import unittest

from webtest import TestApp
from stubd import stubd

class StubdTest(unittest.TestCase):
  def setUp(self):
    self.app = TestApp(stubd)

  def tearDown(self):
    pass

  def test_default(self):
    response = self.app.get('/', status=200)

    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/plain'

  def test_status201(self):
    response = self.app.get('/?status=201 OK', status=201)

    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/plain'

  def test_status201_contenttype(self):
    response = self.app.get('/?status=201 OK&Content-Type=text/css', status=201)

    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/css'

  def test_contenttype(self):
    response = self.app.get("/?Content-Type=text/html", status=200)
    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/html'



