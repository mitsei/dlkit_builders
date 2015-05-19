
class Locale:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Type',
        'from dlkit.primordium.locale.types import language',
        'from dlkit.primordium.locale.types import script',
        'from dlkit.primordium.locale.types import calendar',
        'from dlkit.primordium.locale.types import time',
        'from dlkit.primordium.locale.types import currency',
        'from dlkit.primordium.locale.types import unit_system',
        'from dlkit.primordium.locale.types import numeric_format',
        'from dlkit.primordium.locale.types import calendar_format',
        'from dlkit.primordium.locale.types import time_format',
        'from dlkit.primordium.locale.types import currency_format',
        'from dlkit.primordium.locale.types import coordinate_format',
    ]

    init = """
    ##
    # This constructor should probably be referencing a locale settings
    # module for default values?
    def __init__(self,
                 language_type_identifier='ENG',
                 script_type_identifier='LATN',
                 calendar_type_identifier='ISO_8601',
                 time_type_identifier='UTC',
                 currency_type_identifier='USD',
                 unit_system_type_identifier='ENGLISH',
                 numeric_format_type_identifier='F8.2',
                 calendar_format_type_identifier='MMDDYYYY',
                 time_format_type_identifier='HHMMSS',
                 currency_format_type_identifier='US',
                 coordinate_format_type_identifier='DMS'):

        self._language_type_identifier = language_type_identifier
        self._script_type_identifier = script_type_identifier
        self._calendar_type_identifier = calendar_type_identifier
        self._time_type_identifier = time_type_identifier
        self._currency_type_identifier = currency_type_identifier
        self._unit_system_type_identifier = unit_system_type_identifier
        self._numeric_format_type_identifier = numeric_format_type_identifier
        self._calendar_format_type_identifier = calendar_format_type_identifier
        self._time_format_type_identifier = time_format_type_identifier
        self._currency_format_type_identifier = currency_format_type_identifier
        self._coordinate_format_type_identifier = coordinate_format_type_identifier
"""

    get_language_type = """
        return Type(**language.get_type_data(self._language_type_identifier))"""

    get_script_type = """
        return Type(**script.get_type_data(self._script_type_identifier))"""

    get_calendar_type = """
        return Type(**calendar.get_type_data(self._calendar_type_identifier))"""

    get_time_type = """
        return Type(**time.get_type_data(self._time_type_identifier))"""

    get_currency_type = """
        return Type(**currency.get_type_data(self._currency_type_identifier))"""

    get_unit_system_type = """
        return Type(**unit_system.get_type_data(self._unit_system_type_identifier))"""

    get_numeric_format_type = """
        return Type(**numeric_format.get_type_data(self._numeric_format_type_identifier))"""

    get_calendar_format_type = """
        return Type(**calendar_format.get_type_data(self._calendar_format_type_identifier))"""

    get_time_format_type = """
        return Type(**time_format.get_type_data(self._time_format_type_identifier))"""

    get_currency_format_type = """
        return Type(**currency_format.get_type_data(self._currency_format_type_identifier))"""

    get_coordinate_format_type = """
        return Type(**coordinate_format.get_type_data(self._coordinate_format_type_identifier))"""


class DisplayText:

    init = """
    ##
    # This constructor should be calling a locale settings module,
    # which should be set to the default language, script and format
    # types. 
    def __init__(self,
                 text,
                 language_type_identifier='ENG',
                 script_type_identifier='LATN',
                 format_type_identifier='PLAIN',
                 language_type=None,
                 script_type=None,
                 format_type=None):
        from ..locale.types import Format
        self._text = text
        if language_type:
            self._language_type = language_type
        else:
            self._language_type = Type(**language.get_type_data(language_type_identifier))
        if script_type:
            self._script_type = script_type
        else:
            self._script_type = Type(**script.get_type_data(script_type_identifier))
        if format_type:
            self._format_type = format_type
        else:
            self._format_type = Type(**format.get_type_data(format_type_identifier))
"""

    get_text = """
        return self._text"""

    get_language_type = """
        return self._language_type
        # This could also be where the get_type functions go, instead of
        # during initialization since consumers will likely not be interested
        # in the locale types as often as they are in the text itself."""

    get_script_type = """
        return self._script_type
        # This could also be where the get_type functions go, instead of
        # during initialization since consumers will likely not be interested
        # in the locale types as often as they are in the text itself."""

    get_format_type = """
        return self._format_type
        # This could also be where the get_type functions go, instead of
        # during initialization since consumers will likely not be interested
        # in the locale types as often as they are in the text itself."""

class LocaleList:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
    ]

    get_next_locale = """
        try:
            next_item = self.next()
        except StopIteration:
            raise errors.IllegalState('no more elements available in this list')
        except: #Need to specify exceptions here
            raise errors.OperationFailed()
        else:
            return next_item

    def next(self):
        next_item = osid_objects.OsidList.next(self)
        return Locale(next_item)"""
