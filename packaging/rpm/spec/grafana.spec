Name:             grafana
Version:          6.0.1
Release:          1%{?dist}
Summary:          Metrics dashboard and graph editor
License:          ASL 2.0
URL:              https://grafana.org

# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz

# Source1 contains the front-end javascript modules bundled into a webpack
Source1:          grafana_webpack-%{version}.tar.gz

# Source2 is the script to create the above webpack from grafana sources
Source2:          make_webpack.sh

# Fedora/FHS and config patch
Patch0:           000-grafana-fedora.patch

ExclusiveArch:    %{nodejs_arches} # nodejs arches only

# omit golang debugsource, see BZ995136 and related
%define           _debugsource_template %{nil}

%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}
%global           GRAFANA_HOME %{_datadir}/%{name}

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

BuildRequires:    systemd
BuildRequires:    golang

#
# golang build deps. These allow us to unbundle some vendor golang source.
# No unbundling for old Fedora and older RHEL - use the Grafana vendor src.
# Note: for grafana v6.x, golang >= 1.11 is needed, but f28 only has 1.10.
# So we treat f28 (and earlier) as "old", and will soon be unsupported
# anyway.
#
%if 0%{?fedora} > 28 || 0%{?rhel} > 7
BuildRequires: golang-github-aws-aws-sdk-go-devel
BuildRequires: golang-github-beorn7-perks-devel
BuildRequires: golang-github-bmizerany-assert-devel
BuildRequires: golang-github-bradfitz-gomemcache-devel
BuildRequires: golang-github-BurntSushi-toml-devel
BuildRequires: golang-github-codegangsta-cli-devel
BuildRequires: golang-github-davecgh-go-spew-devel
BuildRequires: golang-github-denisenkom-go-mssqldb-devel
BuildRequires: golang-github-fatih-color-devel
BuildRequires: golang-github-go-ini-ini-devel
BuildRequires: golang-github-golang-appengine-devel
BuildRequires: golang-github-golang-sys-devel
BuildRequires: golang-github-go-macaron-inject-devel
BuildRequires: golang-github-google-go-genproto-devel
BuildRequires: golang-github-gopherjs-devel
BuildRequires: golang-github-gorilla-websocket-devel
BuildRequires: golang-github-go-sql-driver-mysql-devel
BuildRequires: golang-github-grpc-grpc-go-devel
BuildRequires: golang-github-hashicorp-go-hclog-devel
BuildRequires: golang-github-hashicorp-go-plugin-devel
BuildRequires: golang-github-hashicorp-yamux-devel
BuildRequires: golang-github-hashicorp-version-devel
BuildRequires: golang-github-jmespath-go-jmespath-devel
BuildRequires: golang-github-jtolds-gls-devel
BuildRequires: golang-github-klauspost-cpuid-devel
BuildRequires: golang-github-klauspost-crc32-devel
BuildRequires: golang-github-kr-pretty-devel
BuildRequires: golang-github-kr-text-devel
BuildRequires: golang-github-lib-pq-devel
BuildRequires: golang-github-mattn-go-colorable-devel
BuildRequires: golang-github-mattn-go-isatty-devel
BuildRequires: golang-github-mattn-go-sqlite3-devel
BuildRequires: golang-github-matttproud-golang_protobuf_extensions-devel
BuildRequires: golang-github-mitchellh-go-testing-interface-devel
BuildRequires: golang-github-patrickmn-go-cache-devel
BuildRequires: golang-github-pkg-errors-devel
BuildRequires: golang-github-prometheus-client_golang-devel
BuildRequires: golang-github-prometheus-client_model-devel
BuildRequires: golang-github-prometheus-common-devel
BuildRequires: golang-github-prometheus-procfs-devel
BuildRequires: golang-github-sergi-go-diff-devel
BuildRequires: golang-github-smartystreets-assertions-devel
BuildRequires: golang-github-smartystreets-goconvey-devel
BuildRequires: golang-golangorg-crypto-devel
BuildRequires: golang-golang-org-net-devel
BuildRequires: golang-golangorg-text-devel
BuildRequires: golang-googlecode-goauth2-devel
BuildRequires: golang-googlecode-goprotobuf-devel
BuildRequires: golang-google-golangorg-cloud-devel
BuildRequires: golang-gopkg-asn1-ber-1-devel
BuildRequires: golang-gopkg-yaml-devel
BuildRequires: golang-x-sync-devel
BuildRequires: golang-github-klauspost-compress-devel
BuildRequires: golang-gopkg-ini-1-devel
BuildRequires: golang-gopkg-square-jose-2-devel

