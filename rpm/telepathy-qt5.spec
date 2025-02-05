Name:       telepathy-qt5
Summary:    Qt 5 Telepathy library
Version:    0.9.8
Release:    1
License:    LGPLv2+
URL:        https://github.com/sailfishos/telepathy-qt
Source0:    %{name}-%{version}.tar.gz
Source1:    INSIGNIFICANT
Source2:    mktests.sh.in
Source3:    runDbusTest.sh.in
Source4:    runTest.sh.in

Patch0:     0001-Install-tests.patch
Patch1:     0002-Remove-assert-which-appears-invalid-for-conference-c.patch
Patch2:     0003-Use-python3-on-tests-accountmanager.patch
Patch3:     0004-Fix-build-with-glib-2.72.0-and-newer.patch
Patch4:     0005-Add-missing-include-to-glib-tests.patch

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(farstream-0.2)
BuildRequires:  pkgconfig(telepathy-glib) >= 0.18.0
BuildRequires:  pkgconfig(telepathy-farstream) >= 0.4.0
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  python3-base
BuildRequires:  dbus-python3
BuildRequires:  doxygen
BuildRequires:  cmake

%description
Qt-based library for Telepathy components.


%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing applications
that use %{name}.


%package farstream
Summary:    Qt 5 Telepathy/Farstream integration
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description farstream
This package provides telepathy-qt5 integration with telepathy-farstream,
which implements media stream using gstreamer and Farstream.


%package farstream-devel
Summary:    Development files for telepathy-qt5-farstream
Requires:   %{name}-farstream = %{version}-%{release}
Requires:   telepathy-qt5-devel = %{version}
Requires:   telepathy-farstream-devel

%description farstream-devel
This package contains libraries and header files for developing applications
that use telepathy-qt5-farstream.


%package tests
Summary:    Automated tests for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   %{name} = %{version}

%description tests
This package contains automated tests and tests.xml


%prep
%autosetup -p1 -n %{name}-%{version}/telepathy-qt

%build
%__cp $RPM_SOURCE_DIR/INSIGNIFICANT tests/
%__cp $RPM_SOURCE_DIR/mktests.sh.in tests/
%__cp $RPM_SOURCE_DIR/runDbusTest.sh.in tests/
%__cp $RPM_SOURCE_DIR/runTest.sh.in tests/
%__chmod 0644 tests/INSIGNIFICANT
%__chmod 0755 tests/mktests.sh.in
%__chmod 0755 tests/runDbusTest.sh.in
%__chmod 0755 tests/runTest.sh.in


%cmake -DENABLE_TESTS=TRUE -DENABLE_FARSTREAM=TRUE -DENABLE_EXAMPLES=FALSE

%make_build

tests/mktests.sh > tests/tests.xml

%install
export QT_SELECT=5
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post farstream -p /sbin/ldconfig

%postun farstream -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/libtelepathy-qt5.so.*
%{_libdir}/libtelepathy-qt5-service.so.*

%files devel
%{_libdir}/libtelepathy-qt5.so
%{_libdir}/libtelepathy-qt5-service.so
%{_libdir}/pkgconfig/TelepathyQt5.pc
%{_includedir}/telepathy-qt5/TelepathyQt/*
%{_libdir}/cmake/TelepathyQt5/*.cmake
%{_libdir}/cmake/TelepathyQt5Service/TelepathyQt5ServiceConfig.cmake
%{_libdir}/cmake/TelepathyQt5Service/TelepathyQt5ServiceConfigVersion.cmake
%{_libdir}/pkgconfig/TelepathyQt5Service.pc

%files farstream
%{_libdir}/libtelepathy-qt5-farstream.so.*

%files farstream-devel
%{_libdir}/libtelepathy-qt5-farstream.so
%{_includedir}/telepathy-qt5/TelepathyQt/Farstream/*
%{_libdir}/cmake/TelepathyQt5Farstream/TelepathyQt5FarstreamConfig.cmake
%{_libdir}/cmake/TelepathyQt5Farstream/TelepathyQt5FarstreamConfigVersion.cmake
%{_libdir}/pkgconfig/TelepathyQt5Farstream.pc

%files tests
/opt/tests/%{name}/*

