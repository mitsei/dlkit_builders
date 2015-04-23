import datetime
from ..abstract_osid.osid import markers as abc_osid_markers
from ..abstract_osid.id.primitives import Id as abc_id
from ..abstract_osid.type.primitives import Type as abc_type
from ..abstract_osid.locale.primitives import DisplayText as abc_displaytext
from ..abstract_osid.installation.primitives import Version as abc_version
from ..abstract_osid.calendaring import primitives as abc_calendaring_primitives
from ..abstract_osid.mapping import primitives as abc_mapping_primitives
from ..abstract_osid.transport import objects as abc_transport_objects
from . import types

from .osid_errors import *

class OsidPrimitive(abc_osid_markers.OsidPrimitive):
    """A marker interface for an interface that behaves like a language primitive.

    Primitive types, such as numbers and strings, do not encapsulate
    behaviors supplied by an OSID Provider. More complex primitives are
    expressed through interface definitions but are treated in a similar
    fashion as a language primitive. OSID Primitives supplied by an OSID
    Consumer must be consumable by any OSID Provider.

    """
    
    def _test_escape(self):
        print self._unescape(self._escape("here:there@okapia.net")) == "here:there@okapia.net"
        print self._unescape(self._escape("here:there/somewhere@okapia.net")) == "here:there/somewhere@okapia.net"
        print self._unescape(self._escape("here:there%3asomewhere@okapia.net")) == "here:there%3asomewhere@okapia.net"
        print self._unescape(self._escape("almost%3ahere:there%3asomewhere@okapia.net")) == "almost%3ahere:there%3asomewhere@okapia.net"
        print self._unescape(self._escape("almost%3ahere:there%3asomewhere@okapia.net")) == "almost%3ahere:there%3asomewhere@okapia.net"
        print self._unescape(self._escape("almost%3ahere:there%3asomewhere%40else@okapia.net")) == "almost%3ahere:there%3asomewhere%40else@okapia.net"
        print self._unescape(self._escape("almost%3ahere:there%3asomewhere%40else@site%40okapia.net")) == "almost%3ahere:there%3asomewhere%40else@site%40okapia.net"
        print self._unescape(self._escape("almost%3ahere:there%3asomewhere%40else@our%3asite%40okapia.net")) == "almost%3ahere:there%3asomewhere%40else@our%3asite%40okapia.net"
        print self._unescape(self._escape("al!#$<>;^&*()_+|}{?//-=most%3ahere:there%3asome!#$<>;^&*()_+|}{?//-=where%40else@our%3asite%40ok!#$<>;^&*()_+|}{?//-=apia")) == "al!#$<>;^&*()_+|}{?//-=most%3ahere:there%3asome!#$<>;^&*()_+|}{?//-=where%40else@our%3asite%40ok!#$<>;^&*()_+|}{?//-=apia"


class Id(abc_id, OsidPrimitive):

    def __init__(self, idstr=None, authority=None, namespace=None, identifier=None):
        self._idstr = idstr
        if idstr is not None:
            idstr = self._unescape(idstr)
            self._authority = self._unescape(idstr.split('@')[-1])
            self._namespace = self._unescape(idstr.split(':')[0])
            self._identifier = self._unescape(idstr.split('@')[0].split(':')[-1])
        elif authority is not None and namespace is not None and identifier is not None:
            self._authority = authority
            self._namespace = namespace
            self._identifier = identifier
        else:
            raise NullArgument()
    
    def __str__(self):
        if self._idstr is not None:
            return self._idstr
        else:
            return super(Id, self).__str__()

    def get_authority(self):
        return self._authority

    def get_identifier_namespace(self):
        return self._namespace

    def get_identifier(self):
        return self._identifier

    authority = property(get_authority)
    identifier_namespace = property(get_identifier_namespace)
    namespace = property(get_identifier_namespace)
    identifier = property(get_identifier)

