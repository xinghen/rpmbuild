%define nginx_user	nginx
%define	nginx_group	%{nginx_user}
%define	nginx_prefix	/usr/local/nginx

Name:	nginx
Version:	1.6.2
Release:	1%{?dist}
Summary:	   Nginx is an open source reverse proxy server for HTTP,HTTPS,SMTP,POP3,and IMAP protocols,as well as a load balancer,cache,and a web server.
Group:	Applications/Internet
Vendor:	 yichao.chen
Packager:	yichao.chen(cycxhen@hotmail.com)

License:	BSD
URL:	http://nginx.org/download/nginx-1.6.2.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gcc,binutils,zlib,zlib-devel,openssl-devel
Requires:	pcre,openssl,gd
Requires(pre):	shadow-utils
Requires(postun):	initscripts
Provides:	web server

Source:  

%description
Nginx (pronounced "engine-x") is an open source reverse proxy server for HTTP, HTTPS, SMTP, POP3, and IMAP protocols, as well as a load balancer, HTTP cache, and a web server (origin server). The nginx project started with a strong focus on high concurrency, high performance and low memory usage. It is licensed under the 2-clause BSD-like license and it runs on Linux, BSD variants, Mac OS X, Solaris, AIX, HP-UX, as well as on other *nix flavors.[7] It also has a proof of concept port for Microsoft Windows.

%prep
%setup -q

%build
./configure  --prefix=%{nginx_prefix}  --user=%{nginx_user}  --group=%{nginx_group}  --with-http_ssl_module  --with-http_realip_module  --with-http_xslt_module  --with-http_sub_module  --with-http_dav_module  --with-http_flv_module  --with-http_gzip_static_module   --with-http_stub_status_module  --with-http_perl_module  --with-mail  --with-mail_ssl_module  --with-http_mp4_module  --http-proxy-temp-path=/usr/local/nginx/proxy  --http-fastcgi-temp-path=/usr/local/nginx/fcgi --http-client-body-temp-path=/usr/local/nginx/client --http-uwsgi-temp-path=/usr/local/nginx/uwsgi --http-scgi-temp-path=/usr/local/nginx/scgi
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESDIR="%{buildroot}"

%{__install} -p -d -m 0755 %{buildroot}/var/run/nginx
%{__install} -p -d -m 0755 %{buildroot}/var/log/nginx

%clean
rm -rf %{buildroot}

%pre
if [ $1 == 1 ];then
	/usr/sbin/useradd -s /sbin/nologin -r nginx 2>/dev/null || :
fi

%post
if [ $1 == 1 ];then
	/sbin/chkconfig --add %{name}

%preun
if [ $1 == 0 ];then
	/sbin/service %{name} stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}
	userdel nginx
fi

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README
/usr/local/nginx/sbin/nginx
%dir	/var/run/nginx
%dir	/var/log/nginx
%dir	/etc/nginx
%config(noreplace)	/usr/local/nginx/conf/%{name}.conf
/usr/local/nginx/html/50x.html
/usr/local/nginx/html/index.html
%attr(0755,root,root)	%{_initrddir}/%{name}

%changelog
* Wed Nov 26 2014 Chen YiChao	<cycxhen@hotmail.com> -1.7-1
-Initial version
#End
