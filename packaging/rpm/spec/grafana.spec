Name:             grafana
Version:          5.4.3
Release:          2%{?dist}
Summary:          Grafana is an open source, feature rich metrics dashboard and graph editor
License:          ASL 2.0
URL:              https://grafana.org

# Source0 is the tagged upstream sources
Source0:          grafana-%{?version}.src.tar.gz

# Source1 contains the front-end javascript modules bundled into a webpack
Source1:          grafana_webpack-%{?version}.src.tar.gz

# Fedora/FSH and config patch
Patch0:           000-grafana-fedora.patch

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

BuildRequires:    tar systemd golang

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -T -D -a 0 -c -n src/github.com/grafana
%setup -q -T -D -a 1 -c -n src/github.com/grafana
%patch0 -p1 -d %{_builddir}/src/github.com/grafana/grafana

%build
# server-side binaries: grafana-server and grafana-cli
export GOPATH=%{_builddir}
cd %{_builddir}/src/github.com/grafana/grafana
go run build.go build

%install
cd %{_builddir}/src/github.com/grafana/grafana

# fix up arch bin directories
[ ! -d bin/x86_64 ] && ln -sf linux-amd64 bin/x86_64
[ ! -d bin/i386 ] && ln -sf linux-386 bin/i386
[ ! -d bin/ppc64le ] && ln -sf linux-ppc64le bin/ppc64le
[ ! -d bin/arm ] && ln -sf linux-arm bin/arm

# set up buildroot directories
install -d -p %{buildroot}/%{_datadir}/%{name}
install -d -p %{buildroot}/%{_sharedstatedir}/%{name}
install -d -p %{buildroot}/%{_localstatedir}/log/%{name}
install -d -p %{buildroot}/%{_datadir}/doc/%{name}
install -d -p %{buildroot}/%{_sysconfdir}/%{name}
install -d -p %{buildroot}/%{_sysconfdir}/sysconfig
install -d -p %{buildroot}/%{_sbindir}
install -d -p %{buildroot}/%{_bindir}
install -d -p %{buildroot}/%{_sharedstatedir}/%{name}/data
install -d -p %{buildroot}/%{_rundir}/%{name}
install -d -p %{buildroot}/%{_unitdir}

# binaries
install -m 755 bin/%{_arch}/%{name}-server %{buildroot}/%{_sbindir}
install -m 755 bin/%{_arch}/%{name}-cli %{buildroot}/%{_sbindir}

# shared files, including docs, public html, webpack and scripts
install -m 644 docs/VERSION *.md %{buildroot}/%{_datadir}/doc/%{name}
cp -rpa docs conf public scripts %{buildroot}/%{_datadir}/%{name}

# config files
install -m 644 conf/defaults.ini %{buildroot}/%{_sysconfdir}/%{name}/grafana.ini
install -m 644 conf/ldap.toml %{buildroot}/%{_sysconfdir}/%{name}/ldap.toml
install -p -m 0644 packaging/rpm/sysconfig/grafana-server %{buildroot}/%{_sysconfdir}/sysconfig/grafana-server

# systemd service files
install -p -m 0644 packaging/rpm/systemd/grafana-server.service %{buildroot}/%{_unitdir}


%files
%defattr(-,root,root,-)
# binaries
%attr(0755, root, root) %{_sbindir}/%{name}-server
%attr(0755, root, root) %{_sbindir}/%{name}-cli

# config files
%attr(0755, root, grafana) %dir %{_sysconfdir}/%{name}
%attr(0640, root, grafana) %{_sysconfdir}/%{name}/grafana.ini
%attr(0640, root, grafana) %{_sysconfdir}/%{name}/ldap.toml
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/sysconfig/grafana-server

# run file directory
%attr(0755, grafana, grafana) %dir %{_rundir}/%{name}

# config database directory
%attr(0755, grafana, grafana) %dir %{_sharedstatedir}/%{name}
%attr(0755, grafana, grafana) %dir %{_sharedstatedir}/%{name}/data

# shared state directory and all files therein
%attr(0755, grafana, grafana) %{_datadir}/%{name}

# systemd service file
%config(noreplace) %attr(-, root, root) %{_unitdir}/grafana-server.service

# log directory
%attr(0755, grafana, grafana) %dir %{_localstatedir}/log/%{name}

