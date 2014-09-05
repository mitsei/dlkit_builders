
class Locale:

    init = """
    ##
    # This constructor should probably be referencing a locale settings 
    # module for default values.
    def __init__(self, language_type_identifier = 'ENG', 
                       script_type_identifier = 'LATN', 
                       calendar_type_identifier = 'ISO_8601', 
                       time_type_identifier = 'UTC', 
                       currency_type_identifier = 'USD', 
                       unit_system_type_identifier = 'ENGLISH', 
                       numeric_format_type_identifier = 'F8.2', 
                       calendar_format_type_identifier = 'MMDDYYYY', 
                       time_format_type_type_identifier = 'HHMMSS', 
                       currency_format_type_identifier = 'US', 
                       coordinate_format_type_identifier = 'DMS'
                ):
        
        self._language_type_identifier = language_type_identifier
        self._script_type_identifier = script_type_identifier
        self._calendar_type_identifier = calendar_type_identifier
        self._time_type_identifier = time_type_identifier
        self._currency_type_identifier = currency_type_identifier
        self._unit_system_type_identifier = unit_system_type_identifier
        self._numeric_format_type_identifier = numeric_format_type_identifier
        self._calendar_format_type_identifier = calendar_format_type_identifier
        self._time_format_type_type_identifier =  time_format_type_type_identifier
        self._currency_format_type_identifier = currency_format_type_identifier
        self._coordinate_format_type_identifier = coordinate_format_type_identifier
"""

    get_language_type = """
        from ..locale.types import Language
        from ..type.primitives import Type
        return Type(**Language().get_type_data(self._language_type_identifier))"""

    get_script_type = """
        from ..locale.types import Script
        from ..type.primitives import Type
        return Type(**Script().get_type_data(self._script_type_identifier))"""

    get_calendar_type = """
        from ..locale.types import Calendar
        from ..type.primitives import Type
        return Type(**Calendar().get_type_data(self._calendar_type_identifier))"""

    get_time_type = """
        from ..locale.types import Time
        from ..type.primitives import Type
        return Type(**Time().get_type_data(self._time_type_identifier))"""

    get_currency_type = """
        from ..locale.types import Currency
        from ..type.primitives import Type
        return Type(**Currency().get_type_data(self._currency_type_identifier))"""

    get_unit_system_type = """
        from ..locale.types import UnitSystem
        from ..type.primitives import Type
        return Type(**UnitSystem().get_type_data(self._system_type_identifier))"""

    get_numeric_format_type = """
        from ..locale.types import NumericFormat
        from ..type.primitives import Type
        return Type(**NumericFormat().get_type_data(self._numeric_format_type_identifier))"""

    get_calendar_format_type = """
        from ..locale.types import CalendarFormat
        from ..type.primitives import Type
        return Type(**CalendarFormat().get_type_data(self._calendar_format_type_identifier))"""

    get_time_format_type = """
        from ..locale.types import TimeFormat
        from ..type.primitives import Type
        return Type(**TimeFormat().get_type_data(self._time_format_type_identifier))"""

    get_currency_format_type = """
        from ..locale.types import CurrencyFormat
        from ..type.primitives import Type
        return Type(**CurrencyFormat().get_type_data(self._currency_format_type_identifier))"""

    get_coordinate_format_type = """
        from ..locale.types import CoordinateFormat
        from ..type.primitives import Type
        return Type(**CoordinateFormat().get_type_data(self._coordinate_format_type_identifier))"""


class DisplayText:

    init = """
    ##
    # This constructor should be calling a locale settings module,
    # which should be set to the default language, script and format
    # types. 
    def __init__(self, text, language_type_identifier = 'ENG',
                             script_type_identifier = 'LATN',
                             format_type_identifier = 'PLAIN',
                             language_type = None,
                             script_type = None,
                             format_type = None):
        from ..locale.types import Format
        self._text = text
        if language_type:
            self._language_type = language_type
        else:
            from ..locale.types import Language
            from ..type.primitives import Type
            self._language_type = Type(**Language().get_type_data(
                                      language_type_identifier))
        if script_type:
            self._script_type = script_type
        else:
            from ..locale.types import Script
            from ..type.primitives import Type
            self._script_type = Type(**Script().get_type_data(
                                     script_type_identifier))
        if format_type:
            self._format_type = format_type
        else:
            from ..locale.types import Format
            from ..type.primitives import Type
            self._format_type = Type(**Format().get_type_data(
                                     format_type_identifier))
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