class Type(abc_type, OsidPrimitive):

    def __init__(self, idstr=None,
                       identifier=None,
                       authority=None,
                       namespace=None,
                       display_name='',
                       display_label='',
                       description='',
                       domain='',
                       **kwargs):
        if (idstr is not None and display_name is not None and 
            description is not None and domain is not None):
            idstr = self._unescape(idstr)
            self._authority = self._unescape(idstr.split('@')[-1])
            self._namespace = self._unescape(idstr.split(':')[0])
            self._identifier = self._unescape(idstr.split('@')[0].split(':')[-1])
        elif (authority is not None and namespace is not None and identifier is not None and
            display_name is not None and description is not None and domain is not None):
            self._authority = authority
            self._namespace = namespace
            self._identifier = identifier
        else:
            raise NullArgument()
        self._display_name = display_name
        self._display_label = display_label
        self._description = description
        self._domain = domain
    
    def get_display_name(self):
        return DisplayText(text = self._display_name,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))

    def get_display_label(self):
        return DisplayText(text = self._display_label,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))

    def get_description(self):
        return DisplayText(text = self._description,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))

    def get_domain(self):
        return DisplayText(text = self._domain,
                           language_type = Type(**types.Language().get_type_data('DEFAULT')),
                           script_type = Type(**types.Script().get_type_data('DEFAULT')),
                           format_type = Type(**types.Format().get_type_data('DEFAULT')))

    def get_authority(self):
        return self._authority

    def get_identifier_namespace(self):
        return self._namespace

    def get_identifier(self):
        return self._identifier

    display_name = property(get_display_name)
    display_label = property(get_display_label)
    description = property(get_description)
    domain = property(get_domain)
    authority = property(get_authority)
    identifier_namespace = property(get_identifier_namespace)
    namespace = property(get_identifier_namespace)
    identifier = property(get_identifier)


class DisplayText(abc_displaytext, OsidPrimitive):

    def __init__(self, display_text_map=None, text=None, language_type=None, script_type=None, format_type=None):
        if display_text_map is not None:
            self._unfold_map(display_text_map)
        elif (text is not None and language_type is not None and
            script_type is not None and format_type is not None):
            self._text = text
            self._language_type = language_type
            self._script_type = script_type
            self._format_type = format_type
        else:
            raise NotFound()

    def _unfold_map(self, display_text_map):
        from .locale import types as locale_types
        lt_identifier = Id(display_text_map['languageTypeId']).get_identifier()
        st_identifier = Id(display_text_map['scriptTypeId']).get_identifier()
        ft_identifier = Id(display_text_map['formatTypeId']).get_identifier()
        try:
            self._language_type = Type(**locale_types.Language().get_type_data(lt_identifier))
        except AttributeError:
            raise NotFound('Language Type: ' + lt_identifier) # or move on to another source
        try:
            self._script_type = Type(**locale_types.Script().get_type_data(st_identifier))
        except AttributeError:
            raise NotFound('Script Type: ' + st_identifier) # or move on to another source
        try:
            self._format_type = Type(**locale_types.Format().get_type_data(ft_identifier))
        except AttributeError:
            raise NotFound('Format Type: ' + ft_identifier) # or move on to another source
        self._text = display_text_map['text']
        

    def get_language_type(self):
        return self._language_type

    def get_script_type(self):
        return self._script_type

    def get_format_type(self):
        return self._format_type

    def get_text(self):
        return self._text

    language_type = property(get_language_type)
    script_type = property(get_script_type)
    format_type = property(get_format_type)
    text = property(get_text)