%else
# Old RHEL / Fedora - just bundle all vendor sources
Provides: bundled(golang-github-aws-aws-sdk-go-devel)
Provides: bundled(golang-github-beorn7-perks-devel)
Provides: bundled(golang-github-bmizerany-assert-devel)
Provides: bundled(golang-github-bradfitz-gomemcache-devel)
Provides: bundled(golang-github-BurntSushi-toml-devel)
Provides: bundled(golang-github-codegangsta-cli-devel)
Provides: bundled(golang-github-davecgh-go-spew-devel)
Provides: bundled(golang-github-denisenkom-go-mssqldb-devel)
Provides: bundled(golang-github-fatih-color-devel)
Provides: bundled(golang-github-go-ini-ini-devel)
Provides: bundled(golang-github-golang-appengine-devel)
Provides: bundled(golang-github-golang-sys-devel)
Provides: bundled(golang-github-go-macaron-inject-devel)
Provides: bundled(golang-github-google-go-genproto-devel)
Provides: bundled(golang-github-gopherjs-devel)
Provides: bundled(golang-github-gorilla-websocket-devel)
Provides: bundled(golang-github-go-sql-driver-mysql-devel)
Provides: bundled(golang-github-grpc-grpc-go-devel)
Provides: bundled(golang-github-hashicorp-go-hclog-devel)
Provides: bundled(golang-github-hashicorp-go-plugin-devel)
Provides: bundled(golang-github-hashicorp-version-devel)
Provides: bundled(golang-github-hashicorp-yamux-devel)
Provides: bundled(golang-github-jmespath-go-jmespath-devel)
Provides: bundled(golang-github-jtolds-gls-devel)
Provides: bundled(golang-github-klauspost-compress-devel)
Provides: bundled(golang-github-klauspost-cpuid-devel)
Provides: bundled(golang-github-klauspost-crc32-devel)
Provides: bundled(golang-github-kr-pretty-devel)
Provides: bundled(golang-github-kr-text-devel)
Provides: bundled(golang-github-lib-pq-devel)
Provides: bundled(golang-github-mattn-go-colorable-devel)
Provides: bundled(golang-github-mattn-go-isatty-devel)
Provides: bundled(golang-github-mattn-go-sqlite3-devel)
Provides: bundled(golang-github-matttproud-golang_protobuf_extensions-devel)
Provides: bundled(golang-github-mitchellh-go-testing-interface-devel)
Provides: bundled(golang-github-patrickmn-go-cache-devel)
Provides: bundled(golang-github-pkg-errors-devel)
Provides: bundled(golang-github-prometheus-client_golang-devel)
Provides: bundled(golang-github-prometheus-client_model-devel)
Provides: bundled(golang-github-prometheus-common-devel)
Provides: bundled(golang-github-prometheus-procfs-devel)
Provides: bundled(golang-github-sergi-go-diff-devel)
Provides: bundled(golang-github-smartystreets-assertions-devel)
Provides: bundled(golang-github-smartystreets-goconvey-devel)
Provides: bundled(golang-golangorg-crypto-devel)
Provides: bundled(golang-golang-org-net-devel)
Provides: bundled(golang-golangorg-text-devel)
Provides: bundled(golang-googlecode-goauth2-devel)
Provides: bundled(golang-google-golangorg-cloud-devel)
Provides: bundled(golang-gopkg-ini-1-devel)
Provides: bundled(golang-gopkg-square-jose-2-devel)
Provides: bundled(golang-gopkg-yaml-devel)
Provides: bundled(golang-x-sync-devel)
%endif

