%define		kdeframever	5.13
%define		qtver		5.3.2
%define		kfname		kwindowsystem

Summary:	Access to the windowing system
Name:		kf5-%{kfname}
Version:	5.13.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	a907421be1461569667ffdd0f7bfae63
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	pkgconfig
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Convenience access to certain properties and features of the windowing
system.

KWindowSystem provides information about the windowing system and
allows interaction with the windowing system. It provides an high
level API which is windowing system independent and has platform
specific implementations. This API is inspired by X11 and thus not all
functionality is available on all windowing systems.

In addition to the high level API, this framework also provides
several more low level classes for interaction with the X Windowing
System.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{kfname}5_qt --with-qm --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %ghost %{_libdir}/libKF5WindowSystem.so.5
%attr(755,root,root) %{_libdir}/libKF5WindowSystem.so.*.*
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/org.kde.kwindowsystem.platforms/KF5WindowSystemWaylandPlugin.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/org.kde.kwindowsystem.platforms/KF5WindowSystemX11Plugin.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KWindowSystem
%{_includedir}/KF5/kwindowsystem_version.h
%{_libdir}/cmake/KF5WindowSystem
%{_libdir}/libKF5WindowSystem.so
%{qt5dir}/mkspecs/modules/qt_KWindowSystem.pri
