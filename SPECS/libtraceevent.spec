# git tag
#%%global commit 5dd505f3aba255c5fbc2a6dbed57fcba51b400f6
#%%global commitdate 20201009
#%%global shortcommit %%(c=%%{commit}; echo ${c:0:7})

Name: libtraceevent
Version: 1.5.3
Release: 1%{?dist}
License: LGPLv2+ and GPLv2+
Summary: Library to parse raw trace event formats

URL: https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/
# If upstream does not provide tarballs, to generate:
# git clone git://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git
# cd libtraceevent
# git archive --prefix=libtraceevent-%%{version}/ -o libtraceevent-%%{version}.tar.gz %%{git_commit}
#Source0: libtraceevent-%%{version}.tar.gz
Source0: https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/libtraceevent-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires: xmlto
BuildRequires: asciidoc

%global __provides_exclude_from ^%{_libdir}/traceevent/plugins


%description
libtraceevent is a library to parse raw trace event formats.

%package devel
Summary: Development headers of %{name}
Requires: %{name}%{_isa} = %{version}-%{release}

%description devel
Development headers of %{name}-libs

%prep
%autosetup -p1

%build
MANPAGE_DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep manpages/docbook.xsl`
%set_build_flags
#looks like CFLAGS is ignored when compiling plugins, but not EXTRA_CFLAGS
export EXTRA_CFLAGS="%{optflags}"
export LDFLAGS="-Wl,-z,now"
make -O -j1 V=1 VERBOSE=1 prefix=%{_prefix} libdir=%{_libdir} MANPAGE_XSL=%{MANPAGE_DOCBOOK_XSL} all doc

%install
%set_build_flags
#looks like CFLAGS is ignored when compiling plugins, but not EXTRA_CFLAGS
export EXTRA_CFLAGS="%{optflags}"
export LDFLAGS="-Wl,-z,now"
%make_install prefix=%{_prefix} libdir=%{_libdir} install doc-install
rm -rf %{buildroot}/%{_libdir}/libtraceevent.a

%files
%license LICENSES/LGPL-2.1
%license LICENSES/GPL-2.0
%{_libdir}/traceevent/
%{_libdir}/libtraceevent.so.%{version}
%{_libdir}/libtraceevent.so.1
%{_mandir}/man3/tep_*.3.*
%{_mandir}/man3/libtraceevent.3.*
%{_mandir}/man3/trace_seq*.3.*
%{_docdir}/%{name}-doc

%files devel
%{_includedir}/traceevent/
%{_libdir}/libtraceevent.so
%{_libdir}/pkgconfig/libtraceevent.pc

%changelog
* Mon Oct 24 2022 Michael Petlan <mpetlan@redhat.com> - 1.5.3-1
- Initial libtraceevent
  Related: rhbz#2075197