# Declare bundled/vendor golang devel packages - not (yet) in Fedora
# These golang packages need to be packaged in Fedora.
Provides: bundled(golang-github-benbjohnson-clock-devel)
Provides: bundled(golang-github-codahale-hdrhistogram-devel)
Provides: bundled(golang-github-facebookgo-inject-devel)
Provides: bundled(golang-github-facebookgo-structtag-devel)
Provides: bundled(golang-github-go-macaron-binding-devel)
Provides: bundled(golang-github-go-macaron-gzip-devel)
Provides: bundled(golang-github-go-macaron-session-devel)
Provides: bundled(golang-github-gosimple-slug-devel)
Provides: bundled(golang-github-go-stack-stack-devel)
Provides: bundled(golang-github-go-xorm-builder-devel)
Provides: bundled(golang-github-go-xorm-core-devel)
Provides: bundled(golang-github-go-xorm-xorm-devel)
Provides: bundled(golang-github-grafana-grafana-plugin-model-devel)
Provides: bundled(golang-github-inconshreveable-log15-devel)
Provides: bundled(golang-github-oklog-run-devel)
Provides: bundled(golang-github-opentracing-opentracing-go-devel)
Provides: bundled(golang-github-rainycape-unidecode-devel)
Provides: bundled(golang-github-teris-io-shortid-devel)
Provides: bundled(golang-github-uber-jaeger-client-go-devel)
Provides: bundled(golang-github-uber-jaeger-lib-devel)
Provides: bundled(golang-github-Unknwon-com-devel)
Provides: bundled(golang-github-VividCortex-mysqlerr-devel)
Provides: bundled(golang-github-yudai-gojsondiff-devel)
Provides: bundled(golang-github-yudai-golcs-devel)
Provides: bundled(golang-gopkg-alexcesaro-quotedprintable-3-devel)
Provides: bundled(golang-gopkg-bufio-1-devel)
Provides: bundled(golang-gopkg-macaron-1-devel)
Provides: bundled(golang-gopkg-mail-2-devel)
Provides: bundled(golang-gopkg-redis-2-devel)

