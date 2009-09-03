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
from datetime import datetime

RFC1123_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

def rfc1123_to_Epoch(s):
  return time.mktime(time.strptime(s, RFC1123_FORMAT))

def Epoch_to_rfc1123(t):
  dt = datetime.fromtimestamp(t)
  return time.strftime(RFC1123_FORMAT, dt.utctimetuple())

