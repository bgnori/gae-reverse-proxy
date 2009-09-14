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

from lib.epoch import rfc1123_to_Epoch 
from lib.epoch import Epoch_to_rfc1123 

def test_rfc1123_to_Epoch_good():
  try:
    t = rfc1123_to_Epoch('Wed, 22 Oct 2008 10:52:40 GMT')
    assert True
    assert isinstance(t, (int, float))
  except:
    assert False

def test_rfc1123_to_Epoch_bad_TZ():
  try:
    t = rfc1123_to_Epoch('Wed, 22 Oct 2008 10:52:40 +0900')
    assert False
  except ValueError:
    assert True

def test_rfc1123_to_Epoch_bad():
  try:
    t = rfc1123_to_Epoch('10:52:40 GMT')
    assert False
  except ValueError:
    assert True

def test_Epoch_to_rfc1123():
  given = 'Wed, 22 Oct 2008 10:52:40 GMT'
  t = rfc1123_to_Epoch(given)
  print t
  s = Epoch_to_rfc1123(t)
  assert isinstance(s, (str))
  print repr(s)
  print repr(given)
  assert s == given