# Declare all nodejs modules bundled in the webpack - this is for security
# purposes so if nodejs-foo ever needs an update, affected packages can be
# easily identified. Generated from package-lock.json once the webpack has
# been built with make_webpack.sh.
Provides: bundled(nodejs-abbrev) = 1.1.1
Provides: bundled(nodejs-ansi-regex) = 2.1.1
Provides: bundled(nodejs-ansi-styles) = 2.2.1
Provides: bundled(nodejs-argparse) = 1.0.10
Provides: bundled(nodejs-array-find-index) = 1.0.2
Provides: bundled(nodejs-async) = 1.5.2
Provides: bundled(nodejs-balanced-match) = 1.0.0
Provides: bundled(nodejs-brace-expansion) = 1.1.11
Provides: bundled(nodejs-builtin-modules) = 1.1.1
Provides: bundled(nodejs-camelcase) = 2.1.1
Provides: bundled(nodejs-camelcase-keys) = 2.1.0
Provides: bundled(nodejs-chalk) = 1.1.3
Provides: bundled(nodejs-coffee-script) = 1.10.0
Provides: bundled(nodejs-colors) = 1.1.2
Provides: bundled(nodejs-concat-map) = 0.0.1
Provides: bundled(nodejs-currently-unhandled) = 0.4.1
Provides: bundled(nodejs-dateformat) = 1.0.12
Provides: bundled(nodejs-decamelize) = 1.2.0
Provides: bundled(nodejs-error-ex) = 1.3.2
Provides: bundled(nodejs-escape-string-regexp) = 1.0.5
Provides: bundled(nodejs-esprima) = 2.7.3
Provides: bundled(nodejs-eventemitter2) = 0.4.14
Provides: bundled(nodejs-exit) = 0.1.2
Provides: bundled(nodejs-find-up) = 1.1.2
Provides: bundled(nodejs-findup-sync) = 0.3.0
Provides: bundled(nodejs-fs.realpath) = 1.0.0
Provides: bundled(nodejs-get-stdin) = 4.0.1
Provides: bundled(nodejs-getobject) = 0.1.0
Provides: bundled(nodejs-glob) = 7.0.6
Provides: bundled(nodejs-graceful-fs) = 4.1.15
Provides: bundled(nodejs-grunt) = 1.0.1
Provides: bundled(nodejs-grunt-cli) = 1.2.0
Provides: bundled(nodejs-grunt-known-options) = 1.1.1
Provides: bundled(nodejs-grunt-legacy-log) = 1.0.2
Provides: bundled(nodejs-lodash) = 4.17.11
Provides: bundled(nodejs-grunt-legacy-log-utils) = 1.0.0
Provides: bundled(nodejs-grunt-legacy-util) = 1.0.0
Provides: bundled(nodejs-has-ansi) = 2.0.0
Provides: bundled(nodejs-hooker) = 0.2.3
Provides: bundled(nodejs-hosted-git-info) = 2.7.1
Provides: bundled(nodejs-iconv-lite) = 0.4.24
Provides: bundled(nodejs-indent-string) = 2.1.0
Provides: bundled(nodejs-inflight) = 1.0.6
Provides: bundled(nodejs-inherits) = 2.0.3
Provides: bundled(nodejs-is-arrayish) = 0.2.1
Provides: bundled(nodejs-is-builtin-module) = 1.0.0
Provides: bundled(nodejs-is-finite) = 1.0.2
Provides: bundled(nodejs-is-utf8) = 0.2.1
Provides: bundled(nodejs-isexe) = 2.0.0
Provides: bundled(nodejs-js-yaml) = 3.5.5
Provides: bundled(nodejs-load-json-file) = 1.1.0
Provides: bundled(nodejs-loud-rejection) = 1.6.0
Provides: bundled(nodejs-map-obj) = 1.0.1
Provides: bundled(nodejs-meow) = 3.7.0
Provides: bundled(nodejs-minimatch) = 3.0.4
Provides: bundled(nodejs-minimist) = 1.2.0
Provides: bundled(nodejs-nopt) = 3.0.6
Provides: bundled(nodejs-normalize-package-data) = 2.4.2
Provides: bundled(nodejs-number-is-nan) = 1.0.1
Provides: bundled(nodejs-object-assign) = 4.1.1
Provides: bundled(nodejs-once) = 1.4.0
Provides: bundled(nodejs-parse-json) = 2.2.0
Provides: bundled(nodejs-path-exists) = 2.1.0
Provides: bundled(nodejs-path-is-absolute) = 1.0.1
Provides: bundled(nodejs-path-type) = 1.1.0
Provides: bundled(nodejs-pify) = 2.3.0
Provides: bundled(nodejs-pinkie) = 2.0.4
Provides: bundled(nodejs-pinkie-promise) = 2.0.1
Provides: bundled(nodejs-read-pkg) = 1.1.0
Provides: bundled(nodejs-read-pkg-up) = 1.0.1
Provides: bundled(nodejs-redent) = 1.0.0
Provides: bundled(nodejs-repeating) = 2.0.1
Provides: bundled(nodejs-resolve) = 1.1.7
Provides: bundled(nodejs-rimraf) = 2.2.8
Provides: bundled(nodejs-safer-buffer) = 2.1.2
Provides: bundled(nodejs-semver) = 5.6.0
Provides: bundled(nodejs-signal-exit) = 3.0.2
Provides: bundled(nodejs-spdx-correct) = 3.1.0
Provides: bundled(nodejs-spdx-exceptions) = 2.2.0
Provides: bundled(nodejs-spdx-expression-parse) = 3.0.0
Provides: bundled(nodejs-spdx-license-ids) = 3.0.3
Provides: bundled(nodejs-sprintf-js) = 1.0.3
Provides: bundled(nodejs-strip-ansi) = 3.0.1
Provides: bundled(nodejs-strip-bom) = 2.0.0
Provides: bundled(nodejs-strip-indent) = 1.0.1
Provides: bundled(nodejs-supports-color) = 2.0.0
Provides: bundled(nodejs-trim-newlines) = 1.0.0
Provides: bundled(nodejs-underscore.string) = 3.2.3
Provides: bundled(nodejs-validate-npm-package-license) = 3.0.4
Provides: bundled(nodejs-which) = 1.2.14
Provides: bundled(nodejs-wrappy) = 1.0.2
Provides: bundled(nodejs-yarn) = 1.13.0

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1
%patch0 -p1

%build
# Set up build subdirs and links
mkdir -p %{_builddir}/src/github.com/grafana
ln -sf %{_builddir}/%{name}-%{version} \
    %{_builddir}/src/github.com/grafana/grafana

# remove some development files
rm -f %{_builddir}/src/github.com/grafana/grafana/public/sass/.sass-lint.yml
rm -f %{_builddir}/src/github.com/grafana/grafana/public/test/.jshintrc

