%global commit0 747878eee1667dcd39fbd6420ba24fc0dc40b172
%global date 20240827
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

Name:           RBDOOM-3-BFG
Version:        1.6.0
Release:        2%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Robert Beckebans' Doom 3 BFG engine
License:        GPLv3+ with exceptions
URL:            https://github.com/RobertBeckebans/%{name}

%if 0%{?tag:1}
Source0:        https://github.com/RobertBeckebans/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        %{name}-%{shortcommit0}.tar.xz
%endif
Source1:        %{name}-snapshot.sh

Source10:       %{name}-README.txt
# Does not currently compile on Linux:
Patch0:         %{name}-no-rbdmap.patch

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
BuildRequires:  ncurses-devel
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

cp %{SOURCE10} ./Fedora-README.txt

%build
%cmake \
    -G "Unix Makefiles" \
    -DBINKDEC=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DFFMPEG=OFF \
    -DOPENAL=ON \
    -DRETAIL=ON \
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
* Sat Aug 31 2024 Simone Caronni <negativo17@gmail.com> - 1.6.0-2.20240827git747878e
- Update to latest snapshot.
- Trim changelog.
- Adjust build options.

* Sat Apr 06 2024 Simone Caronni <negativo17@gmail.com> - 1.6.0-1.20240402git1875560
- Update to latest snapshot.
- Drop system minizip patch.
- Generate snapshot from a script to avoid checking Git commit IDs everywhere.

* Thu Nov 09 2023 Simone Caronni <negativo17@gmail.com> - 1.5.1-5.20231018gitb04705c
- Update to latest snapshot.

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
