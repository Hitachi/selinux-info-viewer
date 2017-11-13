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
from common import ajax, count, like_condition

@route('/ajax/bools', apply=[ajax])
def bools(cursor, request, response):
  params = request.params
  keyword = params.get("query","")
  limit = int(params.get("limit","25"))
  offset = int(params.get("offset","0"))

  query = """\
    SELECT id, json FROM bools
  """

  args = []

  keyword = keyword.strip()
  if keyword != "":
    keywords, condition = like_condition(keyword, 'json::TEXT')
    args.extend(keywords)
    query += " WHERE {0}".format(condition)
  query += " ORDER BY id"

  all_count = count(cursor,query, args)

  query += " LIMIT %s OFFSET %s"
  args.extend([limit, offset])
  cursor.execute(query, args)
  items = []
  for row in cursor:
    id, json = row
    json["id"] = id
    items.append(json)

  data = {
    "all": all_count,
    "items": items,
  }
  return data
  

@route('/ajax/bools/rules', apply=[ajax])
def bool_rules(cursor, request, response):
  params = request.params
  name = params.get("name")

  query = """\
    SELECT * FROM rules WHERE json @> JSONB_BUILD_OBJECT(
      'boolean', ARRAY[ARRAY[%s]]
    ) ORDER BY id
  """
  args = [name]
  cursor.execute(query, args)
  items = []

  for row in cursor:
    id, json = row
    json["id"] = id
    items.append(json)

  data = {
    "items": items,
  }
  return data