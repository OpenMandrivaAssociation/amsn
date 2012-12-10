Summary:		MSN Messenger clone for Linux
Name:		amsn
Version:		0.98.4
Release:		1
License:		GPLv2+
Group:		Networking/Instant messaging
URL:		http://amsn.sourceforge.net/
Source0:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.bz2
Patch1:		amsn-0.98.4-defaultplugins.patch
Patch2:		amsn-0.98.4-contact_list_extension.patch
Patch3:		amsn-0.98.4-linkage.patch
Patch4:		amsn-0.98.4-fix_file_locations.patch
Patch5:		amsn-0.98.4-disable_version_check_on_startup.patch
Patch6:		amsn-0.98.4-amsnplus_flags.patch
Patch7:		amsn-0.98.4-kernel-2.6.38.patch
Patch8:		amsn-0.98.4-gcc43.patch
Patch9:		amsn-0.98.4-libpng15.patch
BuildRequires:	tcl >= 8.5
BuildRequires:	pkgconfig(openssl)
BuildRequires:	tk >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	pkgconfig(tk) >= 8.5
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(libpng)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libv4l2) >= 0.8.3
BuildRequires:	pkgconfig(farstream-0.1)
BuildRequires:	pkgconfig(gstreamer-app-0.10)
BuildRequires:	pkgconfig(gupnp-igd-1.0)
BuildRequires:	pkgconfig(imlib)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
Requires:	tcltls
Requires:	gstreamer0.10-plugins-bad
Requires:	gstreamer0.10-farstream
%if %mdkversion >= 201000
Requires:	libnice-utils
%else
Requires:	libnice
%endif
Requires:	tcl-snack
Requires:	alsa-utils
Obsoletes:	amsn-plugins
Obsoletes:	amsn-skins

%description
AMSN is a Microsoft Messenger (MSN) clone for Unix, Windows and 
Macintosh platforms. It supports file transfers, groups, video,
voice and many more features.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p0 -b .defaultplugins
%patch2 -p1 -b .contact_list_extension
%patch3 -p1 -b .link
%patch4 -p0 -b .locations
%patch5 -p0 -b .version_check
%patch6 -p0 -b .flags
%patch7 -p0 -b .kernel
%patch8 -p0 -b .gcc
%patch9 -p1 -b .libpng15

# remove some Win stuff
rm -r skins/default/winicons
rm -r plugins/music/MusicWin*

# use aplay to play sounds
sed -i 's#soundcommand "play \\$sound"#soundcommand "aplay -q \\$sound"#' config.tcl 

%build
autoreconf -fi
%configure2_5x --enable-debug

# don't use prebuilt snapshot binary for amsnplus,
# rebuild it and thus fix binary-or-shlib-defines-rpath
pushd plugins/amsnplus
	rm -rf snapshot
	%make
popd

%make verbose=yes

%install
%makeinstall_std

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
	--delete-original %{buildroot}%{_datadir}/%{name}/%{name}.desktop \
	--add-category="X-MandrivaLinux-CrossDesktop" \
	--dir %{buildroot}%{_datadir}/applications/ \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

# icons
mkdir -p %{buildroot}%{_iconsdir}
mv %{buildroot}%{_datadir}/%{name}/desktop-icons/ %{buildroot}%{_iconsdir}/hicolor/
rm %{buildroot}%{_datadir}/pixmaps/%{name}.png

# cleanup
rm -rf %{buildroot}%{_datadir}/%{name}/sndplay
rm -rf %{buildroot}%{_datadir}/%{name}/lang/{*.*,LANG-HOWTO,sortlang}
rm -rf %{buildroot}%{_datadir}/%{name}/docs/DOCS-HOWTO
rm -rf %{buildroot}%{_datadir}/%{name}/{GNUGPL,INSTALL,remote.help,TODO}
rm -rf %{buildroot}%{_datadir}/%{name}/plugins/amsnplus/{Makefile,snapshot.c}

# fix rights
find %{buildroot}%{_datadir}/%{name}/ -name test.tcl -exec chmod 755 {} \;

%files
%doc AGREEMENT CREDITS FAQ FAQ.html GNUGPL HELP README TODO lang/LANG-HOWTO docs/DOCS-HOWTO remote.help
%{_bindir}/%{name}
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-remote-CLI
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*


%changelog
* Fri Apr 01 2011 Funda Wang <fwang@mandriva.org> 0.98.4-3mdv2011.0
+ Revision: 649575
- fix build
- bump v4l req
- fix build with latest kernel
- fix build with rpm5

* Fri Dec 10 2010 Jani Välimaa <wally@mandriva.org> 0.98.4-2mdv2011.0
+ Revision: 620438
- add missing BRs
- add patch to build amsnplus with desired flags
- increase build time verbosity
- add X-MandrivaLinux-CrossDesktop back to the .desktop file

