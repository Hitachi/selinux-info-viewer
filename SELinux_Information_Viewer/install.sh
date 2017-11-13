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

VIEWER_HOME=`pwd`
INSTALL_DIR=${VIEWER_HOME}/thirdparty
DOWNLOAD_DIR=${INSTALL_DIR}/downloads
PYTHON_DIR=${INSTALL_DIR}/python
WEB_DIR=${INSTALL_DIR}/web
JS_DIR=${WEB_DIR}/js
CSS_DIR=${WEB_DIR}/css
FONT_DIR=${WEB_DIR}/fonts

mkdir -p ${INSTALL_DIR}
mkdir -p ${DOWNLOAD_DIR}
mkdir -p ${PYTHON_DIR}
mkdir -p ${WEB_DIR}
mkdir -p ${JS_DIR}
mkdir -p ${CSS_DIR}
mkdir -p ${FONT_DIR}

cd ${DOWNLOAD_DIR}
curl -O http://fontawesome.io/assets/font-awesome-4.7.0.zip
unzip font-awesome-4.7.0.zip
cp -r font-awesome-4.7.0/css ${WEB_DIR}
cp -r font-awesome-4.7.0/fonts ${WEB_DIR}

cd ${DOWNLOAD_DIR}
curl -O https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css
cp bootstrap.min.css ${CSS_DIR}/bootstrap.min.css


cd ${DOWNLOAD_DIR}
curl -O https://unpkg.com/bootstrap-vue@0.18.0/dist/bootstrap-vue.js
cp bootstrap-vue.js ${JS_DIR}/bootstrap-vue.js

curl -O https://unpkg.com/bootstrap-vue@0.18.0/dist/bootstrap-vue.css
cp bootstrap-vue.css ${CSS_DIR}/bootstrap-vue.css

cd ${DOWNLOAD_DIR}
curl -O https://unpkg.com/babel-polyfill@6.23.0/dist/polyfill.min.js
cp polyfill.min.js ${JS_DIR}/polyfill.min.js


cd ${DOWNLOAD_DIR}
curl -O https://raw.githubusercontent.com/HubSpot/tether/v1.4.0/dist/js/tether.min.js
cp tether.min.js ${JS_DIR}/tether.min.js

curl -O https://raw.githubusercontent.com/HubSpot/tether/v1.4.0/dist/css/tether.min.css
cp tether.min.css ${CSS_DIR}/tether.min.css


cd ${DOWNLOAD_DIR}
curl -O https://raw.githubusercontent.com/vuejs/vue/v2.3.3/dist/vue.min.js
cp vue.min.js ${JS_DIR}/vue.min.js

cd ${DOWNLOAD_DIR}
curl -O https://code.jquery.com/jquery-3.2.1.min.js
cp jquery-3.2.1.min.js ${JS_DIR}/jquery.min.js

cd ${DOWNLOAD_DIR}
curl -O https://pypi.python.org/packages/eb/f3/67579bb486517c0d49547f9697e36582cd19dafb5df9e687ed8e22de57fa/Mako-1.0.7.tar.gz
tar xvfz Mako-1.0.7.tar.gz
cp -r Mako-1.0.7/mako ${PYTHON_DIR}

cd ${DOWNLOAD_DIR}
curl -O https://raw.githubusercontent.com/bottlepy/bottle/master/bottle.py
cp bottle.py ${PYTHON_DIR}

cd ${DOWNLOAD_DIR}
curl -O https://ftp.postgresql.org/pub/source/v9.6.2/postgresql-9.6.2.tar.gz
tar xvzf postgresql-9.6.2.tar.gz
cd postgresql-9.6.2/
./configure \
  --prefix=${INSTALL_DIR}/db/postgresql \
  --without-readline \
  --without-zlib
make
make install

cd contrib/
cd pg_trgm/
make install

cd ${DOWNLOAD_DIR}
PATH=${INSTALL_DIR}/db/postgresql/bin/:$PATH
curl -O http://initd.org/psycopg/tarballs/PSYCOPG-2-7/psycopg2-2.7.3.tar.gz
tar xvfz psycopg2-2.7.3.tar.gz
cd psycopg2-2.7.3
python setup.py build
python setup.py install --prefix=.
cp -r lib64/python2.7/site-packages/psycopg2 ${PYTHON_DIR}


cd ${VIEWER_HOME}