class DataInputStream(abc_transport_objects.DataInputStream):
    """The data input stream provides a means for reading data from a stream."""

    def __init__(self, input_data):
        self._my_data = input_data

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('__'):
                yield attr

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, name):
        if not name.startswith('__'):
            try:
                return getattr(self._my_data, name)
            except:
                raise

    def at_end_of_stream(self):
        """Tests if the end of this stream has been reached.

        This may not be a permanent condition as more data may be
        available at a later time as in the case of tailing a file.

        return: (boolean) - ``true`` if the end of this stream has been
                reached, ``false`` otherwise
        raise:  IllegalState - this stream has been closed
        *compliance: mandatory -- This method must be implemented.*

        """
        pass

    def available(self):
        """Gets the number of ``bytes`` available for retrieval.

        The number returned by this method may be less than or equal to
        the total number of ``bytes`` in this stream.

        return: (cardinal) - the number of ``bytes`` available for
                retrieval
        raise:  IllegalState - this stream has been closed
        *compliance: mandatory -- This method must be implemented.*

        """
        pass

    def skip(self, n=None):
        """Skips a specified number of ``bytes`` in the stream.

        arg:    n (cardinal): the number of ``bytes`` to skip
        return: (cardinal) - the actual number of ``bytes`` skipped
        raise:  IllegalState - this stream has been closed or
                ``at_end_of_stream()`` is ``true``
        *compliance: mandatory -- This method must be implemented.*

        """
        if self._my_data.closed or self.at_end_of_stream():
            raise IllegalState()
        if n is not None:
            self._my_data.seek(n)

    ##
    # The following two methods stray from the spec:

    def read_to_buffer(self, buf=None, n=None):
        """Reads a specified number of ``bytes`` from this stream.

        arg:    buf (byte[]): the buffer in which the data is read
        arg:    n (cardinal): the number of ``bytes`` to read
        return: (integer) - the actual number of ``bytes`` read
        raise:  IllegalState - this stream has been closed or
                ``at_end_of_stream()`` is ``true``
        raise:  InvalidArgument - the size of ``buf`` is less than ``n``
        raise:  NullArgument - ``buf`` is ``null``
        raise:  OperationFailed - unable to complete request
        *compliance: mandatory -- This method must be implemented.*

        """
        if buf is None:
            raise NullArgument()
        if self._my_data.closed or self.at_end_of_stream():
            raise IllegalState()
        initial_buf_len = len(buf)
        buf.append(self._my_data.read(size = n))
        return len(buf) - initial_buf_len

    def read(self, n=None):
        """Reads a specified number of ``bytes`` from this stream.

        arg:    n (cardinal): the number of ``bytes`` to read
        return: (integer) - the ``bytes`` read
        raise:  IllegalState - this stream has been closed or
                ``at_end_of_stream()`` is ``true``
        raise:  InvalidArgument - the size of ``buf`` is less than ``n``
        raise:  OperationFailed - unable to complete request
        *compliance: mandatory -- This method must be implemented.*

        """
        return self._my_data.read(size = n)

    def close(self):
        """Closes this stream and frees up any allocated resources.

        Methods in this object may not be invoked after this method is
        called.

        raise:  IllegalState - this stream has been closed
        *compliance: mandatory -- This method must be implemented.*

        """
        if self._my_data.closed:
            raise IllegalState()
        self._my_data.close()


class Version(abc_version, OsidPrimitive):
    """A ``Version`` represents a version in a scheme."""

    def __init__(self, components=None):
        if components is None:
            self._components =[]
        elif isinstance(components, list):
            self._components = components
        else:
            raise InvalidArgument()

    def get_scheme(self):
        """Gets the versioining scheme as a type.

        :return: the versioning scheme type
        :rtype: ``osid.type.Type``


        *compliance: mandatory -- This method must be implemented.*

        """
        return # osid.type.Type

    scheme = property(fget=get_scheme)

    def get_components(self):
        """Gets the components of the version.

        In a major.minor[.maintenance[.build]] scheme, an example is {3,
        0, 0}.

        :return: the version components
        :rtype: ``string``


        *compliance: mandatory -- This method must be implemented.*

        """
        return self._components

    components = property(fget=get_components)