* Mon Dec 06 2010 Jani Välimaa <wally@mandriva.org> 0.98.4-1mdv2011.0
+ Revision: 612197
- new version 0.98.4
- drop P0 and update other patches
- clean .spec a bit

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.98.3-3mdv2011.0
+ Revision: 609972
- rebuild

  + Jani Välimaa <wally@mandriva.org>
    - fix requires to ease backporting

* Tue Mar 09 2010 Jani Välimaa <wally@mandriva.org> 0.98.3-2mdv2010.1
+ Revision: 516972
- rebuild (previous package was lost in BS)
- new version 0.98.3
- remove Desktop Integration plugin, it's now provided by upstream
- fix rpath issue of amsnplus plugin

* Mon Mar 01 2010 Jani Välimaa <wally@mandriva.org> 0.98.1-5mdv2010.1
+ Revision: 513063
- don't check for newer version on startup (Patch5)
- don't remove AGREEMENT or CREDITS from the main program dir; amsn needs access to them

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 0.98.1-4mdv2010.1
+ Revision: 492267
- rebuild for new libjpeg v8

* Thu Jan 07 2010 Jani Välimaa <wally@mandriva.org> 0.98.1-3mdv2010.1
+ Revision: 487239
- rebuild for new gupnp-igd

* Sat Nov 28 2009 Jani Välimaa <wally@mandriva.org> 0.98.1-2mdv2010.1
+ Revision: 470838
- clean up the main program dir
- fix file rights
- fix icons
- re-add "Desktop Integration" plugin
- drop startup script
- use aplay to play sounds
- fix amsn-remote and amsn-remote-CLI (P4)
- remove unneeded requires
- enable debug symbols
- fix file list
- clean spec

* Sat Nov 07 2009 Jani Välimaa <wally@mandriva.org> 0.98.1-1mdv2010.1
+ Revision: 462430
- new version 0.98.1
- removed unneeded BR

* Mon Oct 12 2009 Jani Välimaa <wally@mandriva.org> 0.98.0-5mdv2010.0
+ Revision: 456958
- don't remove README and HELP from the main program dir (fixes About window not appearing)

* Tue Sep 22 2009 Frederic Crozat <fcrozat@mandriva.com> 0.98.0-4mdv2010.0
+ Revision: 447377
- Remove dependency on obsolete gstreamer0.10-farsight

  + Frederik Himpe <fhimpe@mandriva.org>
    - Rebuild for new gupnp

* Fri Aug 28 2009 Jani Välimaa <wally@mandriva.org> 0.98.0-2mdv2010.0
+ Revision: 422040
- fix Imlib dependency

* Fri Aug 28 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-1mdv2010.0
+ Revision: 421899
- fix release number issue
- New version 0.98 final
- drop SOURCE3 (provided upstream)

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 0.98.0-0.11506.1mdv2010.0
+ Revision: 419749
- new snapshot
- finally fix linkage

* Sun Aug 02 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-0.11406.7mdv2010.0
+ Revision: 407554
- requires gstreamer0.10-plugins-bad

* Tue Jul 28 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-0.11406.6mdv2010.0
+ Revision: 402828
- New svn snapshot
- rediff p1
- fix Requires

* Sun Jun 28 2009 Wanderlei Cavassin <cavassin@mandriva.com.br> 0.98.0-0.11098.6mdv2010.0
+ Revision: 390148
- Added Desktop Integration plugin (default on).
  Fixed double extension in contact lists filename (reported upstream)

* Sun Jun 28 2009 Wanderlei Cavassin <cavassin@mandriva.com.br> 0.98.0-0.11098.5mdv2010.0
+ Revision: 390133
- Fix lang detection in startup script in cases like pt_BR.UTF-8.
  Fix pt encoding (langpt is utf-8).

* Sun Jun 21 2009 Frederik Himpe <fhimpe@mandriva.org> 0.98.0-0.11098.4mdv2010.0
+ Revision: 387876
- Rebuild for new libgupnp-igd2

* Sat Mar 21 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-0.11098.3mdv2009.1
+ Revision: 359962
- drop redundant requires
- requires libnice?\195

* Fri Mar 20 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-0.11098.2mdv2009.1
+ Revision: 358241
- add necessary requires for VoIP

* Thu Mar 19 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-0.11098.1mdv2009.1
+ Revision: 357736
- New svn snapshot
- obsoletes old plugins and skins

* Thu Mar 05 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-0.11074.1mdv2009.1
+ Revision: 349424
- New svn snapshot
- BR gupnp-igd-devel

* Fri Feb 20 2009 Emmanuel Andry <eandry@mandriva.org> 0.98.0-0.11028.1mdv2009.1
+ Revision: 343481
- BR libgstreamer-plugins-base-devel
- New svn snapshot
- BR libfarsight2-devel

