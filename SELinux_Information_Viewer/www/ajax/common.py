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

import bottle
import psycopg2
import json
import re

HOST = "localhost"
PORT = 5432
DB = "postgres"

def ajax(body):
  def wrapper(*args, **kwargs):
    from bottle import response, request
    connection = psycopg2.connect(host=HOST, port=PORT, dbname=DB)
    cursor = connection.cursor()
    data = {}
    try:
      data = body(cursor, request, response)
    finally:
      cursor.close()
      connection.close()

    response.content_type = 'application/json'
    return json.dumps(data) 
  return wrapper

def count(cursor, query, args):
  count_query = """\
    SELECT COUNT(1) FROM ({0}) AS tmp
  """.format(query)
  cursor.execute(count_query, args)
  for row in cursor:
    count, = row
  return count

def like_escape(query):
  return re.sub(r'([%\.\\])', r'\\\1', query)

def like_condition(query, column):
  query = like_escape(query)
  querys = query.split(" ")
  querys = [ "%{0}%".format(query) for query in querys ]
  condition = " {0} LIKE %s ".format(column)
  condition = " AND ".join([ condition for query in querys])
  return querys, condition

def path_condition(path):
  return like_condition(path, "files.json->>'path'")