%define    mysql_user	  mysql
%define	   mysql_prefix	  /usr/local/mysql

Name:	        mysql
Version:	5.6.26
Release:	1%{?dist}
Summary:        MySQL: a very fast and reliable SQL database server.
Group:	        Applications/Databases
Vendor:	        yichao.chen
Packager:	YiChao Chen <cycxhen@hotmail.com>

License:	GPL
URL:	        http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.26.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gcc,binutils,make,automake,ncurses-devel,libxml2-devel,libmcrypt-devel,libtool-ltdl-devel,cmake
Requires:	bison,libmcrypt,ncurses
Requires(pre):	shadow-utils
Requires(postun):	initscripts,chkconfig
Provides:	SQL database server

Source0:	http://dev.mysql.com/get/Downloads/MySQL-5.6/%{name}-%{version}.tar.gz  
Source1:	mysql_default.cnf
Source2:        mysqld_init.sh

%description
    The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
%{mysql_vendor}

    The MySQL software has Dual Licensing, which means you can use the MySQL
software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from %{mysql_vendor} if you do not wish to be bound by the terms of
the GPL. See the chapter "Licensing and Support" in the manual for
further info.

    The MySQL web site (http://www.mysql.com/) provides the latest
news and information about the MySQL software. Also please see the
documentation and the manual for more information.

%prep
%setup -q

%build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{mysql_prefix}  \
    -DMYSQL_DATADIR=%{mysql_prefix}/data    \
    -DWITH_INNOBASE_STORAGE_ENGINE=1   \
    -DDEFAULT_CHARSET=utf8  \
    -DDEFAULT_COLLATION=utf8_general_ci  \
    -DENABLED_LOCAL_INFILE=1  \
    -DMYSQL_TCP_PORT=3306  \
    -DMYSQL_UNIX_ADDR=/var/run/mysql/mysql.sock \
    -DWITH_DEBUG=0   \
    -DWITH_EXTRA_CHARSETS=all  \
    -DWITH_SSL=system  \
    -DENABLE_DOWNLOADS=1

make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}


%{__install} -p -d -m 0755 %{buildroot}/var/run/mysql
%{__install} -p -d -m 0755 %{buildroot}/var/log/mysql
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}/usr/local/mysql/my.cnf
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}/etc/rc.d/init.d/mysqld

%clean
rm -rf %{buildroot}

%pre
if [ $1 == 1 ];then
	/usr/sbin/useradd -s /sbin/nologin -r %{mysql_user} 2>/dev/null || :
fi

%post
if [ $1 == 1 ];then
        export PATH=$PATH:/usr/local/mysql/bin
        /usr/local/mysql/scripts/mysql_install_db --user=%{mysql_user} --basedir=%{mysql_prefix} --datadir=%{mysql_prefix}/data >/dev/null 2>&1
	/sbin/chkconfig --add %{name}d
        /bin/chown -R mysql:mysql /var/run/mysql/
        /bin/chown -R mysql:mysql /var/log/mysql/
        /bin/chown -R mysql:mysql /usr/local/mysql/
fi

%preun
if [ $1 == 0 ];then
	/sbin/service %{name}d stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}d
	userdel %{mysql_user}
fi

%files
%defattr(-,root,root,-)
#%doc LICENSE CHANGES README
%{mysql_prefix}
%dir	/var/run/%{name}
%dir	/var/log/%{name}
%config(noreplace)	%{mysql_prefix}/my.cnf

%attr(0755,root,root)	%{_initrddir}/%{name}d

%changelog
* Mon Aug 14 2015 Yichao Chen <cycxhen@hotmail.com> -5.6.26-1
- Initial version
#End
