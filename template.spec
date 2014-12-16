%define 

Name:
Version:
Release:	1%{?dist}
Summary:
Group:	Applications/Internet
Vendor:	 yichao.chen
Packager:	YiChao Chen <cycxhen@hotmail.com>

License:	BSD
URL:	http://xxxx/xxxx/nginx-1.6.2.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:
Requires:
Requires(pre):
Requires(postun):
Provides:

Source0:	http://nginx.org/download/%{name}-%{version}.tar.gz  
Source1:	nginx.sysinit

%description

%prep
%setup -q

%build
./configure  --prefix=%{xxxxx}

make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESDIR="%{buildroot}"

%{__install} -p -d -m 0755 %{buildroot}/var/run/nginx
%{__install} -p -d -m 0755 %{buildroot}/var/log/nginx
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/nginx

%clean
rm -rf %{buildroot}

%pre
if [ $1 == 1 ];then
	/usr/sbin/useradd -s /sbin/nologin -r %{nginx_user} 2>/dev/null || :
fi

%post
if [ $1 == 1 ];then
	/sbin/chkconfig --add %{name}

%preun
if [ $1 == 0 ];then
	/sbin/service %{name} stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}
	userdel %{nginx_user}
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
%attr(0755,root,root)	/etc/rc.d/init.d/nginx

%changelog
* Wed Nov 26 2014 Chen Yichao	<cycxhen@hotmail.com> -1.6.2-2
- Add sysv script /etc/rc.d/init.d/nginx
- Update nginx version to 1.7.7
* Wed Nov 26 2014 Chen YiChao	<cycxhen@hotmail.com> -1.6.2-1
- Initial version
#End
