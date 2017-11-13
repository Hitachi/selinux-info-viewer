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

"""SELinux util"""
import os
import re
import sepolicy
from sepolicy import policy
from seobject import fcontextRecords, booleanRecords
import selinux

import util

FIND_FILE_LABEL_COMMAND = r'find {0} {1} {2} -printf "\"%p\",\" %Z\",\"%M\",\"%u\",\"%g\",\"%y\"\n"' 


def convert_input(line):
    path, label, permission, owner, group, file_type = util.csv_parse(line)
    permission = (permission, owner, group)
    
    attr = label.split(":")
    user = attr[0]
    role = attr[1]
    domain = attr[2]
    level = attr[3]
    label = (user, role, domain, level)
    
    info = (permission, label, file_type) 
    data = ( path, info )
    return data


def selinux_label_command(path, prune_dir=[], ftype=None):
  prune_option = " ".join(map((lambda d: "-path {0} -prune -o".format(d)), prune_dir))
  type_option = ""
  if ftype == "file":
    type_option = "-type f"
  elif ftype == "dir":
    type_option = "-type d"
  elif ftype == "lnk_file":
    type_option = "-type l"
    
  find_cmd = FIND_FILE_LABEL_COMMAND.format(path, prune_option, type_option)
  return find_cmd

def readline_selinux_label(path, prune_dir=[], ftype=None):
  find_cmd = selinux_label_command(path, prune_dir, ftype)
  return util.run_and_readline(find_cmd)


def load_all_domains():
  domains = []
  attributes = sepolicy.get_all_attributes()
  domains.extend(attributes)
  for attr in attributes:
    types = sepolicy.get_types_from_attribute(attr)
    domains.extend(types)
  domains = sorted(set(domains), key=str)
  return domains


def load_attribute_type_map():
  attributes = sepolicy.get_all_attributes()
  attr_to_types_map = {}
  type_to_attr_map = {}
  for attr in attributes:
    types = sepolicy.get_types_from_attribute(attr)
    attr_to_types_map[attr] = types
    for typ in types:
      attr_list = type_to_attr_map.get(typ,[])
      attr_list.append(attr)
      type_to_attr_map[typ] = attr_list

  for (attr, types) in attr_to_types_map.items():
    attr_to_types_map[attr] = sorted(set(types),key=str)

  for (typ, attrs) in type_to_attr_map.items():
    type_to_attr_map[typ] = sorted(set(attrs),key=str)
  return (attr_to_types_map, type_to_attr_map)


def load_sepolicy_rules(types=None, info={}):
  if types is None:
    types = [
      sepolicy.ALLOW, sepolicy.AUDITALLOW, #sepolicy.NEVERALLOW, 
      sepolicy.DONTAUDIT, sepolicy.TRANSITION, sepolicy.ROLE_ALLOW
    ]
  rules = sepolicy.search(types, info)
  return rules

def load_allow_map(options = {}):
  allows = load_sepolicy_rules([sepolicy.ALLOW], options)
  all_allow_map = {}
  if allows is None:
    return all_allow_map
  for allow in allows:
    source = allow[sepolicy.SOURCE]
    target = allow[sepolicy.TARGET]
    target_map = all_allow_map.get(source, {})
    allowlist = target_map.get(target, [] )
    allow = (allow[sepolicy.CLASS], allow[sepolicy.PERMS])
    allowlist.append(allow)
    target_map[target] = allowlist
    all_allow_map[source] = target_map
  return all_allow_map

def convert_allow_list(map):
  results = []
  for item in map.items():
    results.append(item)
  return results


def load_allow_map_with_args(args):
  source = args.source
  target = args.target
  perms = args.perms
  klass = args.klass
  permit_search_options = {}
  if source != "":
    permit_search_options[sepolicy.SOURCE] = source

  if target != "":
    permit_search_options[sepolicy.TARGET] = target

  if len(perms) > 0 :
    permit_search_options[sepolicy.PERMS] = perms

  if klass != "":
    permit_search_options[sepolicy.CLASS] = klass

  allow_map = load_allow_map(permit_search_options)
  return allow_map



