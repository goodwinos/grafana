Name:             grafana
Version:          5.4.3
Release:          8%{?dist}
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
%global           debug_package %{nil} # avoid empty debugsourcefiles.list

%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}
%global           GRAFANA_HOME %{_datadir}/%{name}

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

BuildRequires:    systemd golang

#
# golang build deps. These allow us to unbundle some vendor golang source.
# No unbundling for old Fedora / RHEL - just use the Grafana vendor src.
#
%if 0%{?fedora} >= 28 || 0%{?rhel} > 7
BuildRequires: golang-google-golangorg-cloud-devel
BuildRequires: golang-github-google-go-genproto-devel
BuildRequires: golang-github-grpc-grpc-go-devel
BuildRequires: golang-gopkg-yaml-devel-v2
BuildRequires: golang-github-aws-aws-sdk-go-devel
BuildRequires: golang-github-davecgh-go-spew-devel
BuildRequires: golang-github-patrickmn-go-cache-devel
BuildRequires: golang-github-golang-appengine-devel
BuildRequires: golang-gopkg-asn1-ber-1-devel
BuildRequires: golang-github-denisenkom-go-mssqldb-devel
BuildRequires: golang-github-go-ldap-ldap-devel
BuildRequires: golang-github-gorilla-websocket-devel
BuildRequires: golang-github-go-sql-driver-mysql-devel
BuildRequires: golang-github-hashicorp-go-hclog-devel
BuildRequires: golang-github-hashicorp-go-plugin-devel
BuildRequires: golang-github-lib-pq-devel
BuildRequires: golang-github-mattn-go-isatty-devel
%endif

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

# Declare bundled/vendor golang devel packages - not (yet) in Fedora
Provides: bundled(golang-github-benbjohnson-devel)
Provides: bundled(golang-github-codahale-devel)
Provides: bundled(golang-github-codegangsta-devel)
Provides: bundled(golang-github-facebookgo-devel)
Provides: bundled(golang-github-fatih-devel)
Provides: bundled(golang-github-golang-devel)
Provides: bundled(golang-github-go-macaron-devel)
Provides: bundled(golang-github-gosimple-devel)
Provides: bundled(golang-github-go-stack-devel)
Provides: bundled(golang-github-go-xorm-devel)
Provides: bundled(golang-github-grafana-devel)
Provides: bundled(golang-github-hashicorp-devel)
Provides: bundled(golang-github-inconshreveable-devel)
Provides: bundled(golang-github-klauspost-devel)
Provides: bundled(golang-github-mattn-devel)
Provides: bundled(golang-github-oklog-devel)
Provides: bundled(golang-github-opentracing-devel)
Provides: bundled(golang-github-rainycape-devel)
Provides: bundled(golang-github-teris-io-devel)
Provides: bundled(golang-github-uber-devel)
Provides: bundled(golang-github-Unknwon-devel)
Provides: bundled(golang-github-VividCortex-devel)
Provides: bundled(golang-github-yudai-devel)
Provides: bundled(golang-gopkg-alexcesaro-devel)
Provides: bundled(golang-gopkg-asn1-ber-v1-devel)
Provides: bundled(golang-gopkg-bufio-v1-devel)
Provides: bundled(golang-gopkg-ini-v1-devel)
Provides: bundled(golang-gopkg-macaron-v1-devel)
Provides: bundled(golang-gopkg-mail-v2-devel)
Provides: bundled(golang-gopkg-redis-v2-devel)
Provides: bundled(golang-gopkg-square-devel)
Provides: bundled(golang-gopkg-yaml-v2-devel)
Provides: bundled(golang-org-x-devel)

# Unstatisfied by BuildRequires on early RHEL / Fedora ONLY
%if 0%{?fedora} <= 27 || 0%{?rhel} <= 7
Provides: bundled(golang-google-golangorg-cloud-devel)
Provides: bundled(golang-github-google-go-genproto-devel)
Provides: bundled(golang-github-grpc-grpc-go-devel)
Provides: bundled(golang-gopkg-yaml-devel-v2)
Provides: bundled(golang-github-aws-aws-sdk-go-devel)
Provides: bundled(golang-github-davecgh-go-spew-devel)
Provides: bundled(golang-github-patrickmn-go-cache-devel)
Provides: bundled(golang-github-golang-appengine-devel)
Provides: bundled(golang-gopkg-asn1-ber-1-devel)
Provides: bundled(golang-github-denisenkom-go-mssqldb-devel)
Provides: bundled(golang-github-go-ldap-ldap-devel)
Provides: bundled(golang-github-gorilla-websocket-devel)
Provides: bundled(golang-github-go-sql-driver-mysql-devel)
Provides: bundled(golang-github-hashicorp-go-hclog-devel)
Provides: bundled(golang-github-hashicorp-go-plugin-devel)
Provides: bundled(golang-github-lib-pq-devel)
Provides: bundled(golang-github-mattn-go-isatty-devel)
%endif

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

%if 0%{?fedora} >= 28 || 0%{?rhel} > 7
# Unbundle grafana vendor/golang src (provided by BuildRequires),
# only on newer Fedora / RHEL.
rm -rf %{_builddir}/src/github.com/grafana/grafana/vendor/cloud.google.com
rm -rf %{_builddir}/src/github.com/grafana/grafana/vendor/google.golang.org
rm -rf { %{_builddir}/src/github.com/grafana/grafana/vendor/github.com/\
beorn7,bmizerany,bradfitz,BurntSushi,davecgh,denisenkom,go-ini,go-ldap,\
gopherjs,gorilla,go-sql-driver,jmespath,jtolds,kr,lib,matttproud,mitchellh,\
patrickmn,pkg,prometheus,sergi,smartystreets }
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

# Set up buildroot directories
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}
install -d %{buildroot}%{_datadir}/doc/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d -m 750 %{buildroot}%{_sharedstatedir}/%{name}/data
install -d -m 750 %{buildroot}%{_sharedstatedir}/%{name}/data/plugins
install -d %{buildroot}%{_rundir}/%{name}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_docdir}/%{name}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_defaultlicensedir}/%{name}
install -d %{buildroot}%{_unitdir} # only needed for manual rpmbuilds

# binaries
install -p -m 755 bin/%{_arch}/%{name}-server %{buildroot}%{_sbindir}
install -p -m 755 bin/%{_arch}/%{name}-cli %{buildroot}%{_sbindir}

# other shared files, public html, webpack
cp -a conf public %{buildroot}%{_datadir}/%{name}

# man pages
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# config files
%if 0%{?fedora} || 0%{?rhel}
# distro defaults
install -p -m 640 conf/distro-defaults.ini %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 640 conf/distro-defaults.ini %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
%else
# grafana.com defaults
install -p -m 640 conf/defaults.ini %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 640 conf/defaults.ini %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
%endif
install -p -m 640 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p -m 640 packaging/rpm/sysconfig/grafana-server %{buildroot}%{_sysconfdir}/sysconfig/grafana-server

# systemd service files
install -p -m 644 packaging/rpm/systemd/grafana-server.service %{buildroot}%{_unitdir}

# daemon run pid file config for using tmpfs
echo "d %{_rundir}/%{name} 0755 %{GRAFANA_USER} {%GRAFANA_GROUP} -" >%{buildroot}%{_tmpfilesdir}/%{name}.conf

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
* Fri Feb 15 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-8
- add BuildRequires (and unbundle) vendor sources available in Fedora
- declare Provides for remaining (bundled) vendor go sources
- do not attempt to unbundle anything on RHEL < 7 or Fedora < 28

* Thu Feb 07 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-7
- further refinement for %doc section from Xavier Bachelot
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
