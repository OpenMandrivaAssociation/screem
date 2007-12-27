%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

Summary:	Site CReating and Editing EnvironMent
Name:		screem
Version:	0.16.1
Release:	%mkrel 4
License:	GPLv2+ and GFDL
Group:		Editors
URL:		http://www.screem.org/
Source0:	http://prdownloads.sourceforge.net/screem/%{name}-%{version}.tar.gz
# (fc) 0.6.2-2mdk fix dtd location in help file
Patch0:		screem-0.14.1-docbooklocation.patch
# (lenny) 0.9.3-2mdk use system wide intltool
Patch1:		screem-intltool.patch
Patch2:		fix_miscompile.patch
Patch3:		screem-0.16.1-desktop-file.patch
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Requires(post): GConf2 >= 2.3.3
Requires(preun): GConf2 >= 2.3.3
Requires:	dbus-x11
BuildRequires:	GConf2 >= 2.3.3
BuildRequires:	ImageMagick
BuildRequires:	dbus-devel
BuildRequires:	gettext
BuildRequires:	gnome-menus-devel
BuildRequires:	gtkhtml2-devel
#BuildRequires:	gtksourceview-devel >= 1.1.90 ?
BuildRequires:	gtksourceview1-devel
BuildRequires:	intltool
BuildRequires:	krb5-devel
BuildRequires:	krb5-server
BuildRequires:	libcroco0.6-devel
BuildRequires:	libglade2.0-devel >= 2.3.0
BuildRequires:	libgnome-menu-devel
BuildRequires:	libgnomeprintui-devel >= 2.2.0
BuildRequires:	libgnomeui2-devel >= 2.2.0
BuildRequires:	libgtkhtml2-devel >= 2.2.0
BuildRequires:	libxml2-devel >= 2.4.3
BuildRequires:	perl(XML::Parser)
BuildRequires:	scrollkeeper
BuildRequires:	popt-devel
Conflicts:	%{name}-devel < 0.16.1-3
%if %build_plf
BuildRequires:	socks5-devel
%endif

%description
SCREEM (Site CReating and Editing EnvironMent) is an integrated development
environment for the creation and maintenance of websites and pages. It is
not a WYSIWYG editor; you are provided with raw html source in its editor
window instead.

Build options:
--with plf	Enable socks V5 support

%package	devel
Summary:	Development files for %{name}
Group:		Development/C
Conflicts:	%{name} < 0.16.1-3

%description	devel
Development files for %{name}

%prep
%setup -q
%patch0 -p1 -b .docbooklocation
%patch1 -p1 -b .intlsystemwide
%patch2	-p1
%patch3 -p0 -b .desktop

# fix build
perl -pi -e "s|-DGTK_DISABLE_DEPRECATED -DGNOME_DISABLE_DEPRECATED -DGNOMEUI_DISABLE_DEPRECATED||g" configure*

%build
rm -f configure; autoreconf

%configure2_5x \
%if %build_plf
    --with-socks=yes \
%else
    --with-socks=no \
%endif
    --disable-schemas-install \
    --disable-update-mime \
    --disable-update-desktop \
    --enable-dbus

%make

%install
rm -rf %{buildroot}

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 -D screem.png       %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert screem.png -geometry 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert screem.png -geometry 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%find_lang %{name} --with-gnome

%clean
rm -rf %{buildroot}

%define schemas screem

%post
%{update_scrollkeeper}
%post_install_gconf_schemas %{schemas}
%{update_menus}
%{update_icon_cache hicolor}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%{clean_menus}
%{clean_scrollkeeper}
%{clean_icon_cache hicolor}

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%{_sysconfdir}/gconf/schemas/screem.schemas
%{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/*.so
%{_datadir}/application-registry/*.applications
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*
%{_datadir}/omf/*
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/%{name}/plugins/*.la
%{_libdir}/pkgconfig/*.pc
