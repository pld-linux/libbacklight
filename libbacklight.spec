#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Linux backlight interface library
Summary(pl.UTF-8):	Biblioteka interfejsu do podświetlania pod Linuksem
Name:		libbacklight
Version:	0.01
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://www.freedesktop.org/software/libbacklight/%{name}-%{version}.tar.gz
# Source0-md5:	a04ae7354b0b0176326914e772dbdf11
Patch0:		%{name}-drm.patch
URL:		http://cgit.freedesktop.org/libbacklight/
BuildRequires:	libdrm-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libpciaccess-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libbacklight provides an abstraction layer that allows applications to
identify the appropriate Linux backlight device for their use.

%description -l pl.UTF-8
Biblioteka libbacklight udostępnia warstwę abstrakcji pozwalającą
aplikacjom zidentyfikować właściwe urządzenie podświetlające pod
Linuksem.

%package devel
Summary:	Header files for libbacklight library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbacklight
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xorg-lib-libpciaccess-devel

%description devel
Header files for libbacklight library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbacklight.

%package static
Summary:	Static libbacklight library
Summary(pl.UTF-8):	Statyczna biblioteka libbacklight
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbacklight library.

%description static -l pl.UTF-8
Statyczna biblioteka libbacklight.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libbacklight.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbacklight.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbacklight.so
%{_includedir}/libbacklight.h
%{_pkgconfigdir}/libbacklight.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbacklight.a
%endif
