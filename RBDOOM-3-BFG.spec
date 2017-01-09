%global commit0 80df3182f1db17c282306f4095a75637db86f484
%global date 20161018
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           RBDOOM-3-BFG
Version:        1.1.0
Release:        4%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Robert Beckebans' Doom 3 BFG engine
License:        GPLv3+ with exceptions
URL:            https://github.com/RobertBeckebans/%{name}

Source0:        https://github.com/RobertBeckebans/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:        %{name}-README.txt
Patch1:         %{name}-noexit.patch
Patch2:         %{name}-png.patch
Patch3:         %{name}-minizip.patch
Patch4:         %{name}-README.patch

# Generic provider for Doom 3 BFG engine based games
Provides:       doom3bfg-engine = 1.1401

# Contains a very old and unknown version of timidity to play audio in original
# Doom I & II.
Provides:       bundled(timidity) = 0.2i

BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  ffmpeg-devel
BuildRequires:  glew-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  minizip-devel
BuildRequires:  openal-soft-devel
BuildRequires:  zlib-devel
BuildRequires:  SDL2-devel

%description
%{name} is a Doom 3 BFG GPL source modification. The goal of %{name}
is to bring Doom 3 BFG with the help of SDL to all suitable platforms. Bugs
present in the original DOOM 3 will be fixed (when identified) without altering
the original game-play.

%prep
%setup -qn %{name}-%{commit0}
%patch1 -p1

# Remove bundled libraries
rm -fr neo/libs/{glew,jpeg-6,openal-soft,ffmpeg*,png,zlib}
%patch2 -p1
%patch3 -p1
%patch4 -p1

cp %{SOURCE1} ./Fedora-README.txt

iconv -f iso8859-1 -t utf-8 COPYING.txt > COPYING.txt.conv && mv -f COPYING.txt.conv COPYING.txt

# Disable level selection menu
echo "#define ID_RETAIL" >> neo/framework/Licensee.h

%build
LDFLAGS='-lpthread'
# Passing a fake build name avoids default CMAKE_BUILD_TYPE="RelWithDebInfo"
# which has hard coded GCC optimizations.
%cmake \
    -DCMAKE_BUILD_TYPE=Fedora \
    -DFFMPEG=ON \
    -DOPENAL=ON \
    -DUSE_PRECOMPILED_HEADERS=OFF \
    -DUSE_SYSTEM_LIBGLEW=ON \
    -DUSE_SYSTEM_LIBJPEG=ON \
    -DUSE_SYSTEM_LIBPNG=ON \
    -DUSE_SYSTEM_ZLIB=ON \
    neo
make %{?_smp_mflags}

%post
/usr/sbin/alternatives --install %{_bindir}/doom3bfg-engine doom3bfg-engine %{_bindir}/RBDoom3BFG 10

%preun
if [ "$1" = 0 ]; then
    /usr/sbin/alternatives --remove doom3bfg-engine %{_bindir}/RBDoom3BFG
fi

%install
# The library is loaded at runtime only and is expected with exactly this name;
# so no ldconfig for it; much like a plugin. We can also then remove RPATH from
# the main binary.
install -D -p -m 0755 RBDoom3BFG %{buildroot}%{_bindir}/RBDoom3BFG
install -D -p -m 0755 idlib/libidlib.so %{buildroot}%{_libdir}/libidlib.so
chrpath --delete %{buildroot}%{_bindir}/RBDoom3BFG

%files
%{!?_licensedir:%global license %%doc}
%license COPYING.txt
%doc Fedora-README.txt README.txt
%{_bindir}/RBDoom3BFG
%{_libdir}/libidlib.so

%changelog
* Mon Jan 09 2017 Simone Caronni <negativo17@gmail.com> - 1.1.0-4.20161018git80df318
- Update to latest snapshot.
- Set snapshot release as per packaging guidelines.

* Mon Jun 13 2016 Simone Caronni <negativo17@gmail.com> - 1.1.0-3.a884b08
- Update to latest sources.

* Sat Feb 27 2016 Simone Caronni <negativo17@gmail.com> - 1.1.0-2.7728dc3
- Update to latest sources.

* Sat Jan 23 2016 Simone Caronni <negativo17@gmail.com> - 1.1.0-1.1275984
- Update to snapshot of 1.1.0.
- Update SPEC file for recent packaging guidelines and add license macro.
- Drop RHEL 6 support.
- Update Fedora README file.
- Further cleanup bundled libraries (minizip), it also simplifies building.

* Thu Jun 25 2015 Simone Caronni <negativo17@gmail.com> - 1.0.3-3.git.223548d
- Update to latest snapshot, disables usage of precompiled headers.
- Fix Source0 url.

* Sat Apr 18 2015 Simone Caronni <negativo17@gmail.com> - 1.0.3-2.git.a60f92b
- Update to latest snapshot and disable development menu.

* Wed Mar 25 2015 Simone Caronni <negativo17@gmail.com> - 1.0.3-1.git.395ef52
- Update to 1.0.3 snapshot.

* Thu Jan 15 2015 Simone Caronni <negativo17@gmail.com> - 1.0.2-2.git.e7817d7
- Update to latest snapshot.
- System libraries can now be used instead of bundled ones!
- Add compatibility patch for newer libpng versions.

* Mon May 12 2014 Simone Caronni <negativo17@gmail.com> - 1.0.2-1.git.7087d56
- First build.
- Add Fedora-README.txt file.
- Add note on idlib.so.
- Use CMake 2.8 on RHEL/CentOS 6.
- Use SDL2 on Fedora 19+ and RHEL/CentOS 7+.
- Removed bundled zlib, jpeg, openal, glew, libpng, ffmpeg.
