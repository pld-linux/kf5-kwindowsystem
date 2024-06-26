#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.116
%define		qtver		5.15.2
%define		kfname		kwindowsystem

Summary:	Access to the windowing system
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	256a82dca3a4352d97f0fb40e957567c
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xcb-util-wm-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xz
Requires:	Qt5Gui >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	Qt5X11Extras >= %{qtver}
Requires:	kf5-dirs
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
Requires:	Qt5Widgets-devel >= %{qtver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5WindowSystem.so.5
%attr(755,root,root) %{_libdir}/libKF5WindowSystem.so.*.*
%dir %{_libdir}/qt5/plugins/kf5/kwindowsystem
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kwindowsystem/KF5WindowSystemX11Plugin.so
%{_datadir}/qlogging-categories5/kwindowsystem.renamecategories
%{_datadir}/qlogging-categories5/kwindowsystem.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KWindowSystem
%{_libdir}/cmake/KF5WindowSystem
%{_libdir}/libKF5WindowSystem.so
%{qt5dir}/mkspecs/modules/qt_KWindowSystem.pri