def _init_content(context):
  main = context[0]
  pattern = main[0]
  regexp = None
  try:
    regexp = re.compile("^"+pattern+"$")
  except:
    None

  target_type = main[1]

  attr = context[1]
  if attr is None:
    attr = ("","","","")

  context = ( regexp, pattern, attr, target_type )
  return context



def load_all_contexts():
  contexts = fcontextRecords().get_all().items()
  contexts = map(_init_content, contexts )
  return contexts



def file_context_json_generator():
  contexts = load_all_contexts()
  for context in contexts:
    ( regexp, pattern, attr, target_type ) = context
    ( seuser, serole, sedomain, selevel ) = attr
    data = {
      "pattern": pattern,
      "label": {
        "user": seuser,
        "role": serole,
        "domain": sedomain,
        "level": selevel,
      },
      "type": target_type,
    }
    yield data


def file_info_json_generator(path, prune=[] , file_type=None):
  for line in readline_selinux_label(path, prune, file_type):
    file = convert_input(line)
    ( path, info ) = file
    ( permission, label, file_type )  = info
    ( permission, owner, group ) = permission
    ( user, role, domain, level ) = label
    
    data = {
      "path": path,
      "permission": permission,
      "owner": owner,
      "group": group,
      "label": {
        "user": user,
        "role": role,
        "domain": domain,
        "level": level,
      },
      "file_type": file_type, 
    }

    yield data


def sepolicy_rules_json_generator(types=None, info={}):
  rules = load_sepolicy_rules(types, info)
  for rule in rules:
    yield rule


def sepolicy_booleans_json_generator():
  for bool in sepolicy.get_all_bools():
    name = bool['name']
    active_flag = selinux.security_get_boolean_active(name)
    current = (False, True)[active_flag]
    records = booleanRecords()
    desc = records.get_desc(name)
    yield {
      "name": name,
      "current": current,
      "default": bool['state'],
      "desc": desc,
    }

def sestatus():
  data = {}
  command = "sestatus"
  for line in util.run_and_readline(command):
    index = line.find(":")
    if index == -1: continue
    label = line[:index]
    val = line[(index+1):].strip()
    data[label] = val
  return data

def sepolicy_common_info():
  sestatus()
  data ={
    "date": util.time(),
    "platform" : util.platform_info(),
    "python": util.python_info(),
    "policy": sepolicy.get_installed_policy(),
    "status": sestatus(),
  }
  return data

def selinux_info_json_generator():
  info = sepolicy_common_info()
  yield info

def sepolicy_attributes_json_generator():
  attributes = sepolicy.get_all_attributes()
  for attr in attributes:
    types = sepolicy.get_types_from_attribute(attr)
    data = {
      "name": attr,
      "types": types,
    }
    yield data

def sepolicy_port_json_generator():
  ports = sepolicy.info(sepolicy.PORT)
  for port in ports:
    yield port

def parse_label(label):
  labels = label.split(":")
  (user, role, domain), level = labels[:3], labels[3:]
  level = ":".join(level)
  return  {
    "user": user,
    "role": role,
    "domain": domain,
    "level": level,
  }

def process_generator():
  command = "ps  -eZ --no-headers"
  for line in util.run_and_readline(command):
    label, pid, tty, time, process = line.split()
    data = {
      "pid": pid,
      "name": process,
      "label": parse_label(label),
      "tty": tty,
      "time": time,
    }
    yield data

