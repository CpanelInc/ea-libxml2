Prefix: /opt/cpanel/ea-libxml2
%define _prefix /opt/cpanel/ea-libxml2
%define _mandir /opt/cpanel/ea-libxml2
%define _docdir /opt/cpanel/ea-libxml2
%define _unpackaged_files_terminate_build 0

Summary: Library providing XML and HTML support
Name: ea-libxml2
Version: 2.13.8
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group: Development/Libraries
Source: https://download.gnome.org/sources/libxml2/2.14/libxml2-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: zlib-devel
BuildRequires: pkgconfig
BuildRequires: xz-devel
URL: http://xmlsoft.org/

%if 0%{?rhel} > 7
    %if 0%{?rhel} == 8
BuildRequires: python36
BuildRequires: python36-devel
    %endif
    %if 0%{?rhel} >= 9
BuildRequires: python3
BuildRequires: python3-devel
    %endif

BuildRequires: libnghttp2
Requires: libnghttp2
%else
BuildRequires: python
BuildRequires: python-devel
%endif

%description
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: ea-libxml2 = %{version}-%{release}
Requires: zlib-devel
Requires: xz-devel
Requires: pkgconfig
Prefix: %{_prefix}

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package static
Summary: Static library for libxml2
Group: Development/Libraries
Requires: ea-libxml2 = %{version}-%{release}

%description static
Static library for libxml2 provided for specific uses or shaving a few
microseconds when parsing, do not link to them for generic purpose packages.

%dump

%prep
%setup -n libxml2-%{version}
# workaround for #877567 - Very weird bug gzip decompression bug in "recent" libxml2 versions

# tar cvf libxml2-%{version}.tar.gz libxml2-%{version}

# %setup -T -a 0
# tar -zxvvf libxml2-%{version}.tar.gz --strip-components 1 -C libxml2-%{version}

# %patch0 -p1
# workaround for #877567 - Very weird bug gzip decompression bug in "recent" libxml2 versions
# %patch1 -p1 -b .do-not-check-crc

%build

%configure

make %{_smp_mflags}

find doc -type f -exec chmod 0644 \{\} \;

%install
rm -fr %{buildroot}

make install DESTDIR=%{buildroot}

