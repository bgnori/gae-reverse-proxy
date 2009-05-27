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


DEFAULT_STATUS = ('200 OK',)
PROHIBTED = ('Content-Encoding', 
             'Content-Length', 
             'Transfer-Encoding')
HTTP_HEADERS = (
'Accept-Ranges', #What partial content range types this server supports || <code>Accept-Ranges: bytes</code>
'Age', #The age the object has been in a [[proxy server|proxy]] cache in seconds || <code>Age: 12</code>
'Allow', #Valid actions for a specified resource. To be used for a ''405 Method not allowed'' || <code>Allow: GET, HEAD</code>
'Cache-Control', #Tells all caching mechanisms from server to client whether they may cache this object || <code>Cache-Control: no-cache</code>
'Content-Encoding', #The type of encoding used on the data || <code>Content-Encoding: gzip</code>
'Content-Language', #The language the content is in || <code>Content-Language: da</code>
'Content-Length', #The length of the response body in 8-bit bytes|| <code>Content-Length: 348</code>
'Content-Location', #An alternate location for the returned data || <code>Content-Location: /index.htm</code>
'Content-Disposition', #An opportunity to raise a "File Download" dialogue box for a known MIME type || <code>Content-Disposition: attachment; filename=fname.ext</code>
'Content-MD5', #An [[MD5]] sum of the content of the response || <code>Content-MD5: 3167b9c13ad2b6d36946493fc47976c8</code>
'Content-Range', #Where in a full body message this partial message belongs || <code>Content-Range: bytes 21010-47021/47022</code>
'Content-Type', #The [[mime type]] of this content || <code>Content-Type: text/html; charset=utf-8</code>
'Date', #The date and time that the message was sent || <code>Date: Tue, 15 Nov 1994 08:12:31 GMT</code>
'ETag', #An identifier for a specific version of a resource, often a [[Hash function|Message Digest]], see [[HTTP_ETag|ETag]] || <code>ETag: 737060cd8c284d8af7ad3082f209582d</code>
'Expires', #Gives the date/time after which the response is considered stale || <code>Expires: Thu, 01 Dec 1994 16:00:00 GMT</code>
'Last-Modified', #The last modified date for the requested object, in [http://www.ietf.org/rfc/rfc2822.txt RFC 2822 format] || <code>Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT</code>
'Location', #Used in redirection, or when a new resource has been created. || <code>Location: <nowiki>http://www.w3.org/pub/WWW/People.html</nowiki></code>
'Pragma', #Implementation-specific headers that may have various effects anywhere along the request-response chain. || <code>Pragma: no-cache</code>
'Proxy-Authenticate', #Request authentication to access the proxy. || <code>Proxy-Authenticate: Basic</code>
'Retry-After', #If an entity is temporarily unavailable, this instructs the client to try again after a specified period of time. || <code>Retry-After: 120</code>
'Server', #A name for the server || <code>Server: Apache/1.3.27 (Unix)  (Red-Hat/Linux)</code>
'Set-Cookie', #an [[HTTP cookie]] || <code>Set-Cookie: UserID=JohnDoe; Max-Age=3600; Version=1</code>
'Trailer', #The Trailer general field value indicates that the given set of header fields is present in the trailer of a message encoded with [[chunked transfer encoding|chunked transfer-coding]]. || <code>Trailer: Max-Forwards</code>
'Transfer-Encoding', #The form of encoding used to safely transfer the entity to the user. [http://www.iana.org/assignments/http-parameters Currently defined methods] are: [[chunked transfer encoding|chunked]], compress, deflate, gzip, identity. || <code>Transfer-Encoding: [[chunked transfer encoding|chunked]]</code>
'Vary', #Tells downstream proxies how to match future request headers to decide whether the cached response can be used rather than requesting a fresh one from the origin server. || <code>Vary: *</code>
'Via', #Informs the client of proxies through which the response was sent. || <code>Via: 1.0 fred, 1.1 nowhere.com (Apache/1.1)</code>
'Warn', #A general warning about possible problems with the entity body. || <code>Warn: 199 Miscellaneous warning</code>
'WWW-Authenticate', #Indicates the authentication scheme that should be used to access the requested entity. || <code>WWW-Authenticate: Basic</code>
)

DEFAULT_HEADER_VALUES = {
    'Content-Type':['text/plain'],
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
  print 'serving at %s, %i'%(sys.argv[1], int(sys.argv[2]))
  httpd = make_server(sys.argv[1], int(sys.argv[2]), stubd)
  httpd.serve_forever()