class DateTime(datetime.datetime, abc_calendaring_primitives.DateTime, OsidPrimitive):
    """The DateTime interface defines a date and/or time.

    This interface provides a very broad range of dates, describes more
    or less precision, and/or conveys an uncertainty. A number of
    convenience methods for retrieving time elements are available but
    only those methods covered by the specified granularity are valid.

    A typical example is describing a day where the time isn't known,
    and the event did not occur at midnight.
      getMillennium() == 2
      getCentury() == 18
      getYear() == 1776
      getMonth() == 7
      getDay() == 4
      getHour() == 0
      getGranularity() == DateTimeResolution.DAY
      definesUncertainty() == false
    

    
    Another example showing that the time is probably 1pm but could have
    been as late as 3pm or early as noon.
      getMillennium() == 3
      getCentury() == 21
      getYear() == 2008
      getMonth() == 3
      getDay() == 17
      getHour() == 13
      getMinute() == 0
      getGranularity() == TimeResolution.MINUTE
      definesUncertainty() == true
      getUncertaintyGranularity() == DateTimeResolution.HOUR
      getUncertaintyMinus() == 1
      getUncertaintyPlus == 2
    

    
    An example marking the birth of the universe. 13.73 billion years
    +/- 120 million years. The granularity suggests that no more
    resolution than one million years can be inferred from the "clock",
    making errors in the exact number of millennia insignificant.
      getEpoch() == -13,730
      getMillennium() == 0
      getCentury() == 0
      getYear() == 0
      getGranularity() == TimeResolution.EPOCH
      definesUncertainty() == true
      getUncertaintyGranularity() == DateTimeResolution.EPOCH
      getUncertaintyMinus() == 120
      getUncertaintyPlus == 120
    


    """

    def get_calendar_type(self):
        """Gets the calendar type.

        return: (osid.type.Type) - the calendar type
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    calendar_type = property(fget=get_calendar_type)

    def get_aeon(self):
        """Gets the aeon starting from 1.

        An aeon is 1B years.

        return: (integer) - the aeon
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    aeon = property(fget=get_aeon)

    def get_epoch(self):
        """Gets the epoch starting from 1.

        An epoch is 1M years.

        return: (integer) - the eposh
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    epoch = property(fget=get_epoch)

    def get_millennium(self):
        """Gets the millennium starting from 1.

        A millenium is 1,000 years.

        return: (integer) - the millennium
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    millennium = property(fget=get_millennium)

    def get_century(self):
        """Gets the century starting from 1.

        return: (integer) - the century
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    century = property(fget=get_century)

    def get_year(self):
        """Gets the year starting from 1.

        return: (integer) - the year
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    year = property(fget=get_year)

    def get_month(self):
        """Gets the month number starting from 1.

        return: (cardinal) - the month
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    month = property(fget=get_month)

    def get_day(self):
        """Gets the day of the month starting from 1.

        return: (cardinal) - the day of the month
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    day = property(fget=get_day)

    def get_time_type(self):
        """Gets the time type.

        return: (osid.type.Type) - the time type
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    time_type = property(fget=get_time_type)

    def get_hour(self):
        """Gets the hour of the day 0-23.

        return: (cardinal) - the hour of the day
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    hour = property(fget=get_hour)

    def get_minute(self):
        """Gets the minute of the hour 0-59.

        return: (cardinal) - the minute of the hour
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    minute = property(fget=get_minute)

    def get_second(self):
        """Gets the second of the minute 0-59.

        return: (cardinal) - the second of the minute
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    second = property(fget=get_second)

    def get_milliseconds(self):
        """Gets the number of milliseconds in this second 0-999.

        A millisecond is one thousandth of a second.

        return: (cardinal) - the milliseconds of the second
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    milliseconds = property(fget=get_milliseconds)

    def get_microseconds(self):
        """Gets the number of microseconds of the second 0-999.

        A microsecond is one millionth of a second.

        return: (cardinal) - the micrseconds of the millisecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    microseconds = property(fget=get_microseconds)

    def get_nanoseconds(self):
        """Gets the number of nanoseconds of the microsecond 0-999.

        A nanosecond is one billionth of a second.

        return: (cardinal) - the nanoseconds of the microsecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    nanoseconds = property(fget=get_nanoseconds)

    def get_picoseconds(self):
        """Gets the number of picoseconds of the nanosecond 0-999.

        A picosecond is one trillionth of a second.

        return: (cardinal) - the picoseconds of the nanosecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    picoseconds = property(fget=get_picoseconds)

    def get_femtoseconds(self):
        """Gets the number of femtoseconds of the picosecond 0-999.

        A femtosecond is one quadrillionth of a second.

        return: (cardinal) - the femtoseconds of the picosecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    femtoseconds = property(fget=get_femtoseconds)

    def get_attoseconds(self):
        """Gets the number of attoseconds of the femtoseconds 0-999.

        An attosecond is one quintillionth of a second.

        return: (cardinal) - the attoseconds of the femtosecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    attoseconds = property(fget=get_attoseconds)

    def get_zeptoseconds(self):
        """Gets the number of zeptoseconds of the attosecond 0-999.

        A zeptosecond is one sextillionth of a second.

        return: (cardinal) - the zeptoseconds of the attosecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    zeptoseconds = property(fget=get_zeptoseconds)

    def get_yoctoseconds(self):
        """Gets the number of yoctoseconds of the picosecond 0-999.

        A yoctosecond is one septillionth of a second. This is getting
        quite small.

        return: (cardinal) - the yoctoseconds of the picosecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    yoctoseconds = property(fget=get_yoctoseconds)

    def get_xoxxoseconds(self):
        """Gets the number of xoxxoseconds of the yoctosecond 0-999.

        A xoxxosecond is one octillionth of a second. We're going with
        Rudy Rucker here.

        return: (cardinal) - the xoxxoseconds of the yoctosecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    xoxxoseconds = property(fget=get_xoxxoseconds)

    def get_weebleseconds(self):
        """Gets the number of weebleseconds of the xoxxosecond 0-999.

        A weeblesecond is one nonillionth of a second.

        return: (cardinal) - the weebleseconds of the xoxxoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    weebleseconds = property(fget=get_weebleseconds)

    def get_vatoseconds(self):
        """Gets the number of vatoseconds of the xoxxosecond 0-999.

        A vatosecond is one decillionth of a second.

        return: (cardinal) - the vatoseconds of the weeblesecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    vatoseconds = property(fget=get_vatoseconds)

    def get_undaseconds(self):
        """Gets the number of undaseconds of the vatosecond 0-999.

        An undasecond is one unadecillionth of a second.

        return: (cardinal) - the undaseconds of the vatosecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    undaseconds = property(fget=get_undaseconds)

    def get_planck_seconds(self):
        """Gets the number of Plancks of the vatoseconds.

        A Planck is 10 quattuordecillionths of a second.

        return: (cardinal) - the plancks of the undasecond
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    planck_seconds = property(fget=get_planck_seconds)

    def get_granularity(self):
        """Gets the granularity of this time.

        The granularity indicates the resolution of the clock. More
        precision than what is specified in this method cannot be
        inferred from the available data.

        return: (osid.calendaring.DateTimeResolution) - granularity
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    granularity = property(fget=get_granularity)

    def get_granularity_multiplier(self):
        """If the granularity of the time equals ``get_granularity(),`` then the multiplier is 1.

        This method may return a different number when the granularity
        differs from one of the defined resolutions.

        return: (cardinal) - granularity multiplier
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    granularity_multiplier = property(fget=get_granularity_multiplier)

    def defines_uncertainty(self):
        """Tests if uncertainty is defined for this time.

        return: (boolean) - ``true`` if uncertainty is defined,
                ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    def get_uncertainty_units(self):
        """Gets the units of the uncertainty.

        return: (osid.calendaring.DateTimeResolution) - units of the
                uncertainty
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    uncertainty_units = property(fget=get_uncertainty_units)

    def get_uncertainty_minus(self):
        """Gets the uncertainty of this time in the negative direction.

        return: (cardinal) - the uncertainty under this value
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    uncertainty_minus = property(fget=get_uncertainty_minus)

    def get_uncertainty_plus(self):
        """Gets the uncertainty of this time in the positive direction.

        return: (cardinal) - the uncertainty over this value
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    uncertainty_plus = property(fget=get_uncertainty_plus)

    def is_uncertainty_date_inclusive(self):
        """Tests if the uncertainty is inclusive of all dates.

        An inclusive uncertainty includes the entire range specified by
        the uncertainty units e.g. +/- 1 year includes all of the months
        and days within that interval. A non-inclusive uncertainty would
        mean the year is uncertain but the month and day is certain.

        return: (boolean) - ``true`` if the uncertainty includes all
                dates, ``false`` otherwise
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    def is_uncertainty_time_inclusive(self):
        """Tests if the uncertainty is time inclusive.

        An inclusive uncertainty includes the entire range specified by
        the uncertainty units e.g. +/- 1 year includes all of the
        seconds within that interval. A non-inclusive uncertainty would
        mean the year is uncertain but the time is certain.

        return: (boolean) - ``true`` if the uncertainty includes all
                times, ``false`` otherwise
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()


class Duration(datetime.timedelta, abc_calendaring_primitives.Duration, OsidPrimitive):
    """The ``Duration`` a length of time."""

    def get_calendar_type(self):
        """Gets the calendar type.

        return: (osid.type.Type) - the calendar type
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    calendar_type = property(fget=get_calendar_type)

    def get_time_type(self):
        """Gets the time type.

        return: (osid.type.Type) - the time type
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    time_type = property(fget=get_time_type)

    def get_aeons(self):
        """Gets the number of aeons.

        An aeon is 1B years.

        return: (decimal) - the number of aeons
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    aeons = property(fget=get_aeons)

    def get_epochs(self):
        """Gets the number of epochs.

        An epoch is 1M years.

        return: (decimal) - the number of epochs
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    epochs = property(fget=get_epochs)

    def get_millennia(self):
        """Gets the number of millennia.

        A millennium is 1,000 years.

        return: (decimal) - the number of millennia
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    millennia = property(fget=get_millennia)

    def get_centuries(self):
        """Gets the number of centuries.

        return: (decimal) - the number of centuries
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    centuries = property(fget=get_centuries)

    def get_scores(self):
        """Gets the number of scores.

        return: (decimal) - the number of scores
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    scores = property(fget=get_scores)

    def get_bluemoons(self):
        """Gets the number of blue moons.

        return: (decimal) - the number of blue moons
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    bluemoons = property(fget=get_bluemoons)

    def get_years(self):
        """Gets the number of years.

        return: (decimal) - the number of years
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    years = property(fget=get_years)

    def get_months(self):
        """Gets the number of months.

        return: (decimal) - the number of months
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    months = property(fget=get_months)

    def get_weeks(self):
        """Gets the number of weeks.

        return: (decimal) - the number of weeks
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    weeks = property(fget=get_weeks)

    def get_days(self):
        """Gets the number of days.

        return: (decimal) - the number of days
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    days = property(fget=get_days)

    def get_hours(self):
        """Gets the number of hours.

        return: (decimal) - the number of hours
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    hours = property(fget=get_hours)

    def get_minutes(self):
        """Gets the number of minutes.

        return: (decimal) - the number of minutes
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    minutes = property(fget=get_minutes)

    def get_seconds(self):
        """Gets the number of seconds.

        return: (decimal) - the number of seconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    seconds = property(fget=get_seconds)

    def get_milliseconds(self):
        """Gets the number of milliseconds.

        A millisecond is one thousandth of a second.

        return: (decimal) - the number of milliseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    milliseconds = property(fget=get_milliseconds)

    def get_microseconds(self):
        """Gets the number of microseconds.

        A microsecond is one millionth of a second.

        return: (decimal) - the number of micrseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

