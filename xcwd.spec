Name: xcwd
Version: 1.0
Release: 1%{?dist}
Summary: X current working directory

License: Public Domain
%global debug_package %{nil}
%undefine _disable_source_fetch
URL: https://github.com/schischi/xcwd
Source: https://github.com/schischi/xcwd/archive/v1.0.tar.gz

BuildRequires: gcc, make

%description
 A simple tool that prints the current working directory of the currently
focused window

%files
%{_bindir}/%{NAME}

%prep
%setup -n %{NAME}-%{VERSION}

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 xcwd %{buildroot}%{_bindir}
