#global tag %{version}
%global date 20230714

%global commit0 a51833e4edca5bd649e10b1367fd4990e64e2dd0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 1cbc9e9d16f997948c429739b1a1886fb4d0c796
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global commit2 799a918af94000d22828125d46aefd6ecd947e8d
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global commit3 0193e158bc9f4d17e3c3a61c9311a0439ed5572d
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global commit4 302302b30839505703d37fb82f536c53cf9172fa
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})

Name:           RBDOOM-3-BFG
Version:        1.5.1
Release:        4%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Robert Beckebans' Doom 3 BFG engine
License:        GPLv3+ with exceptions
URL:            https://github.com/RobertBeckebans/%{name}

%if 0%{?tag:1}
Source0:        https://github.com/RobertBeckebans/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        https://github.com/RobertBeckebans/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif
Source1:        https://github.com/RobertBeckebans/nvrhi/archive/%{commit1}.tar.gz#/nvrhi-%{shortcommit1}.tar.gz
Source2:        https://github.com/NVIDIAGameWorks/RTXMU/archive/%{commit2}.tar.gz#/RTXMU-%{shortcommit2}.tar.gz
Source3:        https://github.com/KhronosGroup/Vulkan-Headers/archive/%{commit3}.tar.gz#/Vulkan-Headers-%{shortcommit3}.tar.gz
Source4:        https://github.com/jarro2783/cxxopts/archive/%{commit4}.tar.gz#/cxxopts-%{shortcommit4}.tar.gz

Source10:       %{name}-README.txt
Patch1:         %{name}-noexit.patch
Patch2:         %{name}-minizip.patch

ExcludeArch:    ppc64le

# Generic provider for Doom 3 BFG engine based games
Provides:       doom3bfg-engine = 1.1401

# Contains a very old and unknown version of timidity to play audio in original
# Doom I & II.
Provides:       bundled(timidity) = 0.2i
Provides:       bundled(libbinkdec)

BuildRequires:  dxc
BuildRequires:  gcc-c++
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  glew-devel
BuildRequires:  libjpeg-turbo-devel >= 1.5.0
BuildRequires:  libpng-devel
BuildRequires:  minizip-compat-devel
BuildRequires:  openal-soft-devel
BuildRequires:  rapidjson-devel
BuildRequires:  zlib-devel
BuildRequires:  SDL2-devel
BuildRequires:  vulkan-loader-devel

%description
%{name} is a Doom 3 BFG GPL source modification. The goal of %{name}
is to bring Doom 3 BFG with the help of SDL to all suitable platforms. Bugs
present in the original DOOM 3 will be fixed (when identified) without altering
the original game-play.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

tar -xzf %{SOURCE1} --strip-components=1 -C neo/extern/nvrhi
tar -xzf %{SOURCE2} --strip-components=1 -C neo/extern/nvrhi/rtxmu
tar -xzf %{SOURCE3} --strip-components=1 -C neo/extern/nvrhi/thirdparty/Vulkan-Headers
tar -xzf %{SOURCE4} --strip-components=1 -C neo/extern/nvrhi/thirdparty/cxxopts

# Remove bundled libraries
rm -fr neo/libs/{jpeg-6,openal-soft,ffmpeg*,png,rapidjson,zlib}

cp %{SOURCE10} ./Fedora-README.txt

%build
# Uncomment this to disable console and dev menu
#CXXFLAGS='%{optflags} -DID_RETAIL'

LDFLAGS='-lpthread'

# Passing a fake build name avoids default CMAKE_BUILD_TYPE="RelWithDebInfo"
# which has hard coded GCC optimizations.
%cmake \
    -DCMAKE_BUILD_TYPE=Fedora \
    -DBINKDEC=ON \
    -DFFMPEG=OFF \
    -DOPENAL=ON \
    -DUSE_PRECOMPILED_HEADERS=OFF \
    -DUSE_SYSTEM_LIBGLEW=ON \
    -DUSE_SYSTEM_LIBJPEG=ON \
    -DUSE_SYSTEM_LIBPNG=ON \
    -DUSE_SYSTEM_RAPIDJSON=ON \
    -DUSE_SYSTEM_ZLIB=ON \
    -DUSE_VULKAN=ON \
    neo

%cmake_build

%post
/usr/sbin/alternatives --install %{_bindir}/doom3bfg-engine doom3bfg-engine %{_bindir}/RBDoom3BFG 10

%preun
if [ "$1" = 0 ]; then
    /usr/sbin/alternatives --remove doom3bfg-engine %{_bindir}/RBDoom3BFG
fi

