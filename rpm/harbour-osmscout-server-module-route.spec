# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       harbour-osmscout-server-module-route

# >> macros
%define __provides_exclude_from ^%{_datadir}/.*$
%define __requires_exclude ^libboost_|libicudata|libicui18n|libicuuc|libprime_server|libzmq|libczmq|libprotobuf|libcurl|libz|liblz4.*$
# << macros

%{!?qtc_qmake:%define qtc_qmake %qmake}
%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}
%{?qtc_builddir:%define _builddir %qtc_builddir}
Summary:    OSM Scout Server Module Route
Version:    2.4.8
Release:    1
Group:      Qt/Qt
License:    LGPL3
URL:        https://github.com/rinigus/osmscout-server
Source0:    %{name}-%{version}.tar.bz2
Source100:  harbour-osmscout-server-module-route.yaml
Source101:  harbour-osmscout-server-module-route-rpmlintrc
Requires:   sailfishsilica-qt5 >= 0.10.9
BuildRequires:  pkgconfig(sailfishapp) >= 1.0.2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  libzmq-devel >= 4.1.4
BuildRequires:  czmq-devel >= 3.0
BuildRequires:  protobuf-devel
BuildRequires:  prime_server-devel == 0.6.3
BuildRequires:  valhalla == 2.4.8
BuildRequires:  valhalla-devel == 2.4.8
BuildRequires:  boost-devel >= 1.51
BuildRequires:  boost-chrono >= 1.51
BuildRequires:  boost-date-time >= 1.51
BuildRequires:  boost-filesystem >= 1.51
BuildRequires:  boost-iostreams >= 1.51
BuildRequires:  boost-program-options >= 1.51
BuildRequires:  boost-regex >= 1.51
BuildRequires:  boost-system >= 1.51
BuildRequires:  boost-thread >= 1.51
BuildRequires:  lz4-devel
BuildRequires:  zlib-devel
BuildRequires:  libcurl-devel
BuildRequires:  desktop-file-utils

%description
This is a module for OSM Scout Server providing Valhalla routing engine


%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
# << build pre

%qtc_qmake5  \
    VERSION='%{version}-%{release}'

%qtc_make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%qmake5_install

# >> install post
################################

# ship all shared libraries not allowed in Harbour with the app
mkdir -p %{buildroot}%{_datadir}/%{name}/lib

cp /usr/lib/libboost_filesystem-mt.so.1.51.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libboost_regex-mt.so.1.51.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libboost_system-mt.so.1.51.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libboost_thread-mt.so.1.51.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libboost_program_options-mt.so.1.51.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libboost_iostreams-mt.so.1.51.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libboost_chrono-mt.so.1.51.0 %{buildroot}%{_datadir}/%{name}/lib

cp /usr/lib/libprime_server.so.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libczmq.so.4  %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libzmq.so.5  %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libprotobuf.so.8  %{buildroot}%{_datadir}/%{name}/lib

cp /usr/lib/libicui18n.so.52 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libicudata.so.52 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libicuuc.so.52 %{buildroot}%{_datadir}/%{name}/lib

cp /usr/lib/liblz4.so.1.8.1 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/liblz4.so.1 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libz.so.1.2.8 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libz.so.1 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libcurl.so.4.4.0 %{buildroot}%{_datadir}/%{name}/lib
cp /usr/lib/libcurl.so.4 %{buildroot}%{_datadir}/%{name}/lib

strip %{buildroot}%{_datadir}/%{name}/lib/libicudata.so.52

# strip executable bit from all libraries
chmod -x %{buildroot}%{_datadir}/%{name}/lib/*.so*

################################
# << install post

desktop-file-install --delete-original       \
  --dir %{buildroot}%{_datadir}/applications             \
   %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root,-)
%{_bindir}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
# >> files
# << files
