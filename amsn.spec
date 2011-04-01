Summary:	MSN Messenger clone for Linux
Name:		amsn
Version:	0.98.4
Release:	%mkrel 3
License:	GPLv2+
Group:		Networking/Instant messaging
URL:		http://amsn.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.bz2
Patch1:		amsn-0.98.4-defaultplugins.patch
Patch2:		amsn-0.98.4-contact_list_extension.patch
Patch3:		amsn-0.98.4-linkage.patch
Patch4:		amsn-0.98.4-fix_file_locations.patch
Patch5:		amsn-0.98.4-disable_version_check_on_startup.patch
Patch6:		amsn-0.98.4-amsnplus_flags.patch
Patch7:		amsn-0.98.4-kernel-2.6.38.patch
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
BuildRequires:	libimlib-devel
BuildRequires:	libice-devel
BuildRequires:	libsm-devel
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
Requires:	tcltls
Requires:	gstreamer0.10-plugins-bad
Requires:	gstreamer0.10-farsight2

%if %mdkversion >= 201000
Requires:	libnice-utils
%else
Requires:	libnice
%endif

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
%setup -q -n %{name}-%{version}
%patch1 -p0 -b .defaultplugins
%patch2 -p1 -b .contact_list_extension
%patch3 -p1 -b .link
%patch4 -p0 -b .locations
%patch5 -p0 -b .version_check
%patch6 -p0 -b .flags
%patch7 -p0 -b .kernel

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
rm -rf %{buildroot}
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
