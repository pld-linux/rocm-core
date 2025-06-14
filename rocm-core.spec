Summary:	ROCm base component
Summary(pl.UTF-8):	Komponent podstawowy ROCm
Name:		rocm-core
Version:	6.4.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ROCm/rocm-core/releases
Source0:	https://github.com/ROCm/rocm-core/archive/rocm-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c6bb77e5e4faece76dbdfd67ba4ea92a
URL:		https://rocm.docs.amd.com/
BuildRequires:	cmake >= 3.16
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ROCM-CORE is a package which can be used to get ROCm release version,
get ROCm install path information etc.

It is also important to note that ROCM-CORE takes the role as a base
component on which all of ROCm can depend, to make it easy to remove
all of ROCm with a package manager.

%description -l pl.UTF-8
ROCM-CORE to pakiet, którego można użyć do pobrania wersji wydania
ROCm, pobrania informacji o ścieżce instalacji ROCm itp.

Istotne jest też, że ROCM-CORE pełni rolę podstawowego komponentu, od
którego zależą wszystkie ROCm, dzięki czemu można usunąć całość ROCm
przy użyciu zarządcy pakietów.

%package devel
Summary:	Header files for ROCM-CORE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ROCM-CORE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ROCM-CORE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ROCM-CORE.

%prep
%setup -q -n %{name}-rocm-%{version}

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' runpath_to_rpath.py

%build
%cmake -B build \
	-DROCM_VERSION="%{version}"

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md copyright
%attr(755,root,root) %{_libdir}/librocm-core.so.*.*.*
%ghost %{_libdir}/librocm-core.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/librocm-core.so
%{_includedir}/rocm-core
%{_libdir}/cmake/rocm-core
%dir %{_libdir}/rocm-core
%attr(755,root,root) %{_libdir}/rocm-core/runpath_to_rpath.py