def netstat_generator():
  command = "sudo netstat -Znp"
  out = util.run_and_readline(command)
  for line in out:
    if line.startswith("Proto RefCnt Flags"): break

  pattern = r'^([^ ]+?) +([0-9]+?) +(\[[^\]]+?\]) +([^ ]+?) +(([^ ]+?) +)?([0-9]+?) +([0-9]+?)/([^ :]+?)(: ([^ ]+?))? +([^ ]+)( +([^ ]+))?$'
  regex = re.compile(pattern)
  for line in out:
      line = line.strip()
      match = regex.match(line)
      if match:
        data = {
          "Proto": match.group(1) ,
          "RefCnt": match.group(2) ,
          "Flags": match.group(3) ,
          "Type": match.group(4) ,
          "State": match.group(6) ,
          "I-Node": match.group(7) ,
          "PID": match.group(8) ,
          "Program name": match.group(9) ,
          "User": match.group(11),
          "Security Context": match.group(12),
          "Path": match.group(14),
        }
        yield data

def sepolicy_all_types_json_generator():
  types = sepolicy.get_all_domains()
  for type in types:
    data = {
      "name": type,
    }
    yield data

def netstat_ip_generator(type):
  command = r"sudo netstat -Znp{0} | sed  -e '1,2d'| sed 's/ \+/ /g'".format(type)
  pattern = r'^([^ ]+?) ([0-9]+?) ([0-9]+?) ([0-9.:]+?) ([0-9.:]+?) ([^ ]+?) ([0-9]+?/[^ ]+?(: [^ ]+?)?|-) (.+)$'
  regex = re.compile(pattern)
  for line in util.run_and_readline(command):
      line = line.strip()
      match = regex.match(line)
      if match:
        local_address = match.group(4)
        ip, port = local_address.split(":")
        local_address = {
          "ip": ip,
          "port": int(port),
        }

        foreign_address = match.group(5)
        ip, port = foreign_address.split(":")
        foreign_address = {
          "ip": ip,
          "port": int(port),
        }

        pid = match.group(7)
        program = None
        if pid == "-":
          pid = None
        else:
          pid, program = pid.split("/")

        label = match.group(9)
        if label == "-":
          label = None
        else:
          vals = label.split(":")
          user, role, domain = vals[:3]
          level = ":".join(vals[3:])
          label = {
            "user": user,
            "role": role,
            "domain": domain,
            "level": level,
          }

        data = {
          "Proto": match.group(1) ,
          "Recv-Q": match.group(2) ,
          "Send-Q": match.group(3) ,
          "Local Address": local_address,
          "Foreign Address": foreign_address ,
          "State": match.group(6) ,
          "PID": pid ,
          "Program name": program ,
          "Security Context": label,
        }
        yield data

def netstat_tcp_generator():
  return netstat_ip_generator("t")
  
def netstat_udp_generator():
  return netstat_ip_generator("u")
  
def netstat_unix_socket_generator():
  command = r"sudo netstat -Znpx | sed  -e '1,2d'| sed 's/ \+/ /g'"
  pattern = r'^(?P<Proto>[^ ]+?)' \
            r' (?P<RefCnt>[0-9]+?)' \
            r' \[(?P<Flags>[^\]]+?)\]' \
            r' (?P<Type>[^ ]+?)' \
            r' ((?P<State>[^ ]+?) )?(?P<INode>[0-9]+?)' \
            r' (-|(?P<PID>[0-9]+?)/(?P<ProgramName>[^ ]+?(: [^ ]+?)?))' \
            r' (-|(?P<SecurityContext>[^ ]+?))' \
            r'($| (?P<Path>.+?)$)'
  regex = re.compile(pattern)
  for line in util.run_and_readline(command):
      line = line.strip()
      match = regex.match(line)
      if match:
      
        label = match.group("SecurityContext")
        if not label is None:
          vals = label.split(":")
          user, role, domain = vals[:3]
          level = ":".join(vals[3:])
          label = {
            "user": user,
            "role": role,
            "domain": domain,
            "level": level,
          }
        data = {
          "Proto": match.group("Proto") ,
          "RefCnt": match.group("RefCnt") ,
          "Flags": match.group("Flags") ,
          "Type": match.group("Type"),
          "State": match.group("State"),
          "I-Node": match.group("INode"),
          "PID": match.group("PID"),
          "Program name": match.group("ProgramName"),
          "Security Context": label,
          "Path": match.group("Path"),
        }
        yield data