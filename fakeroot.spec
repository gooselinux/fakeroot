Summary: Gives a fake root environment
Name: fakeroot
Version: 1.12.2
Release: 22.2%{?dist}
License: GPL+
Group: Development/Tools
URL: http://fakeroot.alioth.debian.org/
Source0: http://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.tar.gz
#Patch0: fakeroot-1.6.4-atfuncs.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gcc-c++
BuildRequires: /usr/bin/getopt
#Currently not needed
#BuildRequires: po4a
BuildRequires: sharutils
Requires: /usr/bin/getopt
Requires: fakeroot-libs = %{version}-%{release}

%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.

%package libs
Summary: Gives a fake root environment (libraries)
Group: Development/Tools

%description libs
This package contains the libraries required by %{name}.

%prep
%setup -q
#patch0 -p1 -b .atfixes
for file in ./doc/*/*.1; do
  iconv -f latin1 -t utf8 < $file > $file.new
  mv -f $file.new $file
done

%build
for type in sysv tcp; do
mkdir obj-$type
cd obj-$type
cat >> configure << 'EOF'
#! /bin/sh
exec ../configure "$@"
EOF
chmod +x configure
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --libdir=%{_libdir}/libfakeroot \
  --with-ipc=$type \
  --program-suffix=-$type
make
cd ..
done

%install
rm -rf %{buildroot}
for type in sysv tcp; do
  make -C obj-$type install libdir=%{_libdir}/libfakeroot DESTDIR=%{buildroot}
  chmod 644 %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so 
  mv %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so \
     %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  strip -s %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.*a*
done

ln -s faked-tcp %{buildroot}%{_bindir}/faked
ln -s fakeroot-tcp %{buildroot}%{_bindir}/fakeroot
ln -s libfakeroot-tcp.so %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so

%check
for type in sysv tcp; do
  make -C obj-$type check
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS BUGS DEBUG doc/README.saving debian/changelog
%{_bindir}/faked-*
%{_bindir}/faked
%{_bindir}/fakeroot-*
%{_bindir}/fakeroot
%{_mandir}/man1/faked-*.1*
%{_mandir}/man1/fakeroot-*.1*
%lang(es) %{_mandir}/es/man1/faked-*.1*
%lang(es) %{_mandir}/es/man1/fakeroot-*.1*
%lang(fr) %{_mandir}/fr/man1/faked-*.1*
%lang(fr) %{_mandir}/fr/man1/fakeroot-*.1*
%lang(sv) %{_mandir}/sv/man1/faked-*.1*
%lang(sv) %{_mandir}/sv/man1/fakeroot-*.1*
%lang(nl) %{_mandir}/nl/man1/faked-*.1*
%lang(nl) %{_mandir}/nl/man1/fakeroot-*.1*

%files libs
%dir %{_libdir}/libfakeroot
%{_libdir}/libfakeroot/libfakeroot-*.so
%{_libdir}/libfakeroot/libfakeroot-0.so

%changelog
* Tue Jul  6 2010 Richard W.M. Jones <rjones@redhat.com> - 1.12.2-22.2
- Don't add extra characters after dist tag in release (RHBZ#604548).

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1.12.2-22.1.el6.1
- Strip libfakeroot-*.so (RHBZ#596819).

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.12.2-22.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.12.2-21
- Update to 1.12.2.
- Create a fakeroot-libs subpackage so that the package is multilib
  aware (by Richard W.M. Jones <rjones@redhat.com>, see RH bug
  #490953).

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.12.1-20
- Update to 1.12.1.

* Sat Nov 22 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.11-19
- Update to 1.11.

* Fri Oct  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.7-18
- Update to 1.9.7.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.6-17
- %%check || : does not work anymore.

* Sun Aug  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.6-16
- Update to 1.9.6.

* Thu Mar  8 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.6.4-15
- Update to 1.6.4.

* Wed Jan 10 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.12-14
- Update to 1.5.12.

* Sun Jan  7 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-13
- po4a currently not need as a BR.
- remove empty README, add debian/changelog.

* Sun Dec 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-12
- Add %%{_libdir}/libfakeroot to %%files.
- Add %%check.

* Fri Dec 29 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-11
- Extend the %%description a bit.

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-10
- Don't build static lib.
- Exclude libtool lib.
- %%makeinstall to make install DESTDIR=%%buildroot.

* Mon Aug  7 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-9
- Update to 1.5.10.

* Fri Feb 17 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.7.

* Thu Nov 24 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.5.

* Sat Sep 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.1.

* Fri Sep  2 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.4.3.

* Sun Jul  3 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.4.1.

* Sun Feb  6 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.4.

* Sun Jan 25 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.8.3.

* Wed Oct  8 2003 Axel Thimm <Axel.Thimm@ATrpms.net> 
- Initial build.