# shared docs
%exclude %{_datadir}/%{name}/docs
%attr(-, root, root) %doc %{_datadir}/doc/%{name}/*.md
%attr(-, root, root) %doc %{_datadir}/doc/%{name}/VERSION

%posttrans
#!/bin/sh

set -e

echo "POSTTRANS: Running script"

[ -f /etc/sysconfig/grafana-server ] && . /etc/sysconfig/grafana-server

# copy config files if missing
if [ ! -f /etc/grafana/grafana.ini ]; then
  echo "POSTTRANS: Config file not found"

  if [ -f /etc/grafana/grafana.ini.rpmsave ]; then
    echo "POSTTRANS: /etc/grafana/grafana.ini.rpmsave config file found."
    mv /etc/grafana/grafana.ini.rpmsave /etc/grafana/grafana.ini
    echo "POSTTRANS: /etc/grafana/grafana.ini restored"

    if [ -f /etc/grafana/ldap.toml.rpmsave ]; then
      echo "POSTTRANS: /etc/grafana/ldap.toml.rpmsave found"
      mv /etc/grafana/ldap.toml.rpmsave /etc/grafana/ldap.toml
      echo "POSTTRANS: /etc/grafana/ldap.toml restored"
    fi

    echo "POSTTRANS: Restoring config file permissions"
    chown -Rh root:$GRAFANA_GROUP /etc/grafana/*
    chmod 755 /etc/grafana
    find /etc/grafana -type f -exec chmod 640 {} ';'
    find /etc/grafana -type d -exec chmod 755 {} ';'
  fi
  chown $GRAFANA_USER /usr/share/grafana/data
  chmod 755 /usr/share/grafana/data
fi

%post
#!/bin/sh

set -e

[ -f /etc/sysconfig/grafana-server ] && . /etc/sysconfig/grafana-server

startGrafana() {
  if [ -x /bin/systemctl ] ; then
                /bin/systemctl daemon-reload
                /bin/systemctl start grafana-server.service
        elif [ -x /etc/init.d/grafana-server ] ; then
                /etc/init.d/grafana-server start
        elif [ -x /etc/rc.d/init.d/grafana-server ] ; then
                /etc/rc.d/init.d/grafana-server start
        fi
}

stopGrafana() {
        if [ -x /bin/systemctl ] ; then
                /bin/systemctl stop grafana-server.service > /dev/null 2>&1 || :
        elif [ -x /etc/init.d/grafana-service ] ; then
                /etc/init.d/grafana-service stop
        elif [ -x /etc/rc.d/init.d/grafana-service ] ; then
                /etc/rc.d/init.d/grafana-service stop
        fi
}


# Initial installation: $1 == 1
# Upgrade: $1 == 2, and configured to restart on upgrade
if [ $1 -eq 1 ] ; then
        [ -z "$GRAFANA_USER" ] && GRAFANA_USER="grafana"
        [ -z "$GRAFANA_GROUP" ] && GRAFANA_GROUP="grafana"
        if ! getent group "$GRAFANA_GROUP" > /dev/null 2>&1 ; then
    groupadd -r "$GRAFANA_GROUP"
        fi
        if ! getent passwd "$GRAFANA_USER" > /dev/null 2>&1 ; then
    useradd -r -g grafana -d /usr/share/grafana -s /sbin/nologin \
    -c "grafana user" grafana
        fi

  # copy user config files
  if [ ! -f $CONF_FILE ]; then
    cp /usr/share/grafana/conf/sample.ini $CONF_FILE
    cp /usr/share/grafana/conf/ldap.toml /etc/grafana/ldap.toml
  fi

  if [ ! -f $PROVISIONING_CFG_DIR ]; then
    mkdir -p $PROVISIONING_CFG_DIR/dashboards $PROVISIONING_CFG_DIR/datasources
    cp /usr/share/grafana/conf/provisioning/dashboards/sample.yaml $PROVISIONING_CFG_DIR/dashboards/sample.yaml
    cp /usr/share/grafana/conf/provisioning/datasources/sample.yaml $PROVISIONING_CFG_DIR/datasources/sample.yaml
  fi 

  # Set user permissions on /var/log/grafana, /var/lib/grafana and /usr/share/grafana/data
  mkdir -p /var/log/grafana /var/lib/grafana /usr/share/grafana/data
  chown -R $GRAFANA_USER:$GRAFANA_GROUP /var/log/grafana /var/lib/grafana /usr/share/grafana/data
  chmod 755 /var/log/grafana /var/lib/grafana /usr/share/grafana/data

  # configuration files should not be modifiable by grafana user, as this can be a security issue
  chown -Rh root:$GRAFANA_GROUP /etc/grafana/*
  chmod 755 /etc/grafana
  find /etc/grafana -type f -exec chmod 640 {} ';'
  find /etc/grafana -type d -exec chmod 755 {} ';'

  if [ -x /bin/systemctl ] ; then
    echo "### NOT starting on installation, please execute the following statements to configure grafana to start automatically using systemd"
    echo " sudo /bin/systemctl daemon-reload"
    echo " sudo /bin/systemctl enable grafana-server.service"
    echo "### You can start grafana-server by executing"
    echo " sudo /bin/systemctl start grafana-server.service"
  elif [ -x /sbin/chkconfig ] ; then
    echo "### NOT starting grafana-server by default on bootup, please execute"
    echo " sudo /sbin/chkconfig --add grafana-server"
    echo "### In order to start grafana-server, execute"
    echo " sudo service grafana-server start"
  fi
elif [ $1 -ge 2 ] ; then
  if [ "$RESTART_ON_UPGRADE" == "true" ]; then
    stopGrafana
    startGrafana
  fi
fi

%changelog
* Wed Jan 30 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-2
- add patch to be standard FSH compliant, remove phantomjs
- update to v5.4.3 upstream community sources
* Wed Jan 09 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.2-1
- update to v5.4.2 upstream community sources
* Thu Oct 18 2018 Mark Goodwin <mgoodwin@redhat.com> 5.3.1-1
- update to v5.3.1 upstream community sources
* Tue Oct 02 2018 Mark Goodwin <mgoodwin@redhat.com> 5.2.5-1
- native RPM spec build with current tagged v5.2.5 sources
