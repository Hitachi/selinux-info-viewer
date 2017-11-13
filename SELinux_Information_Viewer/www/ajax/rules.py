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

def rule_condition(params):
  type = params.get("type","")
  source = params.get("source","")
  target = params.get("target","")
  klass = params.get("class","")
  
  args = []
  conditions = []
  if type != "":
    conditions.append("""
      json->>'type' = %s
    """) 
    args.append(type)
  
  if source != "":
    conditions.append("""
      EXISTS (
        SELECT * FROM domain_crews 
        WHERE domain = %s
        AND json->>'source' = crew
      )
    """) 
    args.append(source)

  if target != "":
    conditions.append("""
      EXISTS (
        SELECT * FROM domain_crews 
        WHERE domain = %s
        AND json->>'target' = crew
      )
    """) 
    args.append(target)

  if klass != "":
    conditions.append("""
      json->>'class' = %s
    """) 
    args.append(klass)

  condition = " AND ".join(conditions) 
  return (args, condition)



@route('/ajax/rules', apply=[ajax])
def rules(cursor, request, response):
  params = request.params
  limit = int(params.get("limit","25"))
  offset = int(params.get("offset","0"))

  query = """\
    SELECT id, json FROM rules
  """

  args, condition = rule_condition(params)
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

@route('/ajax/rules/info', apply=[ajax])
def rule_info(cursor, request, response):

  query = """\
    SELECT JSONB_BUILD_OBJECT(
      'sources', ( SELECT JSONB_AGG(item) FROM
        (SELECT DISTINCT json->>'source' AS item FROM rules ORDER BY item) AS tmp
      )
     ,'targets', ( SELECT JSONB_AGG(item) FROM
        (SELECT DISTINCT json->>'target' AS item FROM rules ORDER BY item) AS tmp
      )
     ,'types', ( SELECT JSONB_AGG(item) FROM
        (SELECT DISTINCT json->>'type' AS item FROM rules ORDER BY item) AS tmp
      )
     ,'classes', ( SELECT JSONB_AGG(item) FROM
        (SELECT DISTINCT json->>'class' AS item FROM rules ORDER BY item) AS tmp
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