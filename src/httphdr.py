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


'''
Source:
http://en.wikipedia.org/wiki/List_of_HTTP_headers
'''


REQUEST_HEADERS = (
'Accept', # Content-Types that are acceptable || <code>Accept: text/plain</code>
'Accept-Charset', # Character sets that are acceptable || <code>Accept-Charset: iso-8859-5</code>
'Accept-Encoding', # Acceptable encodings || <code>Accept-Encoding: compress, gzip</code>
'Accept-Language', # Acceptable languages for response || <code>Accept-Language: da</code> 
'Accept-Ranges', # Allows the server to indicate its acceptance of range requests for a resource || <code> Accept-Ranges: bytes </code>
'Authorization', # Authentication credentials for HTTP authentication || <code>Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==</code>
'Cache-Control', # Used to specify directives that MUST be obeyed by all caching mechanisms along the request/response chain || <code>Cache-Control: no-cache</code>
'Connection', # What type of connection the user-agent would prefer || <code>Connection: close</code>
'Cookie', # an HTTP cookie previously sent by the server with <tt>Set-Cookie</tt> (below) || <code>Cookie: $Version=1; UserId=JohnDoe</code>
'Content-Type', # The [[mime type]] of the body of the request (used with POST and PUT requests) || <code>Content-Type: application/x-www-form-urlencoded</code>
'Date', # The date and time that the message was sent || <code>Date: Tue, 15 Nov 1994 08:12:31 GMT</code>
'Expect', # Indicates that particular server behaviors are required by the client || <code>Expect: 100-continue</code>
'From', # The email address of the user making the request || <code>From: user@email.com</code>
'Host', # The domain name of the server (for [[virtual hosting]]), mandatory since HTTP/1.1 || <code>Host: en.wikipedia.org</code>
'If-Match', # Only perform the action if the client supplied entity matches the same entity on the server. This is mainly for methods like PUT to only update a resource if it has not been modified since the user last updated it. || <code>If-Match: "737060cd8c284d8af7ad3082f209582d"</code>
'If-Modified-Since', # Allows a ''304 Not Modified'' to be returned if content is unchanged || <code>If-Modified-Since: Sat, 29 Oct 1994 19:43:31 GMT</code>
'If-None-Match', # Allows a ''304 Not Modified'' to be returned if content is unchanged, see [[HTTP ETag]] || <code>If-None-Match: "737060cd8c284d8af7ad3082f209582d"</code>
'If-Range', # If the entity is unchanged, send me the part(s) that I am missing; otherwise, send me the entire new entity || <code>If-Range: "737060cd8c284d8af7ad3082f209582d"</code>
'If-Unmodified-Since', # Only send the response if the entity has not been modified since a specific time. || <code>If-Unmodified-Since: Sat, 29 Oct 1994 19:43:31 GMT</code>
'Max-Forwards', # Limit the number of times the message can be forwarded through proxies or gateways. || <code>Max-Forwards: 10</code>
'Pragma', # Implementation-specific headers that may have various effects anywhere along the request-response chain. || <code>Pragma: no-cache</code>
'Proxy-Authorization', # Authorization credentials for connecting to a proxy. || <code>Proxy-Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==</code>
'Range', # Request only part of an entity. || <code>Range: bytes=500-999</code>
'Referer', # This is the address of the previous web page from which a link to the currently requested page was followed. || <code><nowiki>Referer: http://en.wikipedia.org/wiki/Main_Page</nowiki></code>
'TE', # The transfer encodings the user agent is willing to accept: the same values as for the response header Transfer-Encoding can be used, plus the "trailers" value (related to the "[[chunked transfer encoding|chunked]]" transfer method) to notify the server it accepts to receive additional headers (the trailers) after the last, zero-sized, chunk. || <code>TE: trailers, deflate;q=0.5</code>
'Upgrade', # Ask the server to upgrade to another protocol. || <code>Upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11</code>
'User-Agent', # The [[user agent]] string of the user agent || <code>User-Agent: Mozilla/5.0 (Linux; X11)</code>
'Via', # Informs the server of proxies through which the request was sent. || <code>Via: 1.0 fred, 1.1 nowhere.com (Apache/1.1)</code>
'Warn', # A general warning about possible problems with the entity body. || <code>Warn: 199 Miscellaneous warning</code>
)


RESPONSE_HEADERS = (
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