%if 0%{?fedora} > 28 || 0%{?rhel} > 7
#
# Unbundle grafana vendor/golang sources that are provided via BuildRequires
#
%define _vendor %{_builddir}/src/github.com/grafana/grafana/vendor

rm -r %{_vendor}/cloud.google.com
rm -r %{_vendor}/google.golang.org
rm -r %{_vendor}/golang.org/x/crypto
rm -r %{_vendor}/golang.org/x/text
rm -r %{_vendor}/golang.org/x/net
rm -r %{_vendor}/gopkg.in/asn1-ber.v1
rm -r %{_vendor}/gopkg.in/yaml.v2
rm -r %{_vendor}/github.com/beorn7
rm -r %{_vendor}/github.com/bmizerany
rm -r %{_vendor}/github.com/bradfitz
rm -r %{_vendor}/github.com/BurntSushi
rm -r %{_vendor}/github.com/codegangsta
rm -r %{_vendor}/github.com/davecgh
rm -r %{_vendor}/github.com/denisenkom
rm -r %{_vendor}/github.com/fatih
rm -r %{_vendor}/github.com/go-macaron/inject
rm -r %{_vendor}/github.com/gopherjs
rm -r %{_vendor}/github.com/gorilla/websocket
rm -r %{_vendor}/github.com/go-sql-driver
rm -r %{_vendor}/github.com/hashicorp/go-hclog
rm -r %{_vendor}/github.com/hashicorp/yamux
rm -r %{_vendor}/github.com/hashicorp/go-version
rm -r %{_vendor}/github.com/jmespath/go-jmespath
rm -r %{_vendor}/github.com/jtolds/gls
rm -r %{_vendor}/github.com/klauspost/cpuid
rm -r %{_vendor}/github.com/klauspost/crc32
rm -r %{_vendor}/github.com/kr/pretty
rm -r %{_vendor}/github.com/kr/text
rm -r %{_vendor}/github.com/lib/pq
rm -r %{_vendor}/github.com/mattn/go-colorable
rm -r %{_vendor}/github.com/mattn/go-isatty
rm -r %{_vendor}/github.com/mattn/go-sqlite3
rm -r %{_vendor}/github.com/matttproud
rm -r %{_vendor}/github.com/mitchellh
rm -r %{_vendor}/github.com/patrickmn
rm -r %{_vendor}/github.com/pkg/errors
rm -r %{_vendor}/github.com/prometheus/client_golang
rm -r %{_vendor}/github.com/prometheus/client_model
rm -r %{_vendor}/github.com/prometheus/common
rm -r %{_vendor}/github.com/prometheus/procfs
rm -r %{_vendor}/github.com/sergi/go-diff
rm -r %{_vendor}/github.com/smartystreets
%endif

# Build server-side binaries: grafana-server and grafana-cli
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}:%{gopath}
go run build.go build

%install
# Fix up a few things (arch bin directories, modes)
[ ! -d bin/x86_64 ] && ln -sf linux-amd64 bin/x86_64
[ ! -d bin/i386 ] && ln -sf linux-386 bin/i386
[ ! -d bin/ppc64le ] && ln -sf linux-ppc64le bin/ppc64le
[ ! -d bin/arm ] && ln -sf linux-arm bin/arm
chmod 644 %{SOURCE2} # silence an rpmlint non-issue

# binaries
install -d %{buildroot}%{_sbindir}
install -p -m 755 bin/%{_arch}/%{name}-server %{buildroot}%{_sbindir}
install -p -m 755 bin/%{_arch}/%{name}-cli %{buildroot}%{_sbindir}

# other shared files, public html, webpack
install -d %{buildroot}%{_datadir}/%{name}
cp -a conf public %{buildroot}%{_datadir}/%{name}

# man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# config files
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/sysconfig
%if 0%{?fedora} || 0%{?rhel}
# distro defaults
install -p conf/distro-defaults.ini \
    %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p conf/distro-defaults.ini \
    %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
%else
# grafana.com defaults
install -p conf/defaults.ini \
    %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p conf/defaults.ini \
    %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
%endif
install -p conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p packaging/rpm/sysconfig/grafana-server \
    %{buildroot}%{_sysconfdir}/sysconfig/grafana-server

# config database directory and plugins
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}/data
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}/data/plugins

# log directory
install -d %{buildroot}%{_localstatedir}/log/%{name}

