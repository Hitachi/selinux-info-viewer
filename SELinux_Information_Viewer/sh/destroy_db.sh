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

THIRDPARTY=./thirdparty
DBBINPATH=${THIRDPARTY}/db/postgresql/bin/
DBLIBPATH=${THIRDPARTY}/db/postgresql/lib/
DBTMPPATH=tmp/db
DBDATAPATH=${DBTMPPATH}/data

#${DBBINPATH}/pg_ctl -D ${DBDATAPATH} -w stop
rm -r ${DBTMPPATH} 
