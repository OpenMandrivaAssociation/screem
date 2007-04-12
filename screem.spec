%define	name	screem
%define	version	0.14.1
%define rel	10
%define	release	%mkrel %{rel}

%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

%define iconname %{name}.png

Summary:	Site CReating and Editing EnvironMent
Name:		screem
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Editors
URL:		http://www.screem.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		%{name}-%{version}.tar.bz2
# (fc) 0.6.2-2mdk fix dtd location in help file
Patch0:		screem-0.14.1-docbooklocation.patch
# (lenny) 0.9.3-2mdk use system wide intltool
Patch1:		screem-intltool.patch
Patch3:		screem-0.14.1-gnome-2.11-build-fix.patch
# (fc) 0.14.1-10mdv don't use deprecated dbus api
Patch4:		screem-0.14.1-deprecated.patch

BuildRequires:	ImageMagick
BuildRequires:	gtksourceview-devel >= 0.3.0
BuildRequires:	libgnomeui2-devel >= 2.2.0
BuildRequires:	libglade2.0-devel
BuildRequires:	libgtkhtml2-devel >= 2.2.0
BuildRequires:	libgnomeprintui-devel >= 2.2.0
BuildRequires:	libgnome-menu-devel
# (abel) external neon support is quite broken? use bundled one instead
#BuildRequires:	neon-devel >= 0.24.0
BuildRequires:	scrollkeeper
BuildRequires:	krb5-devel
BuildRequires:	intltool libcroco0.6-devel
BuildRequires:	dbus-devel
BuildRequires:  desktop-file-utils
# hell
BuildRequires:	krb5-server
%if %build_plf
BuildRequires:	socks5-devel
%endif
Requires(post):		scrollkeeper
Requires(postun):	scrollkeeper
Requires(post):		GConf2 >= 2.3.3
Requires(preun):	GConf2 >= 2.3.3
Requires: dbus-x11

%description
SCREEM (Site CReating and Editing EnvironMent) is an integrated development
environment for the creation and maintenance of websites and pages. It is
not a WYSIWYG editor; you are provided with raw html source in its editor
window instead.

Build options:
--with plf	Enable socks V5 support

%prep
%setup -q
%patch0 -p1 -b .docbooklocation
%patch1 -p1 -b .intlsystemwide
%patch3 -p1 -b .gnome211
%patch4 -p1 -b .deprecated

%build
%configure2_5x \
%if %build_plf
	--with-socks=yes \
%else
	--with-socks=no \
%endif
	--with-ssl=yes \
	--with-included-neon=yes \
	--disable-update-mime \
	--disable-update-desktop

%make

%install
rm -rf %{buildroot}

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# icons
mkdir -p %{buildroot}%{_miconsdir} \
         %{buildroot}%{_iconsdir}
install -m 644 -D screem.png       %{buildroot}%{_liconsdir}/%{iconname}
convert screem.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{iconname}
convert screem.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{iconname}

# menu
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
    command="%{_bindir}/screem" \
    icon="%{iconname}" \
    title="Screem" \
    longtitle="Website creation environment" \
    needs="X11" \
    section="Internet/Web Editors" \
    xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Internet-WebEditors" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%find_lang %{name} --with-gnome

# remove unwanted files
rm -f %{buildroot}%{_libdir}/%{name}/plugins/*.la

%clean
rm -rf %{buildroot}

%define schemas screem

%post
%update_scrollkeeper
%post_install_gconf_schemas %{schemas}
%update_menus

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%clean_menus
%clean_scrollkeeper

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING TODO BUGS
%{_sysconfdir}/gconf/schemas/screem.schemas
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/application-registry/*.applications
%{_datadir}/applications/*.desktop
%{_datadir}/mime-info/*
%{_datadir}/mime/*
%{_datadir}/omf/*
%{_datadir}/pixmaps/*
%{_datadir}/%{name}

# menu
%{_menudir}/%{name}
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png

