# Package contains plugins not built with libtool, and does not contain
# any shared libraries, so disable underlinking checks - AdamW 2008/07
%define _disable_ld_no_undefined 1

%define pre	0
%define svn	0
%define rel	4
%if %pre
%define release		%mkrel -c %pre %rel
%define distname	http://downloads.sourceforge.net/%{name}/%{name}-%{version}%{pre}.tar.bz2
%define dirname		%{name}-%{version}%{pre}
%else
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	http://www.amsn-project.net/amsn_dev.tar.gz
%define dirname		msn
%else
%define release		%mkrel %rel
%define distname	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
%define dirname		%{name}-%{version}
%endif
%endif

Summary:	MSN Messenger clone for Linux
Summary(fr):	Cl�ne MSN Messenger pour Linux
Summary(de):	MSN Messenger-Klon f�r Linux
Name:		amsn
Version:	0.97.2
Release:	%{release}
License:	GPLv2+
Group:		Networking/Instant messaging
URL:		http://amsn.sourceforge.net/
Source0:	%{distname}
Source2:	amsn-0.97-startup
Patch0:		amsn-0.95-www-browser.diff
# Make it detect Tcl/Tk 8.6 - not sure if it's needed - AdamW 2008/10
Patch1:		amsn-0.97.2-tcl86.patch
BuildRequires:	tcl >= 8.5
BuildRequires:	openssl-devel
BuildRequires:	tk >= 8.5
BuildRequires:  tcl-devel >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:  automake
BuildRequires:	ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  png-devel
BuildRequires:  jpeg-devel
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
Requires:	tcltls
Requires:       soundwrapper
Requires:	tcl-snack
Suggests:	gstreamer0.10-farsight
BuildRoot:	%{_tmppath}/buildroot-%{name}-%{version}

%description
AMSN is a Microsoft Messenger (MSN) clone for Unix, Windows and 
Macintosh platforms. It supports file transfers, groups, video,
voice and many more features.

%description -l fr
amsn est un client Microsoft Messenger (MSN) pour UNIX, Windows et
Macintosh écrit en Tcl/Tk.  Il supporte les tranferts de fichiers, les
groupes et beaucoup d'autres possibilités. 
Visitez http://amsn.sourceforge.net/ pour de plus amples d�tails.

%description -l de
amsn ist ein Microsoft Messenger (MSN) Client f�r UNIX, Windows und
Macintosh, der in Tcl/Tk geschrieben ist. Es unterst�tzt
Datei�bertragungen, Gruppen uvm.
Begeben Sie sich auf http://amsn.sourceforge.net/ um mehr �ber dieses
Projekt zu erfahren.

%prep

%setup -q -n %{dirname}
%patch0 -p0 -b .www-browser
%patch1 -p1 -b .tcl86

# lib64 fixes
sed -i -e "s|/usr/lib/|%{_libdir}|g" configure*
sed -i -e "s|/lib\b|/%{_lib}|g" configure*
sed -i -e "s|^set libtls .*|set libtls \"%{tcl_sitearch}/tls1.6\"|g" amsn

%build
rm -f configure
autoreconf -i -f
%configure2_5x --enable-alsa
%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -d %{buildroot}%{_bindir}
rm -f %{buildroot}%{_bindir}/amsn
install -m0755 %{SOURCE2} %{buildroot}%{_bindir}/amsn

# fix softlinks
pushd %{buildroot}%{_bindir}
    ln -snf %{_datadir}/amsn/amsn-remote amsn-remote
    ln -snf %{_datadir}/amsn/amsn-remote-CLI amsn-remote-CLI
popd

ln -sf %{_docdir}%{name}-%{version}/README %{buildroot}%{_datadir}/amsn/README
ln -sf %{_docdir}%{name}-%{version}/HELP %{buildroot}%{_datadir}/amsn/HELP

# Menu
sed -i -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/amsn/amsn.desktop
desktop-file-install --vendor="" \
  --remove-key="Encoding" \
  --remove-key="Info" \
  --remove-category="Application" \
  --remove-key='Info' \
  --remove-key='Encoding' \
  --add-category="Network" \
  --add-category="InstantMessaging" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/amsn %{buildroot}%{_datadir}/amsn/amsn.desktop

mkdir -p %{buildroot}%{_datadir}/applications
cp  %{buildroot}%{_datadir}/amsn/amsn.desktop %{buildroot}%{_datadir}/applications/amsn.desktop

#icons
mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{128x128,96x96,72x72,64x64,48x48,32x32,22x22,16x16}/apps
install -m644 desktop-icons/128x128/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/128x128/apps/%{name}.png
install -m644 desktop-icons/96x96/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/96x96/apps/%{name}.png
install -m644 desktop-icons/72x72/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/72x72/apps/%{name}.png
install -m644 desktop-icons/64x64/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -m644 desktop-icons/48x48/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 desktop-icons/32x32/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 desktop-icons/22x22/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/22x22/apps/%{name}.png
install -m644 desktop-icons/16x16/apps/%{name}.png %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# cleanup
rm -rf %{buildroot}%{_datadir}/amsn/HELP
rm -rf %{buildroot}%{_datadir}/amsn/README
rm -f %{buildroot}%{_datadir}/amsn/sndplay

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

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
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/pixmaps/*

