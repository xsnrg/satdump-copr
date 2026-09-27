%global commit f3d82adbfe04e57c596b93479d687f4b830ee26c
%global commitdate 20260921
%global shortcommit %(c=%{commit}; echo ${c:0:9})

Name:           satdump
Version:        2.0.0
Release:        0.8.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Generic satellite data processing software

License:        GPL-3.0-or-later
URL:            https://github.com/SatDump/SatDump
Source0:        https://github.com/SatDump/SatDump/archive/%{commit}.tar.gz

# GCC 16 on aarch64 segfaults in cc1plus compiling heavy nlohmann/json +
# angelscript template TUs at -O2 (independent of annobin/LTO). Use -O1 there.
%ifarch aarch64
%undefine _annotated_build
%global _lto_cflags %{nil}
%global optflags -O1 -g -pipe
%endif

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:  volk-devel
BuildRequires:  fftw-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libzstd-devel
BuildRequires:  jemalloc-devel
BuildRequires:  nng-devel
BuildRequires:  sqlite-devel
BuildRequires:  libcurl-devel
BuildRequires:  glfw-devel
BuildRequires:  armadillo-devel
BuildRequires:  libomp-devel
BuildRequires:  ocl-icd-devel
BuildRequires:  opencl-headers
BuildRequires:  libglvnd-devel
BuildRequires:  dbus-devel
BuildRequires:  portaudio-devel
BuildRequires:  hdf5-devel
BuildRequires:  rtl-sdr-devel
BuildRequires:  hackrf-devel
BuildRequires:  airspyone_host-devel
BuildRequires:  airspyhf-devel
BuildRequires:  uhd-devel
BuildRequires:  boost-devel
BuildRequires:  libiio-devel

%global simd_flags -DPLUGIN_SIMD_SSE41=OFF -DPLUGIN_SIMD_AVX2=OFF -DPLUGIN_SIMD_NEON=OFF
%ifarch x86_64
%global simd_flags -DPLUGIN_SIMD_SSE41=ON -DPLUGIN_SIMD_AVX2=ON -DPLUGIN_SIMD_NEON=OFF
%endif
%ifarch aarch64
%global simd_flags -DPLUGIN_SIMD_SSE41=OFF -DPLUGIN_SIMD_AVX2=OFF -DPLUGIN_SIMD_NEON=ON
%endif

%description
SatDump is a generic satellite data processing program. It demodulates,
decodes, and processes recorded or live satellite transmissions.

%prep
%autosetup -n SatDump-%{commit}

%build
%cmake \
  -DBUILD_GUI=ON \
  -DBUILD_OPENMP=ON \
  -DBUILD_OPENCL=ON \
  -DBUILD_TESTING=OFF \
  -DBUILD_TOOLS=OFF \
  -DPLUGIN_AARONIA_SDR_SUPPORT=OFF \
  -DPLUGIN_AAUDIO_SINK=OFF \
  -DPLUGIN_SDRPLAY_SDR_SUPPORT=OFF \
  -DPLUGIN_MIRISDR_SDR_SUPPORT=OFF \
  -DPLUGIN_RFNM_SDR_SUPPORT=OFF \
  -DPLUGIN_SDDC_SDR_SUPPORT=OFF \
  -DPLUGIN_SOAPY_SDR_SUPPORT=OFF \
  -DPLUGIN_LIMESDR_SDR_SUPPORT=OFF \
  -DPLUGIN_BLADERF_SDR_SUPPORT=OFF \
  %{simd_flags}
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/satdump.desktop

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md
%{_bindir}/satdump
%{_bindir}/satdump-ui
%{_bindir}/satdump_sdr_server
%{_libdir}/libsatdump*.so*
%{_libdir}/satdump/
%{_datadir}/satdump/
%{_datadir}/applications/satdump.desktop
%{_datadir}/icons/hicolor/
%{_includedir}/satdump/

%changelog
* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 2.0.0-0.8.20260921gitf3d82adbf
- aarch64: build -O1 to avoid GCC16 cc1plus segfault on nlohmann/angelscript

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 2.0.0-0.7.20260921gitf3d82adbf
- %undefine _annotated_build on aarch64 (0 does not disable the annobin macro)

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 2.0.0-0.6.20260921gitf3d82adbf
- Disable annobin via _annotated_build (aarch64 GCC 16 ICE); drop bad -fno-annobin

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 2.0.0-0.5.20260921gitf3d82adbf
- Disable LTO + annobin on aarch64 (GCC 16 ICE on angelscript/json TUs)

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 2.0.0-0.2.20260921gitf3d82adbf
- Add sqlite-devel required by master src-core

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 2.0.0-0.3.20260921gitf3d82adbf
- Add boost-devel (uhd usrp plugin headers)

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 2.0.0-0.4.20260921gitf3d82adbf
- Package satdump_sdr_server and hicolor icons added on master

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 1.2.2-2
- Drop BladeRF and LimeSuite; those -devel packages are not in Fedora

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 1.2.2-1
- Initial Copr package of release 1.2.2
