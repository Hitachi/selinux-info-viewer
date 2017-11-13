#!/usr/bin/env bash

# Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#    https://opensource.org/licenses/MIT
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OF ANY KIND.

set -eux

source sh/env.sh

if [ ! -e ${DBDATAPATH} ]; then
  INIT_DB=TRUE
  mkdir -p ${DBTMPPATH}
  ${DBBINPATH}/initdb -D ${DBDATAPATH} --locale=C --encoding=UTF-8
fi

if [ ! -e ${DBDATAPATH}/postmaster.pid ]; then
  ${DBBINPATH}/pg_ctl -D ${DBDATAPATH} -w -l ${DBLOGFILE} -o "-p ${DBPORT} " start
fi

if [ -v INIT_DB ] ; then
  source sh/construct_db.sh
fi
