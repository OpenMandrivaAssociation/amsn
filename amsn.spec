%define pre	0
%define svn	0
%define rel	2

%if %pre
%define release		%mkrel -c %pre %rel
%define distname	http://downloads.sourceforge.net/%{name}/%{name}-%{version}%{pre}.tar.bz2
%define dirname		%{name}-%{version}%{pre}
%else
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%{name}-%{svn}.tar.lzma
%define dirname		amsn
%else
%define release		%mkrel %rel
%define distname	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
%define dirname		%{name}-%{version}
%endif
%endif

Summary:	MSN Messenger clone for Linux
Summary(fr):	Clône MSN Messenger pour Linux
Summary(de):	MSN Messenger-Klon für Linux
Name:		amsn
Version:	0.98.1
Release:	%{release}
License:	GPLv2+
Group:		Networking/Instant messaging
URL:		http://amsn.sourceforge.net/
Source0:	%{distname}
Source3:	amsn-desktop_integration_r11173.tar.gz
Patch0:		amsn-11098-pt-encoding.patch
Patch1:		amsn-11406-defaultplugins.patch
Patch2:		amsn-11098-contact_list_extension.patch
Patch3:		amsn-0.98-linkage.patch
Patch4:		amsn-0.98.1-fix_file_locations.patch
BuildRequires:	tcl >= 8.5
BuildRequires:	openssl-devel
BuildRequires:	tk >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	png-devel
BuildRequires:	jpeg-devel
BuildRequires:	libv4l-devel
BuildRequires:	farsight2-devel
BuildRequires:	libgstreamer-plugins-base-devel
BuildRequires:	gupnp-igd-devel
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
Requires:	tcltls
Requires:	gstreamer0.10-plugins-bad
Requires:	gstreamer0.10-farsight2
Requires:	libnice-utils
Obsoletes:	amsn-plugins
Obsoletes:	amsn-skins
BuildRoot:	%{_tmppath}/buildroot-%{name}-%{version}

%description
AMSN is a Microsoft Messenger (MSN) clone for Unix, Windows and 
Macintosh platforms. It supports file transfers, groups, video,
voice and many more features.

%description -l fr
amsn est un client Microsoft Messenger (MSN) pour UNIX, Windows et
Macintosh écrit en Tcl/Tk.  Il supporte les tranferts de fichiers, les
groupes et beaucoup d'autres possibilités. 

%description -l de
amsn ist ein Microsoft Messenger (MSN) Client für UNIX, Windows und
Macintosh, der in Tcl/Tk geschrieben ist. Es unterstützt
Dateiübertragungen, Gruppen uvm.

%prep

%setup -q -n %{dirname}
%patch0 -p1 -b .pt_encoding
%patch1 -p0 -b .defaultplugins
%patch2 -p1 -b .contact_list_extension
%patch3 -p1 -b .link
%patch4 -p0 -b .locations

# remove some Win stuff
rm -r skins/default/winicons
rm -r plugins/music/MusicWin*

# use aplay to play sounds
sed -i 's#soundcommand "play \\$sound"#soundcommand "aplay -q \\$sound"#' config.tcl 

# add Desktop Integration plugin
cd plugins
tar xvf %{_sourcedir}/amsn-desktop_integration_r11173.tar.gz

%build
autoreconf -fi
%configure2_5x --enable-debug
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Menu
desktop-file-install --vendor="" \
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
%doc AGREEMENT CREDITS FAQ FAQ.html GNUGPL HELP README TODO lang/LANG-HOWTO
%{_bindir}/%{name}
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-remote-CLI
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/pixmaps/*
