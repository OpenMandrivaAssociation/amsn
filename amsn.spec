%define pre	0
%define svn	0
%define rel	3

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
Requires:	tcl-snack
Requires:	alsa-utils
Obsoletes:	amsn-plugins
Obsoletes:	amsn-skins
BuildRoot:	%{_tmppath}/buildroot-%{name}-%{version}

%description
AMSN is a Microsoft Messenger (MSN) clone for Unix, Windows and 
Macintosh platforms. It supports file transfers, groups, video,
voice and many more features.

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
mv  %{buildroot}%{_datadir}/amsn/amsn.desktop %{buildroot}%{_datadir}/applications/amsn.desktop

#icons
mkdir -p %{buildroot}%{_iconsdir}
mv %{buildroot}%{_datadir}/%{name}/desktop-icons/ %{buildroot}%{_iconsdir}/hicolor/
rm %{buildroot}%{_datadir}/pixmaps/%{name}.png

# cleanup
rm -f %{buildroot}%{_datadir}/%{name}/sndplay
rm -r %{buildroot}%{_datadir}/%{name}/lang/{*.*,LANG-HOWTO,sortlang}
rm -f %{buildroot}%{_datadir}/%{name}/docs/DOCS-HOWTO
rm -r %{buildroot}%{_datadir}/%{name}/{AGREEMENT,CREDITS,GNUGPL,INSTALL,remote.help,TODO}

# fix rights
chmod 755 %{buildroot}%{_datadir}/%{name}/utils/voipcontrols/test.tcl
chmod 755 %{buildroot}%{_datadir}/%{name}/skins/Dark\ Matter\ 4.0/pixmapscroll/test.tcl

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
%doc AGREEMENT CREDITS FAQ FAQ.html GNUGPL HELP README TODO lang/LANG-HOWTO docs/DOCS-HOWTO remote.help
%{_bindir}/%{name}
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-remote-CLI
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
