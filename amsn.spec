%define name	amsn
%define version	0.97
%define pre	RC1
%if %pre
%define release	%mkrel 0.%pre.1
%else
%define release	%mkrel 1
%endif

Summary:	MSN Messenger clone for Linux
Summary(fr):	Clône MSN Messenger pour Linux
Summary(de):	MSN Messenger-Klon für Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Instant messaging
URL:		http://amsn.sourceforge.net/
%if %pre
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}%{pre}.tar.bz2
%else
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
%endif
Source2:	amsn-0.95.startup.bz2
Patch0:		amsn-0.95-www-browser.diff
BuildRequires:	tcl >= 8.4.2-2mdk, openssl-devel
BuildRequires:	tk >= 8.4.2
BuildRequires:  tcl-devel, tk-devel
BuildRequires:  automake1.7
BuildRequires:	ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  png-devel
BuildRequires:  jpeg-devel
Requires:	tcl >= 8.4.2
Requires:	libtcltls1.50
Requires:	tk >= 8.4.2
Requires:	%{mklibname tcltls 1.50}
Requires:       soundwrapper
BuildRoot:	%{_tmppath}/buildroot-%{name}-%{version}

%description
AMSN is a Microsoft Messenger (MSN) clone for Unix, Windows and 
Macintosh platforms. It supports file transfers, groups, video,
voice and many more features.

%description -l fr
amsn est un client Microsoft Messenger (MSN) pour UNIX, Windows et
Macintosh Ã©crit en Tcl/Tk.  Il supporte les tranferts de fichiers, les
groupes et beaucoup d'autres possibilitÃ©s. 
Visitez http://amsn.sourceforge.net/ pour de plus amples détails.

%description -l de
amsn ist ein Microsoft Messenger (MSN) Client für UNIX, Windows und
Macintosh, der in Tcl/Tk geschrieben ist. Es unterstützt
Dateiübertragungen, Gruppen uvm.
Begeben Sie sich auf http://amsn.sourceforge.net/ um mehr über dieses
Projekt zu erfahren.

%prep

%if %pre
%setup -q -n %{name}-%{version}%{pre}
%else
%setup -q
%endif
%patch0 -p0 -b .www-browser

bzcat %{SOURCE2} > amsn.startup

# lib64 fixes
perl -pi -e "s|/usr/lib/|%{_libdir}|g" configure*
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
perl -pi -e "s|^set libtls .*|set libtls \"%{_libdir}/tls1.50\"|g" amsn

%build
rm -f configure
libtoolize --copy --force; aclocal-1.7; autoconf --force

%configure2_5x --enable-alsa

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_bindir}
rm -f %{buildroot}%{_bindir}/amsn
install -m0755 amsn.startup %{buildroot}%{_bindir}/amsn

# fix softlinks
pushd %{buildroot}%{_bindir}
    ln -snf %{_datadir}/amsn/amsn-remote amsn-remote
    ln -snf %{_datadir}/amsn/amsn-remote-CLI amsn-remote-CLI
popd

ln -sf %{_docdir}%{name}-%{version}/README %{buildroot}%{_datadir}/amsn/README
ln -sf %{_docdir}%{name}-%{version}/HELP %{buildroot}%{_datadir}/amsn/HELP

# Menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Network" \
  --add-category="InstantMessaging" \
  --add-category="X-MandrivaLinux-Internet-InstantMessaging" \
  --dir $RPM_BUILD_ROOT%{_datadir}/amsn $RPM_BUILD_ROOT%{_datadir}/amsn/amsn.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp  $RPM_BUILD_ROOT%{_datadir}/amsn/amsn.desktop $RPM_BUILD_ROOT%{_datadir}/applications/amsn.desktop

#icons
mkdir -p $RPM_BUILD_ROOT/{%_liconsdir,%_iconsdir,%_miconsdir}
mkdir -p $RPM_BUILD_ROOT/%_iconsdir/hicolor/{128x128,96x96,72x72,64x64,48x48,32x32,22x22,16x16}/apps
install -m644 desktop-icons/48x48/apps/%{name}.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
install -m644 desktop-icons/32x32/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
install -m644 desktop-icons/16x16/apps/%{name}.png $RPM_BUILD_ROOT/%_miconsdir/%name.png
install -m644 desktop-icons/128x128/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/128x128/apps/%name.png
install -m644 desktop-icons/96x96/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/96x96/apps/%name.png
install -m644 desktop-icons/72x72/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/72x72/apps/%name.png
install -m644 desktop-icons/64x64/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/64x64/apps/%name.png
install -m644 desktop-icons/48x48/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/48x48/apps/%name.png
install -m644 desktop-icons/32x32/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/32x32/apps/%name.png
install -m644 desktop-icons/22x22/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/22x22/apps/%name.png
install -m644 desktop-icons/16x16/apps/%{name}.png $RPM_BUILD_ROOT/%_iconsdir/hicolor/16x16/apps/%name.png

# cleanup
rm -rf %{buildroot}%{_datadir}/amsn/HELP
rm -rf %{buildroot}%{_datadir}/amsn/README
rm -f %{buildroot}%{_datadir}/amsn/sndplay

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AGREEMENT CREDITS FAQ GNUGPL HELP README TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-remote-CLI
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/pixmaps/*
