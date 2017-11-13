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

"""Common util"""
import subprocess
import shutil
import os.path
from datetime import datetime
import csv
from  ConfigParser import SafeConfigParser as config
from argparse import ArgumentParser

import platform
from datetime import datetime
import json
from types import MethodType

def run_and_readline(command):
  devnull = open(os.devnull, 'wb') 
  proc = subprocess.Popen(
    command,
    shell  = True,
    stdout = subprocess.PIPE,
    stderr = devnull)
  return proc.stdout

def run(command):
  proc = subprocess.Popen(
    command,
    shell  = True,
    stdin  = subprocess.PIPE,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE)
  stdout_data, stderr_data = proc.communicate()
  return (stdout_data, stderr_data)

def rmdir(target_dir):
  if os.path.isdir(target_dir):
   shrmtree(target_dir) 

def remkdir(target_dir):
  rmdir(target_dir)
  os.makedirs(target_dir)

def backup(path):
  if os.path.exists(path):
    dt = datetime.fromtimestamp(os.stat(path).st_mtime)
    time = dt.strftime('%Y%m%d%H%M%S')
    os.rename(path, "{0}.{1}".format(path, time))

def file_backup(file):
  if os.path.isfile(file):
    backup(file)

def fopen(path, mode):
  path = os.path.abspath(path)
  directory = os.path.dirname(path)
  if not os.path.exists(directory):
    os.makedirs(directory)
  return open(path, mode)

def csv_parse(line):
  vals = list(csv.reader([line]))[0]
  vals = map(lambda v: v.strip(), vals)
  return vals

def read_inifile(filename="config.ini", defaults = {}):
 if not os.path.isfile(filename): return None
 inifile = config(defaults)
 inifile.read(filename)
 return inifile

class IniFile:
  def __init__(self, filename, defaults):
    self.ini = read_inifile(filename, defaults)

  def get(self, key, section="settings"):
    if not self.ini.has_option(section, key):
      return None
    val = self.ini.get(section, key)
    if val == "":
      val = None
    return val
  
  def get_list(self, key, section="settings"):
    val = self.get(key, section)
    if val == None:
      return []
    val = csv_parse(val)
    return val    

class Arguments:
  def __init__(self, ini, description):
    self.ini = ini
    self.parser = ArgumentParser(description=description)

  def add(self, key, default=None, help=None):
    ini_val = self.ini.get(key)
    if not ini_val is None:
      default = ini_val
    self.parser.add_argument(key, action='store', default=default, help=help )

  def add_list(self, key, default=[], help=None):
    ini_val = self.ini.get_list(key)
    if len(ini_val) > 0:
      default = ini_val 
    self.parser.add_argument(key, action='store', default= default, nargs="*", help=help)

  def parse(self):
    return self.parser.parse_args()

def backup_directory(path):
  if os.path.isdir(path):
    backup(path)
  os.makedirs(path)


def format_json_string(data):
  return json.dumps(data, sort_keys=False)

def output_json(path, mode, generator):
  with fopen(path, mode) as file:
    for data in generator:
      data = format_json_string(data)
      file.write(data+"\n")


def platform_info():
  data = {
    "system": platform.system(),
    "machine": platform.machine(),
    "hostname": platform.node(),
    "platform": platform.platform(),
    "version": platform.version(),
    "release": platform.release(),
  }
  return data

def python_info():
  build_no, build_date = platform.python_build()
  data = {
    "build_number": build_no,
    "build_date": build_date,
    "compiler": platform.python_compiler(),
    "version": platform.python_version(),
  }
  return data


def time(d=datetime.now()):
  return d.strftime("%Y/%m/%d %H:%M:%S")