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

@route('/ajax/processes', apply=[ajax])
def processes(cursor, request, response):
  params = request.params
  limit = int(params.get("limit","25"))
  offset = int(params.get("offset","0"))

  query = """\
    SELECT id, json FROM processes
  """

  name = params.get("name","")
  domain = params.get("domain","")
  
  args = []
  conditions = []
  if name != "":
    conditions.append("""
      json->>'name' = %s
    """) 
    args.append(name)
  
  if domain != "":
    conditions.append("""
      EXISTS (
        SELECT * FROM domain_crews 
        WHERE domain = %s
        AND json->'label'->>'domain' = crew
      )
    """) 
    args.append(domain)

  condition = " AND ".join(conditions) 
  if len(condition) > 0:
    query += " WHERE " + condition 

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

@route('/ajax/processes/info', apply=[ajax])
def processes_info(cursor, request, response):

  query = """\
    SELECT JSONB_BUILD_OBJECT(
      'names', ( SELECT JSONB_AGG(item) FROM
        (SELECT DISTINCT json->>'name' AS item FROM processes ORDER BY item) AS tmp
      )
     ,'domains', ( SELECT JSONB_AGG(item) FROM
        (SELECT DISTINCT json->'label'->>'domain' AS item FROM processes ORDER BY item) AS tmp
      )
    )
  """
  args = []
  cursor.execute(query, args)
  info, = cursor.fetchone()

  data = {
    "info": info,
  }
  return data
