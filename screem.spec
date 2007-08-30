%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

%define iconname %{name}.png

Summary:	Site CReating and Editing EnvironMent
Name:		screem
Version:	0.16.1
Release:	%mkrel 1
License:	GPL
Group:		Editors
URL:		http://www.screem.org/
Source0:	http://prdownloads.sourceforge.net/screem/%{name}-%{version}.tar.gz
# (fc) 0.6.2-2mdk fix dtd location in help file
Patch0:		screem-0.14.1-docbooklocation.patch
# (lenny) 0.9.3-2mdk use system wide intltool
Patch1:		screem-intltool.patch
Patch2:		fix_miscompile.patch
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Requires(post): GConf2 >= 2.3.3
Requires(preun): Conf2 >= 2.3.3
Requires:	dbus-x11
BuildRequires:	GConf2 >= 2.3.3
BuildRequires:	ImageMagick
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
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
%if %build_plf
BuildRequires:	socks5-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%description	devel
Development files for %{name}

%prep

%setup -q
%patch0 -p1 -b .docbooklocation
%patch1 -p1 -b .intlsystemwide
%patch2	-p1

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
%doc AUTHORS BUGS COPYING COPYING-DOCS ChangeLog NEWS README TODO
%{_sysconfdir}/gconf/schemas/screem.schemas
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/application-registry/*.applications
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*
%{_datadir}/omf/*
%{_datadir}/pixmaps/*
%{_datadir}/%{name}

# menu
%{_menudir}/%{name}
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/%{name}/plugins/*.la
%{_libdir}/pkgconfig/*.pc
