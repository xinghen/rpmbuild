%define nginx_user	nginx
%define	nginx_group	%{nginx_user}
%define	nginx_prefix	/usr/local/nginx

Name:	nginx
Version:	1.9.3
Release:	1%{?dist}
Summary:	   Nginx is an open source reverse proxy server for HTTP,HTTPS,SMTP,POP3,and IMAP protocols,as well as a load balancer,cache,and a web server.
Group:	Applications/Internet
Vendor:	 yichao.chen
Packager:	YiChao Chen <cycxhen@hotmail.com>

License:	BSD
URL:	http://nginx.org/download/nginx-1.9.3.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gcc,binutils,zlib-devel,openssl-devel,pcre-devel,make,automake,libxslt-devel,perl-ExtUtils-Embed,perl-devel
Requires:	pcre,openssl,zlib,libxml2,libxslt,perl
Requires(pre):	shadow-utils
Requires(postun):	initscripts,chkconfig
Provides:	Web Server/Proxy

Source0:	http://nginx.org/download/%{name}-%{version}.tar.gz  
Source1:	nginx.sysinit
Source2:        nginx.conf

%description
    Nginx (pronounced "engine-x") is an open source reverse proxy server for HTTP, HTTPS, SMTP, POP3, and IMAP protocols, as well as a load balancer, HTTP cache, and a web server (origin server). The nginx project started with a strong focus on high concurrency, high performance and low memory usage. It is licensed under the 2-clause BSD-like license and it runs on Linux, BSD variants, Mac OS X, Solaris, AIX, HP-UX, as well as on other *nix flavors.[7] It also has a proof of concept port for Microsoft Windows.

%prep
%setup -q

%build
export DESTDIR=%{buildroot}
./configure  \
    --prefix=%{nginx_prefix}  \
    --user=%{nginx_user}  \
    --group=%{nginx_group} \
    --with-http_ssl_module  \
    --with-http_realip_module  \
    --with-http_xslt_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_gzip_static_module \
    --with-http_stub_status_module \
    --with-http_perl_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-http_mp4_module \
    --http-proxy-temp-path=%{nginx_prefix}/proxy \
    --http-fastcgi-temp-path=%{nginx_prefix}/fcgi \
    --http-client-body-temp-path=%{nginx_prefix}/client \
    --http-uwsgi-temp-path=%{nginx_prefix}/uwsgi \
    --http-scgi-temp-path=%{nginx_prefix}/scgi \
    --with-pcre \
    --with-http_secure_link_module \
    --with-http_random_index_module \
    --with-file-aio
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}

%{__install} -p -d -m 0755 %{buildroot}/var/run/nginx
%{__install} -p -d -m 0755 %{buildroot}/var/log/nginx
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/nginx
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}/usr/local/nginx/conf/nginx.conf
%clean
rm -rf %{buildroot}

%pre
if [ $1 == 1 ];then
	/usr/sbin/useradd -s /sbin/nologin -r %{nginx_user} 2>/dev/null || :
fi

%post
if [ $1 == 1 ];then
	/sbin/chkconfig --add %{name}
fi

%preun
if [ $1 == 0 ];then
	/sbin/service %{name} stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}
	userdel %{nginx_user}
fi

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README
/usr/local/nginx/
%dir	/var/run/nginx
%dir	/var/log/nginx
%config(noreplace)	/usr/local/nginx/conf/%{name}.conf

/usr/lib64/perl5/perllocal.pod
/usr/local/lib64/perl5/auto/nginx/.packlist
/usr/local/lib64/perl5/auto/nginx/nginx.bs
/usr/local/lib64/perl5/auto/nginx/nginx.so
/usr/local/lib64/perl5/nginx.pm
/usr/local/share/man/man3/nginx.3pm


%attr(0755,root,root)	%{_initrddir}/%{name}
#%attr(0755,root,root)	/etc/rc.d/init.d/nginx

%changelog
* Mon Aug 10 2015 Yichao Chen <cycxhen@hotmail.com> -1.9.3-3
- Update nginx version to 1.9.3
* Wed Nov 26 2014 Chen Yichao	<cycxhen@hotmail.com> -1.6.2-2
- Add sysv script /etc/rc.d/init.d/nginx
- Update nginx version to 1.7.7
* Wed Nov 26 2014 Chen YiChao	<cycxhen@hotmail.com> -1.6.2-1
- Initial version
#End
