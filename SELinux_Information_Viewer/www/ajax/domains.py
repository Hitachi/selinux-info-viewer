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

@route('/ajax/domains', apply=[ajax])
def domains(cursor, request, response):

  query = """\
    SELECT DISTINCT * FROM (
      SELECT json->>'name' AS name FROM types
      UNION
      SELECT json->>'attribute' as name FROM attributes
      UNION
      SELECT json->>'source' as name FROM rules
    ) AS domains ORDER BY name
  """
  
  cursor.execute(query)

  domains = []
  for row in cursor:
    name, = row
    domains.append(name)

  data = {
    "domains": domains,
  }
  return data