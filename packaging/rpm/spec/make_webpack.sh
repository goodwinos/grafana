#! /bin/bash
#
# Copyright (c) 2019 Red Hat.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

[ $# -ne 1 ] && echo "Usage: $0 version" && exit 1

# grafana version (must be tagged on github.com/grafana/grafana as "v$VER")
VER=$1
BUILDDIR=`mktemp -d buildXXXXXX`

[ ! -f /usr/bin/npm ] && echo Error, please install \"npm\" package && exit 1

# get src tree and set cwd
echo Fetching pristine upstream git tagged branch for grafana version v$VER ...
git clone -b v$VER https://github.com/grafana/grafana grafana-$VER
cd grafana-$VER

# exclude the phantomjs-prebuilt binary module from the webpack
sed -ie '/phantomjs-prebuilt/d' package.json

# nuke grunt task for copying phantomjs
rm -f scripts/grunt/options/phantomjs.js
sed -ie '/phantomjs/d' scripts/grunt/*.js

# populate node_modules using package.json
npm install yarn grunt
echo Running yarn to populate local node_modules ....
node_modules/yarn/bin/yarn --ignore-engines install --pure-lockfile > yarn.out 2>&1

# build the webpack
echo Running grunt to create webpack ....
node_modules/grunt/bin/grunt > grunt.out 2>&1

cd ..

# webpack tarball. Includes public/views because index.html references the webpack
tar czf grafana_webpack-$VER.tar.gz grafana-$VER/public/build grafana-$VER/public/views

# done
echo Created grafana_webpack-$VER.tar.gz
echo These should be copied to your \$HOME/rpmbuild/SOURCES

exit 0
