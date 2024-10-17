%define         oe_rel 20130126-002033
Name:           openerp-client
Version:        6.1
Release:        5.%(echo %{oe_rel} | tr '-' '_')
                # See LICENSING
License:        AGPLv3 and GPLv3+ and LGPLv3+
Group:          Databases
Summary:        Business Applications Server Client
URL:            https://www.openerp.com
#Source0:        http://nightly.openerp.com/%%{version}/releases/%%{name}-%%{version}-1.tar.gz
Source0:        http://nightly.openerp.com/%{version}/nightly/src/%{name}-%{version}-%{oe_rel}.tar.gz

Source1:        %{name}.desktop
Source2:        %{name}-licensing
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  python-libxslt
BuildRequires:  pkgconfig(pygtk-2.0)
BuildRequires:  python-setuptools
BuildRequires:  python-devel
BuildRequires:  python-hippo-canvas

Requires:       hicolor-icon-theme
Requires:       python-egenix-mx-base
Requires:       pygtk2.0-libglade
Requires:       python-dateutil
Requires:       python-lxml
Requires:       python-matplotlib
Requires:       python-hippo-canvas

%description
Gtk client for Open ERP.

OpenERP is a free Enterprise Resource Planning and Customer Relationship
Management software. It is mainly developed to meet changing needs.

This package only contains the thin, native client for the ERP application.
After installing this, you will be able to connect to any OpenERP server
running in your local network or the Internet.

%prep
%setup -q -n %{name}-%{version}-%{oe_rel}

# Remove bundled stuff and foreign packaging
rm -f setup.nsi
rm -rf bin/SpiffGtkWidgets
sed -i '/SpiffGtkWidgets/d' setup.py
#rm -f msgfmt.py

sed -i -e '\;/usr/bin/env;d' bin/release.py bin/%{name}.py
sed -i -e 's/\r//' doc/README* doc/License.rtf
chmod 644 doc/License.rtf

%build
PYTHONPATH=%{_bindir} %{__python} ./setup.py --quiet build

%install
PYTHONPATH=%{_bindir} \
    %{__python} ./setup.py --quiet install --root=%{buildroot}

rm -rf %{buildroot}%{_docdir}/*
rm doc/INSTALL
cp %{SOURCE2} doc

install -m 644 -D bin/pixmaps/openerp-icon.png \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
# https://bugs.launchpad.net/bugs/994216
# Adjusting locale names for Albania, Ukraine
pushd %{buildroot}/%{_datadir}/locale
    mv al sq
    rm -r ua # there is already an "uk" file for Ukraine, ua seems old.
popd

mkdir %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir  %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

%find_lang %{name}

%post
update-desktop-database %{_datadir}/applications > /dev/null || :
touch --no-create %{_datadir}/icons &>/dev/null || :

%postun
update-desktop-database %{_datadir}/applications > /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :

%files -f %{name}.lang
%doc doc/*
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{python_sitelib}/%{name}
%{python_sitelib}/openerp_client*egg-info
