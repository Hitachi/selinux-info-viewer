# coding: utf-8

# Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#    https://opensource.org/licenses/MIT
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OF ANY KIND.

from bottle  import route
from common import ajax


@route('/ajax/info', apply=[ajax])
def info(cursor, request, response):
  query = """\
    SELECT json FROM info
  """
  cursor.execute(query)
  info = {}
  for row in cursor:
      info, = row

  data = {
    "info": info    
  }
  return data