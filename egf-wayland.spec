Name:           egl-wayland
Version:        1.1.21
Release:        1%{?dist}
Summary:        EGLStream-based Wayland external platform

License:        MIT
URL:            https://github.com/NVIDIA/egl-wayland
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Restrict the build to aarch64 as requested
ExclusiveArch:  aarch64

%global debug_package %{nil}

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.50
BuildRequires:  ninja-build
BuildRequires:  wayland-protocols-devel
BuildRequires:  libglvnd-devel
BuildRequires:  pkgconfig(eglexternalplatform)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl-backend)

Requires:       libglvnd-egl%{?_isa}
# Requires:       wayland%{?_isa}

%description
This is an implementation of a EGL External Platform library to add client-side
Wayland support to EGL on top of EGLDevice and EGLStream families of extensions.
This library implements an EGL External Platform interface to work along with
EGL drivers that support the external platform mechanism.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       wayland-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
# RHEL 10 uses the standard meson macros
%meson
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
# The compiled dynamic library
%{_libdir}/libnvidia-egl-wayland.so.1*
# The JSON configuration file so the NVIDIA driver loads it
%dir %{_datadir}/egl
%dir %{_datadir}/egl/egl_external_platform.d
%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json

%files devel
%{_libdir}/libnvidia-egl-wayland.so
%{_libdir}/pkgconfig/wayland-eglstream.pc
# Add the newly discovered pkgconfig file:
%{_datadir}/pkgconfig/wayland-eglstream-protocols.pc
# Claim the entire directory and all XML files inside it:
%{_datadir}/wayland-eglstream/

%changelog