%if 0%{?_licensedir:1}
mkdir -p %{buildroot}/%{_licensedir}
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxml2-%{version}/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxml2-python-%{version}/*

(cd example ; make clean ; rm -rf .deps Makefile)
gzip -9 -c doc/libxml2-api.xml > doc/libxml2-api.xml.gz


# %check
# disabled due to broken test in docs/example
# make runtests

mkdir -p %{buildroot}/opt/cpanel/ea-libxml2-devel/doc
cp -R example %{buildroot}/opt/cpanel/ea-libxml2-devel/doc

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
/opt/cpanel/ea-libxml2
%if 0%{?_licensedir:1}
%dir %{_licensedir}
%endif

%{!?_licensedir:%global license %%doc}
%license Copyright
%doc NEWS README.md
%doc %{_mandir}/man1/xmllint.1*
%doc %{_mandir}/man1/xmlcatalog.1*

%{_libdir}/lib*.so.*
%{_bindir}/xmllint
%{_bindir}/xmlcatalog

%files devel
%defattr(-, root, root)

%doc %{_mandir}/man1/xml2-config.1*
%doc NEWS README.md Copyright
%doc doc/*.html
/opt/cpanel/ea-libxml2-devel/doc

%{_libdir}/lib*.so
# %{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake

%files static
%defattr(-, root, root)
# %{_libdir}/*a

%changelog
* Thu Apr 17 2025 Cory McIntire <cory.mcintire@webpros.com> - 2.13.8-1
- EA-12821: Update ea-libxml2 from v2.13.6 to v2.13.8
- [CVE-2025-32415] schemas: Fix heap buffer overflow in xmlSchemaIDCFillNodeTables
- [CVE-2025-32414] python: Read at most len/4 characters. (Maks Verver)

* Tue Feb 18 2025 Cory McIntire <cory.mcintire@webpros.com> - 2.13.6-1
- EA-12713: Update ea-libxml2 from v2.13.5 to v2.13.6

* Fri Nov 15 2024 Cory McIntire <cory@cpanel.net> - 2.13.5-1
- EA-12551: Update ea-libxml2 from v2.13.4 to v2.13.5

* Wed Sep 18 2024 Cory McIntire <cory@cpanel.net> - 2.13.4-1
- EA-12396: Update ea-libxml2 from v2.13.3 to v2.13.4

* Thu Aug 29 2024 Julian Brown <julian.brown@cpanel.net> - 2.13.3-3
- ZC-12114: Build 2.13.3

* Tue Aug 13 2024 Cory McIntire <cory@cpanel.net> - 2.13.3-2
- EA-12336: Rolling “ea-libxml2” back to “f77d3db2ad0957accee0eda34f1bb8bc66a9bb5c”: breaks older php-pears

* Tue Aug 06 2024 Cory McIntire <cory@cpanel.net> - 2.13.3-1
- EA-12315: Update ea-libxml2 from v2.12.6 to v2.13.3

* Tue Jul 02 2024 Cory McIntire <cory@cpanel.net> - 2.12.6-2
- EA-12252: Rolling “ea-libxml2” back to “0e1f4ea2052c4cb2643ebd9d51394223643c6fc2”: breaks scl-phps

* Fri Mar 15 2024 Cory McIntire <cory@cpanel.net> - 2.12.6-1
- EA-12022: Update ea-libxml2 from v2.12.4 to v2.12.6
- [CVE-2024-25062] xmlreader: Don't expand XIncludes when backtracking

* Mon Jan 15 2024 Cory McIntire <cory@cpanel.net> - 2.12.4-1
- EA-11908: Update ea-libxml2 from v2.12.3 to v2.12.4

* Tue Dec 12 2023 Cory McIntire <cory@cpanel.net> - 2.12.3-1
- EA-11867: Update ea-libxml2 from v2.12.2 to v2.12.3

* Wed Dec 06 2023 Cory McIntire <cory@cpanel.net> - 2.12.2-1
- EA-11855: Update ea-libxml2 from v2.11.5 to v2.12.2

* Tue Nov 21 2023 Cory McIntire <cory@cpanel.net> - 2.11.5-2
- EA-11822: Rolling “ea-libxml2” back to “04c4b9a40fbd4c0f07e1b66ab71f24a66aa7f90d”: libxml2 upstream updated to 2.12 and changed a lot of .h files, apache/php need patches

* Mon Aug 14 2023 Cory McIntire <cory@cpanel.net> - 2.11.5-1
- EA-11608: Update ea-libxml2 from v2.11.4 to v2.11.5

* Mon May 22 2023 Cory McIntire <cory@cpanel.net> - 2.11.4-1
- EA-11431: Update ea-libxml2 from v2.11.3 to v2.11.4

* Thu May 11 2023 Cory McIntire <cory@cpanel.net> - 2.11.3-1
- EA-11414: Update ea-libxml2 from v2.11.2 to v2.11.3

* Fri May 05 2023 Cory McIntire <cory@cpanel.net> - 2.11.2-1
- EA-11401: Update ea-libxml2 from v2.11.1 to v2.11.2

* Mon May 01 2023 Cory McIntire <cory@cpanel.net> - 2.11.1-1
- EA-11388: Update ea-libxml2 from v2.10.4 to v2.11.1
    - Security Fixes
    - Fix use-after-free in xmlParseContentInternal() (David Kilzer)
    - xmllint: Fix use-after-free with --maxmem
    - parser: Fix OOB read when formatting error message
    - entities: Rework entity amplification checks

* Wed Apr 12 2023 Cory McIntire <cory@cpanel.net> - 2.10.4-1
- EA-11352: Update ea-libxml2 from v2.10.3 to v2.10.4
- [CVE-2023-29469] Hashing of empty dict strings isn't deterministic
- [CVE-2023-28484] Fix null deref in xmlSchemaFixupComplexType

* Thu Feb 02 2023 Cory McIntire <cory@cpanel.net> - 2.10.3-1
- EA-11205: Update ea-libxml2 from v2.9.7 to v2.10.3
- [CVE-2022-23308] Use-after-free of ID and IDREF attributes
- [CVE-2022-29824] Integer overflow in xmlBuf and xmlBuffer
- [CVE-2022-2309] Reset nsNr in xmlCtxtReset
- [CVE-2022-40304] Fix dict corruption caused by entity reference cycles
- [CVE-2022-40303] Fix integer overflows with XML_PARSE_HUGE

* Thu Sep 29 2022 Julian Brown <julian.brown@cpanel.net> - 2.9.7-5
- ZC-10009: Add changes so that it builds on AlmaLinux 9

* Thu May 14 2020 Julian Brown <julian.brown@cpanel.net> - 2.9.7-4
- ZC-6808: Build on CentOS8

* Tue Jan 23 2018 Dan Muey <dan@cpanel.net> - 2.9.7-3
- EA-7135: Add root path to %files and Ensure ownership of _licensedir if it is set

* Fri Jan 19 2018 Cory McIntire <cory@cpanel.net> - 2.9.7-2
- EA-7145: Remove incorrect Provides for libxml2

* Mon Dec 25 2017 Dan Muey <dan@cpanel.net> - 2.9.7-1
- EA-7043: Update from v2.9.4 to v2.9.7
- fixed %setup so that we do not need to modify tarball (EA-6094)
- remove unreferenced 2.9.4-remove-pyverify_fd patch
- Add Provides of libxml2

* Mon May 8 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 2.9.4-3
- Initial import to EasyApache 4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Kevin Fenzi <kevin@scrye.com> - 2.9.4-1
- Update to 2.9.4.
- Apply very hacky patch that removes the no longer in python-3.6 PyVerify_fd symbol.

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.9.3-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Kalev Lember <klember@redhat.com> - 2.9.3-2
- Fix obsoletes versions now that F22 has libxml2 2.9.3 (#1287262)

* Fri Nov 20 2015 Daniel Veillard <veillard@redhat.com> - 2.9.2-1
- upstream release of 2.9.3
- Fixes for CVE-2015-8035, CVE-2015-7942, CVE-2015-7941, CVE-2015-1819
  CVE-2015-7497, CVE-2015-7498, CVE-2015-5312, CVE-2015-7499, CVE-2015-7500
  and CVE-2015-8242
- many other bug fixes

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 2.9.2-9
- Rebuilt for Python3.5 rebuild
- Python3.5 has new naming convention for byte compiled files

* Tue Nov  3 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 2.9.2-8
- Remove executable permissions from documentation.  Complies with packaging
  guidelines and solves issue of libxml2-python3 package depending on python2

* Thu Aug 27 2015 Miro Hrončok <mhroncok@redhat.com> - 2.9.2-7
- Remove dependency on python2 from python3 subpackage, rhbz#1250940

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 2.9.2-6
- Rename the Python 3 subpackage to python3-libxml2 as per guidelines

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.9.2-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Jan 21 2015 Tomas Radej <tradej@redhat.com> - 2.9.2-3
- Added Python 3 subpackage

* Thu Oct 16 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.9.2-2
- Avoid corrupting the xml catalogs

* Thu Oct 16 2014 Daniel Veillard <veillard@redhat.com> - 2.9.2-1
- upstream release of 2.9.2
- Fix for CVE-214-3660 billion laugh DOS
- many other bug fixes

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.9.1-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 19 2013 Daniel Veillard <veillard@redhat.com> - 2.9.1-1
- upstream release of 2.9.1
- a couple more API entry point
- compatibility with python3
- a lot of bug fixes

* Mon Feb 11 2013 Daniel Veillard <veillard@redhat.com> - 2.9.0-4
- fix --nocheck build which I broke in october rhbz#909767

* Mon Nov 19 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.9.0-3
- workaround for crc/len check failure, rhbz#877567

* Thu Oct 11 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-2
- remaining cleanups from merge bug rhbz#226079
- do not put the docs in the main package, only in -devel rhbz#864731

* Tue Sep 11 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-1
- upstream release of 2.9.0
- A few new API entry points
- More resilient push parser mode
- A lot of portability improvement
- Faster XPath evaluation
- a lot of bug fixes and smaller improvement

* Fri Aug 10 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-0rc1
- upstream release candidate 1 of 2.9.0
- introduce a small API change, but ABI compatible, see
  https://mail.gnome.org/archives/xml/2012-August/msg00005.html
  patches for php, gcc/libjava and evolution-data-connector are upstream
  Grab me in cases of problems veillard@redhat.com
- many bug fixes including security aspects and small improvements

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Daniel Veillard <veillard@redhat.com> - 2.8.0-1
- upstream release of 2.8.0
- add lzma compression support
- many bug fixes and small improvements

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar  4 2011 Daniel Veillard <veillard@redhat.com> - 2.7.8-6
- fix a double free in XPath CVE-2010-4494 bug 665965

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Daniel Veillard <veillard@redhat.com> - 2.7.8-4
- reactivate shared libs versionning script

* Thu Nov  4 2010 Daniel Veillard <veillard@redhat.com> - 2.7.8-1
- Upstream release of 2.7.8
- various bug fixes, including potential crashes
- new non-destructive formatting option
- date parsing updated to RFC 5646

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Mar 15 2010 Daniel Veillard <veillard@redhat.com> - 2.7.7-1
- Upstream release of 2.7.7
- fix serious trouble with zlib >= 1.2.4
- xmllint new option --xpath
- various HTML parser improvements
- includes a number of nug fixes

* Tue Oct  6 2009 Daniel Veillard <veillard@redhat.com> - 2.7.6-1
- Upstream release of 2.7.6
- restore thread support off by default in 2.7.5

* Thu Sep 24 2009 Daniel Veillard <veillard@redhat.com> - 2.7.5-1
- Upstream release of 2.7.5
- fix a couple of Relax-NG validation problems
- couple more fixes

* Tue Sep 15 2009 Daniel Veillard <veillard@redhat.com> - 2.7.4-2
- fix a problem with little data at startup affecting inkscape #523002

* Thu Sep 10 2009 Daniel Veillard <veillard@redhat.com> - 2.7.4-1
- upstream release 2.7.4
- symbol versioning of libxml2 shared libs
- very large number of bug fixes

* Mon Aug 10 2009 Daniel Veillard <veillard@redhat.com> - 2.7.3-4
- two patches for parsing problems CVE-2009-2414 and CVE-2009-2416

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Daniel Veillard <veillard@redhat.com> - 2.7.3-1
- new release 2.7.3
- limit default max size of text nodes
- special parser mode for PHP
- bug fixes and more compiler checks

* Wed Dec  3 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-7
- Pull back into Python 2.6

* Wed Dec  3 2008 Caolán McNamara <caolanm@redhat.com> - 2.7.2-6
- AutoProvides requires BuildRequires pkgconfig

* Wed Dec  3 2008 Caolán McNamara <caolanm@redhat.com> - 2.7.2-5
- rebuild to get provides(libxml-2.0) into HEAD rawhide

* Mon Dec  1 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-4
- Rebuild for pkgconfig logic

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-3
- Rebuild for Python 2.6

* Wed Nov 12 2008 Daniel Veillard <veillard@redhat.com> - 2.7.2-2.fc11
- two patches for size overflows problems CVE-2008-4225 and CVE-2008-4226

* Fri Oct  3 2008 Daniel Veillard <veillard@redhat.com> 2.7.2-1.fc10
- new release 2.7.2
- Fixes the known problems in 2.7.1
- increase the set of options when saving documents

* Thu Oct  2 2008 Daniel Veillard <veillard@redhat.com> 2.7.1-2.fc10
- fix a nasty bug in 2.7.x, http://bugzilla.gnome.org/show_bug.cgi?id=554660

* Mon Sep  1 2008 Daniel Veillard <veillard@redhat.com> 2.7.1-1.fc10
- fix python serialization which was broken in 2.7.0
- Resolve: rhbz#460774

* Sat Aug 30 2008 Daniel Veillard <veillard@redhat.com> 2.7.0-1.fc10
- upstream release of 2.7.0
- switch to XML 1.0 5th edition
- switch to RFC 3986 for URI parsing
- better entity handling
- option to remove hardcoded limitations in the parser
- more testing
- a new API to allocate entity nodes
- and lot of fixes and clanups

* Mon Aug 25 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-4.fc10
- fix for entities recursion problem
- Resolve: rhbz#459714

* Fri May 30 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-3.fc10
- cleanup based on Fedora packaging guidelines, should fix #226079
- separate a -static package

* Thu May 15 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-2.fc10
- try to fix multiarch problems like #440206

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-1.fc9
- upstream release 2.6.32 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.6.31-2
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Daniel Veillard <veillard@redhat.com> 2.6.31-1.fc9
- upstream release 2.6.31 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Thu Aug 23 2007 Daniel Veillard <veillard@redhat.com> 2.6.30-1
- upstream release 2.6.30 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Tue Jun 12 2007 Daniel Veillard <veillard@redhat.com> 2.6.29-1
- upstream release 2.6.29 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Wed May 16 2007 Matthias Clasen <mclasen@redhat.com> 2.6.28-2
- Bump revision to fix N-V-R problem

* Tue Apr 17 2007 Daniel Veillard <veillard@redhat.com> 2.6.28-1
- upstream release 2.6.28 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.6.27-2
- rebuild against python 2.5

* Wed Oct 25 2006 Daniel Veillard <veillard@redhat.com> 2.6.27-1
- upstream release 2.6.27 see http://xmlsoft.org/news.html
- very large amount of bug fixes reported upstream

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.26-2.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.26-2.1
- rebuild

* Wed Jun  7 2006 Daniel Veillard <veillard@redhat.com> 2.6.26-2
- fix bug #192873
* Tue Jun  6 2006 Daniel Veillard <veillard@redhat.com> 2.6.26-1
- upstream release 2.6.26 see http://xmlsoft.org/news.html

* Tue Jun  6 2006 Daniel Veillard <veillard@redhat.com>
- upstream release 2.6.25 broken, do not ship !

