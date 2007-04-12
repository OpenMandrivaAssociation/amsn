Summary:	MSN Messenger clone for Linux
Summary(fr):	Clône MSN Messenger pour Linux
Summary(de):	MSN Messenger-Klon für Linux
Name:		amsn
Version:	0.96
Release:	%mkrel 2
License:	GPL
Group:		Networking/Instant messaging
URL:		http://amsn.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/amsn/amsn-%{version}.tar.bz2
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
Requires:	tk >= 8.4.2
Requires:	%{mklibname tcltls 1.50}
Requires:       soundwrapper
BuildRoot:	%{_tmppath}/buildroot-%{name}-%{version}

%description
This is Tcl/Tk clone that implements the Microsoft Messenger (MSN) for
Unix,Windows, or Macintosh platforms. It supports file transfers,
groups, and many more features. Visit http://amsn.sourceforge.net/ for
details. This is an ongoing project, and it is already going pretty
well.

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

%setup -q -n amsn-%{version}
%patch0 -p0 -b .www-browser

bzcat %{SOURCE2} > amsn.startup

# lib64 fixes
perl -pi -e "s|/usr/lib/|%{_libdir}|g" configure*
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*
perl -pi -e "s|^set libtls .*|set libtls \"%{_libdir}/tls1.50\"|g" amsn

%build
rm -f configure
libtoolize --copy --force; aclocal-1.7; autoconf --force

%configure2_5x

%make

%install
rm -rf %{buildroot}

%make \
    INSTALL_PREFIX=%{buildroot} \
    rpm-install

install -d %{buildroot}%{_bindir}
rm -f %{buildroot}%{_bindir}/amsn
install -m0755 amsn.startup %{buildroot}%{_bindir}/amsn

# fix softlinks
pushd %{buildroot}%{_bindir}
    ln -snf %{_datadir}/amsn/amsn-remote amsn-remote
    ln -snf %{_datadir}/amsn/amsn-remote-CLI amsn-remote-CLI
popd

# mimic the previous version somewhat
install -d %{buildroot}%{_datadir}/pixmaps
install -m0644 icons/48x48/msn.png %{buildroot}%{_datadir}/pixmaps/msn.png

ln -sf %{_docdir}%{name}-%{version}/README %{buildroot}%{_datadir}/amsn/README
ln -sf %{_docdir}%{name}-%{version}/HELP %{buildroot}%{_datadir}/amsn/HELP

# Menu
install -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): command="%{_bindir}/%{name}" needs="X11" \
icon="%{name}.png" section="Internet/Instant Messaging" \
title="aMSN" longtitle="MSN clone" xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Network" \
  --add-category="InstantMessaging" \
  --add-category="X-MandrivaLinux-Internet-InstantMessaging" \
  --dir $RPM_BUILD_ROOT%{_datadir}/amsn $RPM_BUILD_ROOT%{_datadir}/amsn/amsn.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp  $RPM_BUILD_ROOT%{_datadir}/amsn/amsn.desktop $RPM_BUILD_ROOT%{_datadir}/applications/amsn.desktop

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 icons/128x128/aMSN_128.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 icons/128x128/aMSN_128.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 icons/128x128/aMSN_128.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

# cleanup
rm -rf %{buildroot}%{_datadir}/amsn/HELP
rm -rf %{buildroot}%{_datadir}/amsn/README
rm -f %{buildroot}%{_datadir}/amsn/sndplay

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AGREEMENT CREDITS FAQ GNUGPL HELP README TODO
%{_bindir}/amsn
%{_bindir}/amsn-remote
%{_bindir}/amsn-remote-CLI
%dir %{_datadir}/amsn
%{_datadir}/amsn/
%{_datadir}/applications/amsn.desktop
%{_menudir}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/pixmaps/*




