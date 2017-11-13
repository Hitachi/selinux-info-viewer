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

if [ ! -v __ONCE__ ] ; then
  __ONCE__=ONCE
  THIRDPARTY=./thirdparty
  DBBINPATH=${THIRDPARTY}/db/postgresql/bin/
  DBLIBPATH=${THIRDPARTY}/db/postgresql/lib/
  DBTMPPATH=tmp/db
  DBDATAPATH=${DBTMPPATH}/data
  DBLOGFILE=${DBTMPPATH}/log.txt
  DBPORT=20000
  WEBPORT=8080
  JSONDIR=result
  WWWLIBDIR=${THIRDPARTY}/python
  SERVER=www/index.py

  JSONDIR=`readlink -f ${JSONDIR}`

  for OPT in "$@"
  do
      case $OPT in
          '--web-port' )
              WEBPORT=$2
              shift 2
              ;;
          '--db-port' )
              DBPORT=$2
              shift 2
              ;;
      esac
  done

  export PGHOST=localhost
  export POSTGRES_HOME=${DBBINPATH}
  export PGLIB=${DBLIBPATH}
  export PGDATA=${DBDATAPATH}
  export LD_LIBRARY_PATH=${PGLIB}
fi