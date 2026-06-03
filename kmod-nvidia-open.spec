%define driver_version 595.58.03
%define kversion %(ls /usr/src/kernels/ | grep '\.gb10' | sort -V | tail -n 1)
%define kversion_bare %(echo "%{kversion}" | sed -e 's/+64k$//' -e 's/\\.el[0-9]*[^.]*\\.[^.]*$//' -e 's/-/./g')
%global debug_package %{nil}

Name:           kmod-nvidia-open
Version:        %{kversion_bare}
Release:        1%{?dist}
Summary:        NVIDIA open-source GPU kernel modules
License:        MIT and GPLv2
URL:            https://github.com/NVIDIA/open-gpu-kernel-modules
Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/refs/tags/%{driver_version}.tar.gz#/open-gpu-kernel-modules-%{driver_version}.tar.gz

BuildRequires:  kernel-devel-uname-r = %{kversion}
BuildRequires:  make
BuildRequires:  gcc
Requires:       kernel-uname-r = %{kversion}

Provides:       kmod-nvidia-open = 3:%{driver_version}
Provides:       nvidia-kmod = 3:%{driver_version}
Conflicts:      kmod-nvidia-open-dkms
Conflicts:      kmod-nvidia-latest-dkms

%description
This package provides the NVIDIA open-source GPU kernel modules built from
the official NVIDIA open-gpu-kernel-modules repository.

%prep
%setup -q -n open-gpu-kernel-modules-%{driver_version}

%build
unset LDFLAGS
make modules -j %{?_smp_mflags} SYSSRC=/usr/src/kernels/%{kversion}

%install
mkdir -p %{buildroot}/lib/modules/%{kversion}/extra/nvidia
install -m 644 kernel-open/nvidia-peermem.ko %{buildroot}/lib/modules/%{kversion}/extra/nvidia/
install -m 644 kernel-open/nvidia-modeset.ko %{buildroot}/lib/modules/%{kversion}/extra/nvidia/
install -m 644 kernel-open/nvidia-drm.ko %{buildroot}/lib/modules/%{kversion}/extra/nvidia/
install -m 644 kernel-open/nvidia-uvm.ko %{buildroot}/lib/modules/%{kversion}/extra/nvidia/
install -m 644 kernel-open/nvidia.ko %{buildroot}/lib/modules/%{kversion}/extra/nvidia/

%post
/sbin/depmod -a %{kversion} || :

%postun
/sbin/depmod -a %{kversion} || :

%files
/lib/modules/%{kversion}/extra/nvidia/nvidia-peermem.ko
/lib/modules/%{kversion}/extra/nvidia/nvidia-modeset.ko
/lib/modules/%{kversion}/extra/nvidia/nvidia-drm.ko
/lib/modules/%{kversion}/extra/nvidia/nvidia-uvm.ko
/lib/modules/%{kversion}/extra/nvidia/nvidia.ko

%changelog