# systemd service files
install -d %{buildroot}%{_unitdir} # only needed for manual rpmbuilds
install -p -m 644 packaging/rpm/systemd/grafana-server.service \
    %{buildroot}%{_unitdir}

# daemon run pid file config for using tmpfs
install -d %{buildroot}%{_tmpfilesdir}
echo "d %{_rundir}/%{name} 0755 %{GRAFANA_USER} {%GRAFANA_GROUP} -" \
    > %{buildroot}%{_tmpfilesdir}/%{name}.conf

%pre
getent group %{GRAFANA_GROUP} >/dev/null || groupadd -r %{GRAFANA_GROUP}
getent passwd %{GRAFANA_USER} >/dev/null || \
    useradd -r -g %{GRAFANA_GROUP} -d %{GRAFANA_HOME} -s /sbin/nologin \
    -c "%{GRAFANA_USER} user account" %{GRAFANA_USER}
exit 0

%preun
%systemd_preun grafana-server.service

%post
%systemd_post grafana-server.service

%postun
%systemd_postun_with_restart grafana-server.service


%files
# binaries
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli

# config files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(0640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/grafana.ini
%config(noreplace) %attr(0640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/ldap.toml
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# config database directory and plugins (actual db files are created by grafana-server)
%dir %{_sharedstatedir}/%{name}
%attr(-, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %{_sharedstatedir}/%{name}/data

# shared directory and all files therein
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/public
%dir %{_datadir}/%{name}/conf
%attr(-, root, %{GRAFANA_GROUP}) %{_datadir}/%{name}/conf/*

# systemd service file
%{_unitdir}/grafana-server.service

# log directory - grafana.log is created by grafana-server, and it does it's own log rotation
%attr(0755, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_localstatedir}/log/%{name}

# man pages for grafana binaries
%{_mandir}/man1/%{name}-server.1*
%{_mandir}/man1/%{name}-cli.1*

# other docs and license
%license LICENSE.md
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md NOTICE.md
%doc PLUGIN_DEV.md README.md ROADMAP.md UPGRADING_DEPENDENCIES.md

%changelog
* Thu Mar 07 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.1-1
- update to v6.0.1 upstream sources, tweak distro config, re-do patch
- simplify make_webpack.sh script (Elliott Sales de Andrade)
- vendor/github.com/go-ldap is now gone, so don't unbundle it

* Thu Mar 07 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-11
- tweak after latest feedback, bump to 5.4.3-11 (BZ 1670656)
- build debuginfo package again
- unbundle BuildRequires for golang-github-hashicorp-version-devel
- remove some unneeded development files
- remove macros from changelog and other rpmlint tweaks

* Fri Feb 22 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-10
- tweak spec for available and unavailable (bundled) golang packages

* Wed Feb 20 2019 Xavier Bachelot <xavier@bachelot.org> 5.4.3-9
- Remove extraneous slash (cosmetic)
- Create directories just before moving stuff in them
- Truncate long lines
- Group all golang stuff
- Simplify BuildRequires/bundled Provides
- Sort BuildRequires/bundled Provides
- Fix bundled go packages Provides

* Fri Feb 15 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-8
- add BuildRequires (and unbundle) vendor sources available in Fedora
- declare Provides for remaining (bundled) vendor go sources
- do not attempt to unbundle anything on RHEL < 7 or Fedora < 28

* Thu Feb 07 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-7
- further refinement for spec doc section from Xavier Bachelot
- disable debug_package to avoid empty debugsourcefiles.list

* Wed Feb 06 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-6
- further refinement following review by Xavier Bachelot

* Tue Feb 05 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-5
- further refinement following review by Xavier Bachelot

* Fri Feb 01 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-4
- further spec updates after packaging review
- reworked post-install scriplets

* Thu Jan 31 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-3
- tweak FHS patch, update spec after packaging review

* Wed Jan 30 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-2
- add patch to be standard FHS compliant, remove phantomjs
- update to v5.4.3 upstream community sources

* Wed Jan 09 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.2-1
- update to v5.4.2 upstream community sources

* Thu Oct 18 2018 Mark Goodwin <mgoodwin@redhat.com> 5.3.1-1
- update to v5.3.1 upstream community sources

* Tue Oct 02 2018 Mark Goodwin <mgoodwin@redhat.com> 5.2.5-1
- native RPM spec build with current tagged v5.2.5 sources
