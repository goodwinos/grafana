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
[ ! -f /usr/bin/go ] && echo Error, please install \"golang\" package && exit 1

export GOPATH=`pwd`/"$BUILDDIR"
cd $GOPATH
echo "Building in $GOPATH ..."

# get src tree and set cwd
echo Fetching pristine upstream git tagged branch for grafana version v$VER ...
go get github.com/grafana/grafana
cd $GOPATH/src/github.com/grafana/grafana

# get upstream git tagged branch
git checkout -b v$VER v$VER

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

# webpack tarball. Includes public/views because index.html references the webpack
tar czf ../grafana_webpack-$VER.tar.gz --transform "s/^/grafana-$VER\//" public/build public/views
cp ../grafana_webpack-$VER.tar.gz $GOPATH/..

# source tarball
cd $GOPATH/..
wget --quiet -O grafana-$VER.tar.gz https://github.com/grafana/grafana/archive/v$VER/grafana-$VER.tar.gz

# done
echo Created grafana-$VER.tar.gz and grafana_webpack-$VER.tar.gz
echo These should be copied to your \$HOME/rpmbuild/SOURCES

exit 0