%install
install -D -p -m 0755 %{_vpath_builddir}/RBDoom3BFG %{buildroot}%{_bindir}/RBDoom3BFG

# The library is loaded at runtime only and is expected with exactly this name;
# so no ldconfig for it; much like a plugin. We can also then remove RPATH from
# the main binary.
install -D -p -m 0755 %{_vpath_builddir}/idlib/libidlib.so %{buildroot}%{_libdir}/libidlib.so
chrpath --delete %{buildroot}%{_bindir}/RBDoom3BFG

# Shaders
mkdir -p %{buildroot}%{_datadir}/doom3bfg
cp -av base %{buildroot}%{_datadir}/doom3bfg/

%files
%license LICENSE.md
%doc Fedora-README.txt RELEASE-NOTES.md README.md
%{_bindir}/RBDoom3BFG
%{_libdir}/libidlib.so
%{_datadir}/doom3bfg

%changelog
* Tue Aug 08 2023 Simone Caronni <negativo17@gmail.com> - 1.5.1-4.20230714gita51833e
- Update to latest snapshot.

* Sun Jul 02 2023 Simone Caronni <negativo17@gmail.com> - 1.5.1-2
- Fix game not being able to restart.

* Thu Jun 22 2023 Simone Caronni <negativo17@gmail.com> - 1.5.1-1
- Update to final 1.5.1.

* Tue Apr 04 2023 Simone Caronni <negativo17@gmail.com> - 1.5.0-3.20230402git1d36dcf
- Add additional Doom 3 BFG custom resources.

* Mon Apr 03 2023 Simone Caronni <negativo17@gmail.com> - 1.5.0-2.20230402git1d36dcf
- Update to latest snapshot.

* Sun Apr 02 2023 Simone Caronni <negativo17@gmail.com> - 1.5.0-1.20230330git33b5448
- Update to latest snapshot.

* Fri Apr 08 2022 Simone Caronni <negativo17@gmail.com> - 1.4.0-1
- Update to final 1.4.0.

* Mon Oct 04 2021 Simone Caronni <negativo17@gmail.com> - 1.3.0-4.20211001gitbf44cd0
- Update snapshot.

* Fri Sep 17 2021 Simone Caronni <negativo17@gmail.com> - 1.3.0-3.20210911gitcbf17d4
- Update to latest snapshot.

* Thu Sep 09 2021 Simone Caronni <negativo17@gmail.com> - 1.3.0-2.20210828git87bbeba
- Update to latest snapsthot.

* Mon Aug 02 2021 Simone Caronni <negativo17@gmail.com> - 1.3.0-1.20210730gitb02eaf8
- Update to latest 1.3.0 snapshot.

* Fri Dec 04 2020 Simone Caronni <negativo17@gmail.com> - 1.2.0-7.20201126git05a3e04
- Update to latest snapshot.
- Drop suppport for CentOS/RHEL 7.

* Sun Jun 07 2020 Simone Caronni <negativo17@gmail.com> - 1.2.0-6.20200531gitc0e76c4
- Update to latest snapshot, drop no longer required patches.
- Switch to GCC 8 for EL7.

* Fri Feb 14 2020 Simone Caronni <negativo17@gmail.com> - 1.2.0-5.20200202gitbce8237
- Update to latest snapshot.

* Mon Nov 04 2019 Simone Caronni <negativo17@gmail.com> - 1.2.0-4.20191015gitf18ccd6
- Fix build on RHEL/CentOS 7.

* Sun Nov 03 2019 Simone Caronni <negativo17@gmail.com> - 1.2.0-3.20191026gitf18ccd6
- Update snapshot to post 1.2.0-preview1 release.

* Sun Jun 16 2019 Simone Caronni <negativo17@gmail.com> - 1.2.0-2.20181013git4356376
- Fedora 30 requires minizip-compat-devel.

* Sun Jan 06 2019 Simone Caronni <negativo17@gmail.com> - 1.2.0-1.20181013git4356376
- Update to latest snapshot.

* Mon Oct 02 2017 Simone Caronni <negativo17@gmail.com> - 1.1.0-8.20170903gitc8e3cd9
- Update to latest snapshot.

* Thu May 04 2017 Simone Caronni <negativo17@gmail.com> - 1.1.0-7.20170421git81dc651
- Update to latest snapshot.

* Thu Apr 06 2017 Simone Caronni <negativo17@gmail.com> - 1.1.0-6.20161018git80df318
- Exclude ppc64le.

* Thu Apr 06 2017 Simone Caronni <negativo17@gmail.com> - 1.1.0-5.20161018git80df318
- Remove bundled rapidjson.

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
