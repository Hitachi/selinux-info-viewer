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

"""SE Policy EXTRACT"""

import os.path
import csv
import sys
from argparse import ArgumentParser

from lib import util
from lib.util import IniFile, Arguments
from lib import seutil


ini = IniFile("config.ini", {})
args = Arguments(ini,description='SELINUX INFORMATION EXTRACT')
args.add("--output-dir", default="result", help="Output folder path")
args.add("--root-path", default="/", help="Root path for find command")
args.add_list("--prune", help="Pruned folders for find command")
args = args.parse()


dist_dir = args.output_dir
path = args.root_path

util.backup_directory(dist_dir)
print "OUTPUT: {0}".format(dist_dir)
print "Extract file contexts."
contexts = seutil.file_context_json_generator()
util.output_json("{0}/contexts.json".format(dist_dir), "w", contexts)

print "Extract file information."
files = seutil.file_info_json_generator(path, prune=args.prune)
util.output_json("{0}/files.json".format(dist_dir), "w", files)

print "Extract SEPolicy rules."
rules = seutil.load_sepolicy_rules()
util.output_json("{0}/rules.json".format(dist_dir), "w", rules)

print "Extract SEPolicy bools"
bools =  seutil.sepolicy_booleans_json_generator()
util.output_json("{0}/bools.json".format(dist_dir), "w", bools)

print "Extract SELinux information"
info = seutil.selinux_info_json_generator()
util.output_json("{0}/info.json".format(dist_dir), "w", info)

print "Extract SEPolicy attributes."
attrs = seutil.sepolicy_attributes_json_generator()
util.output_json("{0}/attributes.json".format(dist_dir), "w", attrs)

print "Extract SEPolicy port information."
ports = seutil.sepolicy_port_json_generator()
util.output_json("{0}/ports.json".format(dist_dir), "w", ports)

print "Extract SELinux process information."
processes = seutil.process_generator()
util.output_json("{0}/processes.json".format(dist_dir), "w", processes)

#netstats = seutil.netstat_generator()
#util.output_json("{0}/netstats.json".format(dist_dir), "w", netstats)

print "Extract SEPolicy type information."
types = seutil.sepolicy_all_types_json_generator()
util.output_json("{0}/types.json".format(dist_dir), "w", types)

print "Extract SELinux TCP information."
tcps = seutil.netstat_tcp_generator()
util.output_json("{0}/tcps.json".format(dist_dir), "w", tcps)

print "Extract SELinux UDP information."
udps = seutil.netstat_udp_generator()
util.output_json("{0}/udps.json".format(dist_dir), "w", udps)

print "Extract SELinux Unix Socket information."
unix_sockets = seutil.netstat_unix_socket_generator()
util.output_json("{0}/unix_sockets.json".format(dist_dir), "w", unix_sockets)