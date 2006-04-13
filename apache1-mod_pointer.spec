# TODO
# - apache config
# - package split by backend
%define		mod_name	pointer
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module for making domain redirects
Name:		apache1-mod_%{mod_name}
Version:	0.8
Release:	0.6
License:	Apache
Group:		Networking/Daemons
Source0:	http://stderr.net/mod_pointer/dist/mod_pointer-%{version}.tar.gz
# Source0-md5:	2f6529c49f1d10ecd06d3f6bc8503a5f
Patch0:		apache1-mod_pointer-mysql.patch
URL:		http://stderr.net/mod_pointer/
BuildRequires:	apache1-devel >= 1.3.34-8.5
BuildRequires:	gdbm-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_pointer is an Apache module for making domain redirects easy - the
known service of many hosting providers that lets a domain point to
your webpage on another server.

The configuration part of the mappings are handled in either a MySQL
or Postgresql database or a NDBM or SDBM db file, so it's easy to
build a webbased interface for letting users change it on their own.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{__make} all \
	WITH_APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

%{__make} install \
	APXS="%{apxs} -S DESTDIR=$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES SUPPORT TODO frameset.html *.sql *.readme pointer.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