#    microseconds = property(fget=get_microseconds)

    def get_nanoseconds(self):
        """Gets the number of nanoseconds.

        A nanosecond is one billionth of a second.

        return: (decimal) - the number of nanoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    nanoseconds = property(fget=get_nanoseconds)

    def get_picoseconds(self):
        """Gets the number of picoseconds.

        A picosecond is one trillionth of a second.

        return: (decimal) - the number of picoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    picoseconds = property(fget=get_picoseconds)

    def get_femtoseconds(self):
        """Gets the number of femtoseconds.

        A femtosecond is one quadrillionth of a second.

        return: (decimal) - the number of femtoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    femtoseconds = property(fget=get_femtoseconds)

    def get_attoseconds(self):
        """Gets the number of attoseconds.

        An attosecond is one quintillionth of a second.

        return: (decimal) - the number of attoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    attoseconds = property(fget=get_attoseconds)

    def get_zeptoseconds(self):
        """Gets the number of zeptoseconds.

        A zeptosecond is one sextillionth of a second.

        return: (decimal) - the number of zeptoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    zeptoseconds = property(fget=get_zeptoseconds)

    def get_yoctoseconds(self):
        """Gets the number of yoctoseconds.

        A yoctosecond is one septillionth of a second. This is getting
        quite small.

        return: (decimal) - the number of yoctoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    yoctoseconds = property(fget=get_yoctoseconds)

    def get_xoxxoseconds(self):
        """Gets the number of xoxxoseconds.

        A xoxxosecond is one octillionth of a second. We're going with
        Rudy Rucker here.

        return: (decimal) - the number of xoxxoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    xoxxoseconds = property(fget=get_xoxxoseconds)

    def get_weebleseconds(self):
        """Gets the number of weebleseconds.

        A weeblesecond is one nonillionth of a second.

        return: (decimal) - the number of weebleseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    weebleseconds = property(fget=get_weebleseconds)

    def get_vatoseconds(self):
        """Gets the number of vatoseconds.

        A vatosecond is one decillionth of a second.

        return: (decimal) - the number of vatoseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    vatoseconds = property(fget=get_vatoseconds)

    def get_undaseconds(self):
        """Gets the number of undaseconds.

        An undasecond is one unadecillionth of a second.

        return: (decimal) - the number of undaseconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    undaseconds = property(fget=get_undaseconds)

    def get_planck_seconds(self):
        """Gets the number of Planck sseconds.

        A Planck is 10 quattuordecillionths of a second.

        return: (decimal) - the number of planck seconds
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    planck_seconds = property(fget=get_planck_seconds)

    def get_granularity(self):
        """Gets the granularity of this duration.

        The granularity indicates the resolution of the clock. More
        precision than what is specified in this method cannot be
        inferred from the available data.

        return: (osid.calendaring.DateTimeResolution) - the time units
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    granularity = property(fget=get_granularity)

    def get_granularity_multiplier(self):
        """If the granularity of the time equals ``get_granularity(),`` then the multiplier is 1.

        This method may return a different number when the granularity
        differs from one of the defined resolutions.

        return: (cardinal) - granularity multiplier
        *compliance: mandatory -- This method must be implemented.*

        """
        return 1

    granularity_multiplier = property(fget=get_granularity_multiplier)

    def defines_uncertainty(self):
        """Tests if uncertainty is defined for this time.

        return: (boolean) - ``true`` if uncertainty is defined,
                ``false`` otherwise
        *compliance: mandatory -- This method must be implemented.*

        """
        return False

    def get_uncertainty_units(self):
        """Gets the units of the uncertainty.

        return: (osid.calendaring.DateTimeResolution) - units of the
                uncertainty
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    uncertainty_units = property(fget=get_uncertainty_units)

    def get_uncertainty_minus(self):
        """Gets the uncertainty of this time in the negative direction.

        return: (cardinal) - the uncertainty under this value
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    uncertainty_minus = property(fget=get_uncertainty_minus)

    def get_uncertainty_plus(self):
        """Gets the uncertainty of this time in the positive direction.

        return: (cardinal) - the uncertainty over this value
        raise:  IllegalState - ``defines_uncertainty()`` is ``false``
        *compliance: mandatory -- This method must be implemented.*

        """
        raise Unimplemented()

    uncertainty_plus = property(fget=get_uncertainty_plus)


