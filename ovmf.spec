%undefine _debugsource_packages

Name: ovmf
Version: 202411
Release: 1
Source0: https://github.com/tianocore/edk2/archive/refs/tags/edk2-stable%{version}.tar.gz
# OVMF official sources list OpenSSL_3_0_9, but let's try not to pull in security bugs
# Unfortunately OVMF doesn't seem to be ready for anything past the 3.0.x branch
Source1: https://github.com/openssl/openssl/archive/refs/tags/openssl-3.0.15.tar.gz#/openssl.tar.gz
# OVMF wants https://github.com/google/brotli/archive/f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tar.gz, but let's try something less buggy
Source2: https://github.com/google/brotli/archive/refs/tags/v1.1.0.tar.gz#/brotli.tar.gz
Source3: https://github.com/MIPI-Alliance/public-mipi-sys-t/archive/370b5944c046bab043dd8b133727b2135af7747a.tar.gz#/mipisyst.tar.gz
# OVMF wants https://github.com/Mbed-TLS/mbedtls/tree/8c89224991adff88d53cd380f42a2baa36f91454, but we can do better
Source4: https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/v3.6.2.tar.gz#/mbedtls.tar.gz
# OVMF wants https://github.com/DMTF/libspdm/tree/98ef964e1e9a0c39c7efb67143d3a13a819432e0
Source5: https://github.com/DMTF/libspdm/archive/refs/tags/3.6.0.tar.gz#/libspdm.tar.gz
Summary: A UEFI firmware implementation for virtual machines
URL: https://github.com/tianocore/tianocore.github.io/wiki/OVMF-FAQ
License: BSD+Patent
Group: System
BuildRequires: pkgconfig(uuid)
BuildRequires: nasm
BuildRequires: iasl

%description
A UEFI firmware implementation for virtual machines

%prep
%autosetup -p1 -n edk2-edk2-stable%{version}
tar xf %{S:1}
tar xf %{S:2}
tar xf %{S:3}
tar xf %{S:4}
tar xf %{S:5}
rm -rf CryptoPkg/Library/OpensslLib/openssl MdeModulePkg/Library/BrotliCustomDecompressLib/brotli BaseTools/Source/C/BrotliCompress/brotli MdePkg/Library/MipiSysTLib/mipisyst CryptoPkg/Library/MbedTlsLib/mbedtls SecurityPkg/DeviceSecurity/SpdmLib/libspdm
mv openssl-* CryptoPkg/Library/OpensslLib/openssl
# Adapt to some files moving around in OpenSSL 3.2
#ln -s include/internal/e_os.h CryptoPkg/Library/OpensslLib/openssl/
mv brotli-* MdeModulePkg/Library/BrotliCustomDecompressLib/brotli
mv public-mipi-sys-t-* MdePkg/Library/MipiSysTLib/mipisyst
mv mbedtls-* CryptoPkg/Library/MbedTlsLib/mbedtls
mv libspdm-* SecurityPkg/DeviceSecurity/SpdmLib/libspdm
cp -a MdeModulePkg/Library/BrotliCustomDecompressLib/brotli BaseTools/Source/C/BrotliCompress/brotli

%build
. ./edksetup.sh
cd OvmfPkg
sh build.sh -b RELEASE

%install
mkdir -p %{buildroot}%{_datadir}/qemu
cp Build/OvmfX64/RELEASE_GCC5/FV/OVMF.fd %{buildroot}%{_datadir}/qemu/

%files
%{_datadir}/qemu/OVMF.fd
