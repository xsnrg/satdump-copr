Name:           satdump
Version:        1.2.2
Release:        2%{?dist}
Summary:        Generic satellite data processing software

License:        GPL-3.0-or-later
URL:            https://github.com/SatDump/SatDump
Source0:        https://github.com/SatDump/SatDump/archive/refs/tags/%{version}.tar.gz

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
%autosetup -n SatDump-%{version}

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
%{_libdir}/libsatdump*.so*
%{_libdir}/satdump/
%{_datadir}/satdump/
%{_datadir}/applications/satdump.desktop
%{_includedir}/satdump/

%changelog
* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 1.2.2-2
- Drop BladeRF and LimeSuite; those -devel packages are not in Fedora

* Sun Sep 27 2026 Jim Howard <xsnrg@users.noreply.github.com> - 1.2.2-1
- Initial Copr package of release 1.2.2
