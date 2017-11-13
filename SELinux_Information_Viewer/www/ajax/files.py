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
from common import ajax, count, path_condition

@route('/ajax/files', apply=[ajax])
def files(cursor, request, response):
  params = request.params
  path = params.get("path","")
  limit = int(params.get("limit","25"))
  offset = int(params.get("offset","0"))
  query = """\
    WITH refs AS (
      SELECT file_id, max(context_id) AS context_id 
      FROM context_file_refs
      GROUP BY file_id
    )
    SELECT files.*, contexts.id AS context_id, contexts.json AS context 
    FROM files 
    LEFT OUTER JOIN refs ON refs.file_id = files.id
    LEFT OUTER JOIN contexts ON refs.context_id = contexts.id
  """
  args = []

  paths, condition = path_condition(path)
  args.extend(paths)
  query += " WHERE {0}".format(condition)
  query += " ORDER BY files.id"

  all_count = count(cursor, query, args)

  query += " LIMIT %s OFFSET %s"
  args.extend([limit, offset])
  cursor.execute(query, args)
  files = []
  for row in cursor:
      id, json, context_id, context = row
      json["id"] = id
      if not context_id is None:
        context["id"] = context_id
         
      json["context"] = context
      files.append(json)

  data = {
    "all": all_count,
    "files": files
  }
  return data


@route('/ajax/file', apply=[ajax])
def file(cursor, request, response):
  params = request.params
  id = params.get("id", "0")
  
  query = """\
    SELECT * FROM files WHERE id = %s
  """
  cursor.execute(query,[id])
  file = None
  for row in cursor:
    id, file = row
    file["id"] = id
  
  if file is None:
    return {
      'msg': 'There is no file.',
      'file': {},
    }

  query = """\
    SELECT contexts.* FROM contexts
    JOIN context_file_refs AS refs ON refs.context_id = contexts.id
    JOIN files ON refs.file_id = files.id AND files.id = %s
    ORDER BY contexts.id DESC
  """
  cursor.execute(query,[id])
  contexts = []
  for row in cursor:
    cid, context = row
    context["id"] = cid
    contexts.append(context)
  
  file["contexts"] = contexts

  domain = file["label"]["domain"]
  if len(contexts) > 0:
    context = contexts[0]
    label = context["label"]
    if not label is None:
      domain = label["domain"]
    else:
      domain = None

  rules = []
  if not domain is None:
    ftype = file["file_type"]
    klass = None
    if ftype == "f":
      klass = "file"
    elif ftype == "d":
      klass = "dir"
    elif ftype == "l":
      klass = "lnk_file"
    elif ftype == "s":
      klass = "socket"
    if not klass is None:
      query = """\
        SELECT id, json FROM rules
        JOIN domain_crews as targets ON json->>'target' = targets.crew AND targets.domain = %s
        WHERE json->>'type' = 'allow' 
        AND json->>'class' in ( %s, 'filesystem')
        ORDER BY json->>'source'
      """
      cursor.execute(query, [domain, klass])
      for row in cursor:
        rid, rule = row
        rule["id"] = rid
        rules.append(rule)
  
  file["rules"] = rules

  data = {
    "file": file    
  }
  return data