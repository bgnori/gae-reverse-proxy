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




import wsgiref.handlers



from google.appengine.ext import webapp
from google.appengine.api import urlfetch

cache_related = ('if_match', 'if_modified_since', 'if_none_match', 'if_range', 'if_unmodified_since')

class MainHandler(webapp.RequestHandler):

  def get(self):
    response = urlfetch.fetch('http://image.backgammonbase.com/image?gnubgid=4HPwATDgc%2FABMA%3AMAAAAAAAAAAA&height=300&width=400&css=minimal&format=png')
    self.response.headers['Content-Type'] = response.headers['Content-Type']
    self.response.out.write(response.content)


def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