* Sun Jan 11 2009 Adam Williamson <awilliamson@mandriva.org> 0.98.0-0.10841.1mdv2009.1
+ Revision: 328405
- drop various bits only needed for patches
- disable --as-needed as well as --no-undefined
- drop all patches: merged or superseded upstream
- bump to current SVN at recommendation of upstream to fix Tcl/Tk 8.6 issues

* Sat Jan 03 2009 Emmanuel Andry <eandry@mandriva.org> 0.97.2-7mdv2009.1
+ Revision: 324020
- add P3 and P4 from Fedora to add v4l2 support
- remove URL in descriptions
- fix french description

* Fri Dec 26 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.97.2-6mdv2009.1
+ Revision: 319261
- rebuild for new TCL/TK, probably

* Thu Dec 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.97.2-5mdv2009.1
+ Revision: 319122
- rebuild with Tcl 8.6b1 (seems needed)
- build with -DCONST86="" to fix another build issue
- add variables.patch, from Michael Schlenker: fixes build-breaking problems
- rediff www-browser.diff as www_browser.patch

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 0.97.2-4mdv2009.1
+ Revision: 310797
- adjust for new tcltls location
- use autoreconf, don't do it all manually
- do substitutions with sed not perl
- update tcltls dep
- add tcl86.patch to let it detect Tcl 8.6
- small cleanups

  + Emmanuel Andry <eandry@mandriva.org>
    - suggests gstreamer0.10-farsight for audio conversation support

* Tue Oct 21 2008 Adam Williamson <awilliamson@mandriva.org> 0.97.2-3mdv2009.1
+ Revision: 296301
- can't use -M to fix #39273 as it's invalid for anything but padsp: instead
  directly set PADSP_NO_MIXER, which is what -M does

* Tue Oct 21 2008 Adam Williamson <awilliamson@mandriva.org> 0.97.2-2mdv2009.1
+ Revision: 295886
- fix #39273 (use -M parameter for soundwrapper to fix high CPU use)

* Mon Aug 04 2008 Frederik Himpe <fhimpe@mandriva.org> 0.97.2-1mdv2009.0
+ Revision: 263306
- update to new version 0.97.2

* Wed Jul 02 2008 Adam Williamson <awilliamson@mandriva.org> 0.97.1-1mdv2009.0
+ Revision: 230821
- disable underlink checking (breaks on plugins, and package contains no shared libs)
- bit of spec cleaning
- new release 0.97.1

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat Feb 09 2008 Frederik Himpe <fhimpe@mandriva.org> 0.97-2mdv2008.1
+ Revision: 164480
- Rebuild against new tk 8.5.1 (fixes bug #37624)

  + Adam Williamson <awilliamson@mandriva.org>
    - damn, missed the -devel buildrequires
    - version the tcl / tk buildrequires to 8.5 for the 2008.0 backport

* Fri Dec 28 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.97-1mdv2008.1
+ Revision: 138861
- New version 0.97

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 12 2007 Adam Williamson <awilliamson@mandriva.org> 0.97-0.RC1.20071112.1mdv2008.1
+ Revision: 108305
- requires tcl-snack (required for audio chat to work, thanks Philippe Didier)
- new snapshot 20071112

* Thu Sep 06 2007 Adam Williamson <awilliamson@mandriva.org> 0.97-0.RC1.20070905.2mdv2008.0
+ Revision: 80724
- drop legacy icons
- fix menu entry issues
- update to current svn (more stable than RC1 as per austin)

* Sun Sep 02 2007 Funda Wang <fwang@mandriva.org> 0.97-0.RC1.2mdv2008.0
+ Revision: 77745
- add X-MandrivaLinux-CrossDesktop for amsn (bug#33061).
  Because it sits in contrib without distro flavour, it is very likely
  that users install it manually. Due to it is not a GTK/Qt applications,
  it will listed in Others forever without CrossDesktop.

  + Adam Williamson <awilliamson@mandriva.org>
    - revert previous change by blindauer (the req was already there)

  + Emmanuel Blindauer <blindauer@mandriva.org>
    - Added requires for libtcltls, or amsn won't connect.

* Tue Jun 12 2007 Adam Williamson <awilliamson@mandriva.org> 0.97-0.RC1.1mdv2008.0
+ Revision: 38334
- add fd.o icons
- small spec clean
- new release 0.97RC1

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Add --enable-alsa configure option to fix sound problems

* Wed Apr 25 2007 Gustavo De Nardin <gustavodn@mandriva.com> 0.96-3mdv2008.0
+ Revision: 18126
- rebuild for libtcl/tk 8.5


* Sat Dec 23 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.96-2mdv2007.0
+ Revision: 101910
- Fix BuildRequires

  + plouf <plouf>
    - Fix BuilRequires on libpng-devel
    - New release 0.96

* Mon Oct 16 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.95-9mdv2006.0
+ Revision: 65425
- Add BuildRequires

  + plouf <plouf>
    - add Requires on soundwrapper
    - Import amsn

