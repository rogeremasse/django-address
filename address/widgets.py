import sys

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.template.loader import render_to_string

from .models import Address

if sys.version > '3':
    long = int
    basestring = (str, bytes)
    unicode = str

USE_DJANGO_JQUERY = getattr(settings, 'USE_DJANGO_JQUERY', False)
JQUERY_URL = getattr(settings, 'JQUERY_URL', 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js')
ADDRESS_COMPONENTS_TEMPLATE = getattr(settings, 'ADDRESS_COMPONENTS_TEMPLATE', 'address/address_components.html')

class AddressWidget(forms.TextInput):
    components = [('country', 'country'), ('country_code', 'country_short'),
                  ('locality', 'locality'), ('sublocality', 'sublocality'),
                  ('postal_code', 'postal_code'), ('route', 'route'),
                  ('street_number', 'street_number'),
                  ('state', 'administrative_area_level_1'),
                  ('state_code', 'administrative_area_level_1_short'),
                  ('formatted', 'formatted_address'),
                  ('latitude', 'lat'), ('longitude', 'lng')]

    class Media:
        """Media defined as a dynamic property instead of an inner class."""
        js = [
            'https://maps.googleapis.com/maps/api/js?libraries=places&key=%s' % settings.GOOGLE_API_KEY,
            'js/jquery.geocomplete.min.js',
            'address/js/address.js',
        ]

        if JQUERY_URL:
            js.insert(0, JQUERY_URL)
        elif JQUERY_URL is not False:
            vendor = '' if django.VERSION < (1, 9, 0) else 'vendor/jquery/'
            extra = '' if settings.DEBUG else '.min'

            jquery_paths = [
                '{}jquery{}.js'.format(vendor, extra),
                'jquery.init.js',
            ]

            if USE_DJANGO_JQUERY:
                jquery_paths = ['admin/js/{}'.format(path) for path in jquery_paths]

            js.extend(jquery_paths)

    def __init__(self, *args, show_address_components=False, **kwargs):
        attrs = kwargs.get('attrs', {})
        classes = attrs.get('class', '')
        classes += (' ' if classes else '') + 'address'
        attrs['class'] = classes
        kwargs['attrs'] = attrs
        self.show_address_components = show_address_components
        super(AddressWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):

        # Can accept None, a dictionary of values or an Address object.
        if value in (None, ''):
            ad = {}
        elif isinstance(value, dict):
            ad = value
        elif isinstance(value, (int, long)):
            ad = Address.objects.get(pk=value)
            ad = ad.as_dict()
        else:
            ad = value.as_dict()

        # Generate the elements. We should create a suite of hidden fields
        # For each individual component, and a visible field for the raw
        # input. Begin by generating the raw input.
        elems = [super(AddressWidget, self).render(name, ad.get('formatted', None), attrs, **kwargs)]

        if self.show_address_components:
            # add a table containing the address components
            context = {"name": name, "components": dict(self.components)}
            html = get_template(ADDRESS_COMPONENTS_TEMPLATE).render(context) or None
            if html:
                elems.append(html)
        else:
            # add components as hidden fields.
            elems.append('<div id="%s_components">' % name)
            for com in self.components:
                elems.append('<input type="hidden" name="%s_%s" data-geo="%s" value="%s" />' % (
                    name, com[0], com[1], ad.get(com[0], ''))
                )
            elems.append('</div>')


        return mark_safe(unicode('\n'.join(elems)))

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, '')
        if not raw:
            return raw
        ad = dict([(c[0], data.get(name + '_' + c[0], '')) for c in self.components])
        ad['raw'] = raw
        return ad
