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
from bottle  import route, run, mako_view as view, static_file, template, url

bottle.TEMPLATE_PATH.append("www/views/")

@route('/static/<filepath:path>', name="static")
def static(filepath):
    return static_file(filepath, root="./thirdparty/web")

from ajax import *
from ajax import common as ajax_common
ajax_common.PORT = 20000
ajax_common.DB = "selinux"

@route('/')
@view('index')
def index():
  from bottle import response, request
  
  args = {}

  return dict(url = url,args = args)


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', action='store', default="8080" )

args = parser.parse_args()

run(host='0.0.0.0', port=args.port, reloader=True, debug = True)