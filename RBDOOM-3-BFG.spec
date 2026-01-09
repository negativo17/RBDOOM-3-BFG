%global commit0 b19eb88717fd54465814a3ae3b9086192c1912d9
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20250123

# neo/extern/ShaderMake
%global commit1 13867771f6142f35690a5e2103c1e1efdd90cb0e
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
# neo/extern/nvrhi
%global commit2 dafbd407f6fb8b91078da72ca1712dbbd6ac2496
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

%global tag %{version}

Name:           RBDOOM-3-BFG
Version:        1.6.0
Release:        3%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Robert Beckebans' Doom 3 BFG engine
License:        GPLv3+ with exceptions
URL:            https://github.com/RobertBeckebans/%{name}

%if 0%{?tag:1}
Source0:        https://github.com/RobertBeckebans/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%else
Source0:        %{name}-%{shortcommit0}.tar.xz
%endif
Source1:        https://github.com/RobertBeckebans/ShaderMake/archive/%{commit1}.tar.gz#/ShaderMake-%{shortcommit1}.tar.gz
Source2:        https://github.com/RobertBeckebans/nvrhi/archive/%{commit2}.tar.gz#/nvrhi-%{shortcommit2}.tar.gz

Source10:       %{name}-README.txt
# Does not currently compile on Linux:
Patch0:         %{name}-no-rbdmap.patch

# Generic provider for Doom 3 BFG engine based games
Provides:       doom3bfg-engine = 1.1401

# Contains a very old and unknown version of timidity to play audio in original
# Doom I & II.
Provides:       bundled(timidity) = 0.2i
Provides:       bundled(libbinkdec)

BuildRequires:  dxc
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  glew-devel
BuildRequires:  ispc
BuildRequires:  libjpeg-turbo-devel >= 1.5.0
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

tar -xzf %{SOURCE1} --strip-components=1 -C neo/extern/ShaderMake
tar -xzf %{SOURCE2} --strip-components=1 -C neo/extern/nvrhi

cp %{SOURCE10} ./Fedora-README.txt

rm -f idlib/precompiled.h.gch
rm -f tools/compilers/precompiled.h.gch

%build
%cmake \
    -G "Unix Makefiles" \
    -DBINKDEC=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DFFMPEG=OFF \
    -DOPENAL=ON \
    -DRETAIL=ON \
    -DUSE_PRECOMPILED_HEADERS=OFF \
    -DUSE_SYSTEM_RAPIDJSON=ON \
    -DUSE_SYSTEM_ZLIB=ON \
    -DUSE_VULKAN=ON \
    -DUSE_VMA=ON \
    neo

%cmake_build

chrpath -d %{_vpath_builddir}/RBDoom3BFG

%post
/usr/sbin/alternatives --install %{_bindir}/doom3bfg-engine doom3bfg-engine %{_bindir}/RBDoom3BFG 10

%preun
if [ "$1" = 0 ]; then
    /usr/sbin/alternatives --remove doom3bfg-engine %{_bindir}/RBDoom3BFG
fi

%install
install -D -p -m 0755 %{_vpath_builddir}/RBDoom3BFG %{buildroot}%{_bindir}/RBDoom3BFG

mkdir -p %{buildroot}%{_libdir}/
install -p -m 0755 \
    %{_vpath_builddir}/idlib/libidlib.so \
    %{_vpath_builddir}/libs/moc/libMaskedOcclusionCulling.so \
    %{buildroot}%{_libdir}/

# Shaders
mkdir -p %{buildroot}%{_datadir}/doom3bfg
cp -av base %{buildroot}%{_datadir}/doom3bfg/

# Do not overwrite base configuration (one mouse button at the moment of writing this):
rm -f %{buildroot}%{_datadir}/doom3bfg/base/default.cfg

%files
%license LICENSE.md
%doc Fedora-README.txt RELEASE-NOTES.md README.md
%{_bindir}/RBDoom3BFG
%{_libdir}/libidlib.so
%{_libdir}/libMaskedOcclusionCulling.so
%{_datadir}/doom3bfg

%changelog
* Fri Jan 09 2026 Simone Caronni <negativo17@gmail.com> - 1.6.0-3
- Update to final 1.6.0.

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
