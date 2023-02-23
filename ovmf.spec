%undefine _debugsource_packages

Name: ovmf
Version: 202211
Release: 1
Source0: https://github.com/tianocore/edk2/archive/refs/tags/edk2-stable%{version}.tar.gz
# OVMF official sources list OpenSSL_1_1_1n, but let's try not to pull in security bugs
Source1: https://github.com/openssl/openssl/archive/refs/tags/OpenSSL_1_1_1t.tar.gz
Source2: https://github.com/google/brotli/archive/f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tar.gz#/brotli.tar.gz
Summary: A UEFI firmware implementation for virtual machines
URL: https://github.com/tianocore/tianocore.github.io/wiki/OVMF-FAQ
License: BSD+Patent
Group: System
BuildRequires: pkgconfig(uuid)
BuildRequires: nasm

%description
A UEFI firmware implementation for virtual machines

%prep
%autosetup -p1 -n edk2-edk2-stable%{version}
tar xf %{S:1}
tar xf %{S:2}
rm -rf CryptoPkg/Library/OpensslLib/openssl MdeModulePkg/Library/BrotliCustomDecompressLib/brotli BaseTools/Source/C/BrotliCompress/brotli
mv openssl-* CryptoPkg/Library/OpensslLib/openssl
mv brotli-* MdeModulePkg/Library/BrotliCustomDecompressLib/brotli
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
