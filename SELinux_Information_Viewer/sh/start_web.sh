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

PYTHONPATH=${WWWLIBDIR} \
LD_LIBRARY_PATH=${DBLIBPATH} \
python ${SERVER} --port ${WEBPORT}