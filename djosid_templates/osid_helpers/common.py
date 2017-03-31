# -*- coding: utf-8 -*-

# This module contains simple implementation of common osid services
# that are used by many other service definitions.  It exists so as to
# allow DLKit developers and deployers to stand up the least number of
# django-aware service kits neccessary to support consumer application
# functionality.  The minimum should consist of any service kits being
# directly used plus the osid_kit. It is recommended that in a production
# implementation all required django service implementations be installed

from ..osid import markers as osid_markers
try:
    from ..abstract_osid.id.primitives import Id as abc_id
except:
    # For now ignore abc inheritance if abstract package doesn't exist.
    # This will probably come back to bite
    abc_id = object
try:
    from ..abstract_osid.type.primitives import Type as abc_type
except:
    # Refer to last note
    abc_type = object
try:
    from ..abstract_osid.locale.primitives import DisplayText as abc_displaytext
except:
    # Refer to last note
    abc_locale = object
try:
    from ..abstract_osid.installation.primitives import Version as abc_version
except:
    # Refer to last note
    abc_version = object


class Id(abc_id, osid_markers.OsidPrimitive):

    def __init__(self, authority, namespace, identifier):
        self._authority = authority
        self._namespace = namespace
        self._identifier = identifier

    def get_authority(self):
        return self._authority

    def get_identifier_namespace(self):
        return self._namespace

    def get_identifier(self):
        return self._identifier


class Type(abc_type, osid_markers.OsidPrimitive):

    def __init__(self,
                 authority,
                 namespace,
                 identifier,
                 display_name='',
                 display_label='',
                 description='',
                 domain=''):

        self._authority = authority
        self._namespace = namespace
        self._identifier = identifier
        self._display_name = display_name
        self._display_label = display_label
        self._description = description
        self._domain = domain

    def get_display_name(self):
        return DisplayText(self._display_name)

    def get_display_label(self):
        from locale_kit.dj_locale.primitives import DisplayText
        return DisplayText(self._display_label)

    def get_description(self):
        return DisplayText(self._description)

    def get_domain(self):
        return DisplayText(self._domain)

    def get_authority(self):
        return self._authority

    def get_identifier_namespace(self):
        return self._namespace

    def get_identifier(self):
        return self._identifier


class DisplayText(abc_displaytext, osid_markers.OsidPrimitive):
    # Unless types are explicitely provided, This common DisplayText
    # implementation will only built the default language, script and format
    # types as defined in the profile. So language_type_identifier,
    # script_type_identifier, and format_type_identifier will be ignored.
    def __init__(self,
                 text,
                 language_type_identifier=None,
                 script_type_identifier=None,
                 format_type_identifier=None,
                 language_type=None,
                 script_type=None,
                 format_type=None):
        from osid_kit.dj_osid import profile
        try:
            from type_kit.dj_type.primitives import Type
        except:
            pass
        self._text = text
        if language_type:
            self._language_type = language_type
        else:
            self._language_type = Type(**profile.LANGUAGETYPE)
        if script_type:
            self._script_type = script_type
        else:
            self._script_type = Type(**profile.SCRIPTTYPE)
        if format_type:
            self._format_type = format_type
        else:
            self._format_type = Type(**profile.FORMATTYPE)

    def get_language_type(self):
        return self._language_type

    def get_script_type(self):
        return self._script_type

    def get_format_type(self):
        return self._format_type

    def get_text(self):
        return self._text

"""
class Version(abc_version, osid_markers.OsidPrimitive):

    def __init__(self, components, scheme = None):
        try:
            from type_kit.dj_type.primitives import Type
        except:
            pass
        self._components = components
        if scheme:
            self._scheme = scheme
        else:
            from osid_kit.dj_osid.types import Generic
            self._scheme = Type(**Generic.get_type_data('UNKNOWN'))

    def get_components(self):
        return self._components

    def get_scheme(self):
        return self._scheme
"""
