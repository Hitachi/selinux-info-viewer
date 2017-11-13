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
from common import ajax, count, like_condition, like_escape

@route('/ajax/filecontexts/accessable', apply=[ajax])
def filecontexts_accesable(cursor, request, response):
  params = request.params
  source = params.get("source", "")
  
  keyword = params.get("filter", "")

  offset = int(params.get("offset", "0"))
  limit = int(params.get("limit", "25"))
  
  args = [source]

  keywords, keyword_condition = like_condition(keyword, 'contexts.json::TEXT')
  args.extend(keywords)

  query = """\
    SELECT 
      DISTINCT(contexts.id), 
      contexts.json,
      (EXISTS (SELECT * FROM context_file_refs AS refs WHERE refs.context_id = contexts.id)) AS has_files
    FROM contexts
    JOIN rule_context_refs AS refs ON refs.context_id = contexts.id
    JOIN rules ON rules.id = refs.rule_id AND rules.json->>'type'='allow'
    JOIN domain_crews AS sources ON sources.crew = rules.json->>'source' AND sources.domain = %s
    WHERE {0}
    ORDER BY contexts.id
  """.format(keyword_condition)
 
  all_count = count(cursor, query, args)
  query = query + " LIMIT %s OFFSET %s "
  args.extend([limit, offset])
  
  items = []
  cursor.execute(query, args)
  for row in cursor:
    id, json, has_files = row
    json["id"] = id
    json["has_files"] = has_files
    items.append(json)

  data = {
    "all": all_count,
    "items": items,
  }
  return data


@route('/ajax/filecontexts/files', apply=[ajax])
def files(cursor, request, response):
  params = request.params
  fcontext_id = int(params.get("fcontext", "-1"))
  path = params.get("path","")
  keyword = params.get("keyword", "")
  limit = int(params.get("limit","25"))
  offset = int(params.get("offset","0"))

  path = "{0}%".format(like_escape(path))

  query = """\
    SELECT files.* FROM files 
    JOIN context_file_refs AS refs ON refs.file_id = files.id AND refs.context_id = %s
    WHERE files.json->>'path' LIKE %s
  """
  args = [fcontext_id, path]

  keywords, condition = like_condition(keyword, 'json::TEXT')
  args.extend(keywords)
  query += " AND {0}".format(condition)
  query += " ORDER BY files.id"
  all_count = count(cursor, query, args)

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
    "items": items
  }
  return data


#@route('/ajax/contexts')
def contexts():
  from bottle import response, request
  params = request.params
  domain = params.get("domain", "")
  
  path = params.get("path", "")

  offset = int(params.get("offset", "0"))
  limit = int(params.get("limit", "25"))
  ok = params.get("ok", "true")
  ng = params.get("ng", "false")
  
  connection = psycopg2.connect(host="localhost", port=20000, dbname="selinux")
  cursor = connection.cursor()

  
  count = -1
  items = []
  args = [domain]

  query = """\
    WITH 
    source_crews AS (
      SELECT domain_crews.crew as name FROM domain_crews WHERE domain_crews.domain = %s
    )
    ,related_target AS (
      SELECT DISTINCT json->>'class' AS class, json->>'target' AS domain FROM rules
      JOIN source_crews ON rules.json->>'source' = source_crews.name
      WHERE rules.json->>'type' = 'allow'
    )
    ,target_crews AS (
      SELECT DISTINCT domain_crews.crew as name, related_target.class AS class FROM domain_crews 
      JOIN related_target ON related_target.domain = domain_crews.domain 
    )
    SELECT contexts.id AS context_id
          ,contexts.json->>'pattern' AS context_pattern
          ,contexts.json->'label'->>'domain' AS context_domain
          ,files.id AS file_id
          ,files.json->>'path' AS file_path
          ,files.json->'label'->>'domain' AS file_domain
    FROM files
    JOIN context_file_refs AS cfr ON files.id = cfr.file_id 
    JOIN contexts ON cfr.context_id = contexts.id
    JOIN target_crews AS targets ON contexts.json->'label'->>'domain' = targets.name 
    AND ( 
             (contexts.json->>'type' = 'all files' AND targets.class 
                IN ('file', 'dir', 'lnk_file', 'sock_file', 'fifo_file', 'chr_file', 'blk_file', 'filesystem')
          OR (contexts.json->>'type' = 'regular file' AND targets.class IN ('file', 'filesystem'))
          OR (contexts.json->>'type' = 'directory' AND targets.class IN ('dir', 'filesystem'))
          OR (contexts.json->>'type' = 'symbolic link' AND targets.class IN ('lnk_file', 'filesystem'))
          OR (contexts.json->>'type' = 'socket' AND targets.class IN ('sock_file', 'filesystem'))
          OR (contexts.json->>'type' = 'character device' AND targets.class IN ('chr_file', 'filesystem'))
          OR (contexts.json->>'type' = 'block device' AND targets.class IN ('blk_file', 'filesystem'))
      )
    )
    WHERE
  """
  conditions = []

  if ok!=ng:
    if ok == "true":
      conditions.append("contexts.json->'label'->>'domain' = files.json->'label'->>'domain'")
    elif ng == "true":
      conditions.append("contexts.json->'label'->>'domain' <> files.json->'label'->>'domain'")
  

  paths, p_condition = path_condition(path)
  args.extend(paths)
  conditions.append(p_condition)

  query += " AND ".join(conditions)

  query += """\
    ORDER BY contexts.id
  """

 
  if domain != "":
    
    if offset==0:
      count_query = """\
        SELECT COUNT(1) FROM ({0}) AS tmp
      """.format(query)
      cursor.execute(count_query, args)
      for row in cursor:
        count, = row
   
    query = query + " LIMIT %s OFFSET %s "
    args.extend([limit, offset])
    
    cursor.execute(query, args)
    for row in cursor:
      context_id, context_pattern, context_domain, file_id, file_path, file_domain = row
      item = {
        "context-id": context_id,
        "context-pattern": context_pattern,
        "context-domain": context_domain,
        "file-id": file_id,
        "file-path": file_path,
        "file-domain": file_domain,
      }
      items.append(item)


  cursor.close()
  connection.close()

  response.content_type = 'application/json'
  data = {
    "count": count,
    "items": items,
  }
  return json.dumps(data)