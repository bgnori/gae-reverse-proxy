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

from urllib import urlencode
import unittest

from webtest import TestApp
import stubd

class StubdTest(unittest.TestCase):
  def setUp(self):
    self.app = TestApp(stubd.stubd)

  def tearDown(self):
    pass

  def test_default(self):
    response = self.app.get('/', status=200)

    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/plain'

  def test_status201(self):
    response = self.app.get(
        '/?'+ urlencode({
                'status': '201 OK',
              }),
        status=201)

    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/plain'

  def test_status201_contenttype(self):
    response = self.app.get(
        '/?'+ urlencode({
                'status': '201 OK',
                'Content-Type':'text/css', 
              }),
        status=201)
    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/css'

  def test_contenttype(self):
    response = self.app.get(
        '/?'+ urlencode({
                'Content-Type':'text/html', 
              }),
        status=200)
    print response.status
    print response.headers
    print response.body
    assert response.headers['Content-Type'] == 'text/html'

  def test_headerx(self):
    for h in stubd.HTTP_HEADERS:
      if h in stubd.PROHIBTED:
        continue
      response = self.app.get("/?%s=hoge"%(h,), status=200)
      print response.status
      print response.headers
      print response.body
      assert response.headers[h] == 'hoge'