class RGBColorCoordinate(abc_mapping_primitives.Coordinate, OsidPrimitive):
    """A coordinate represents a position."""

    def __init__(self, hexstr=None, values=None,
                       uncertainty_minus=None,
                       uncertainty_plus=None):
        if values is not None:
            if not isinstance(values, list) or len(values) != 3:
                raise InvalidArgument()
            self._values = values
        elif hexstr is not None:
            if not isinstance(hexstr, str) or len(hexstr) != 6:
                raise InvalidArgument()
            try:
                self._values = [int(hexstr[:-4], 16), int(hexstr[2:-2], 16), int(hexstr[4:], 16)]
            except:
                raise InvalidArgument(hexstr)
        else:
            raise NullArgument()
        self._uncertainty_minus = uncertainty_minus
        self._uncertainty_plus = uncertainty_plus

    def __str__(self):
        hexlist = []
        for value in self._values:
            hexstr = hex(value)[2:]
            if len(hexstr) == 1:
                hexstr = '0' + hexstr
            hexlist.append(hexstr)
        return ''.join(hexlist)

    def get_coordinate_type(self):
        return Type(identifier = 'rgb_color',
                    authority = 'ODL.MIT.EDU',
                    namespace = 'mapping.Coordinate',
                    display_name = 'RGB Color Coordinate',
                    display_label = 'RGB Color',
                    description = 'Coordinate Type for an RGB Color',
                    domain = 'mapping.Coordinate')

    coordinate_type = property(fget=get_coordinate_type)

    def get_dimensions(self):
        return len(self._values)

    dimensions = property(fget=get_dimensions)

    def get_values(self):
        return self._values

    values = property(fget=get_values)

    def defines_uncertainty(self):
        return self._uncertainty_minus or self._uncertainty_plus

    def get_uncertainty_minus(self):
        return bool(self._uncertainty_minus)

    uncertainty_minus = property(fget=get_uncertainty_minus)

    def get_uncertainty_plus(self):
        return bool(self._uncertainty_plus)

    uncertainty_plus = property(fget=get_uncertainty_plus)

