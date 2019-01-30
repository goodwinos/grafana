#! /bin/bash

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

# build pristine src tarball from upstream git tagged branch
git checkout -b v$VER v$VER
git archive --format tar --prefix grafana/ -o ../grafana-$VER.src.tar HEAD
gzip ../grafana-$VER.src.tar

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

# webpack tarball
tar czf ../grafana_webpack-$VER.src.tar.gz --transform 's/^/grafana\//' public/build

# done
cp ../grafana-$VER.src.tar.gz ../grafana_webpack-$VER.src.tar.gz $GOPATH/..
echo Created grafana-$VER.src.tar.gz grafana_webpack-$VER.src.tar.gz
exit 0
