# These are the allowable OSID Language Primitives that can be used in OSID
# method signatures. Parameters and returns in OSID methods may be specified
# in terms of other OSID interfaces or using one of these primitives. All
# OSID Language Primitives are immutable.

OSID_Language_Primitives = [
    'boolean',  # A boolean is a truth value of true or false.

    'byte',     # A byte is a basic unit of storage supporting a minimum of an
                # 8-bit value. A byte should be used to represent a unit of
                # arbitrary data not defined in the OSIDs.

    'cardinal',  # A cardinal is a non-negative number supporting a 64-bit value
                 # (0..9,223,372,036,854,775,808) . Cardinal numbers should be
                 # used to represent numbers such as sizes and counters where
                 # negative numbers have no meaning.

    'decimal',  # A signed arbitrary precision decimal number.

    'integer',  # An integer is a number supporting a 64-bit value
                # (-9,223,372,036,854,775,808.. 9,223,372,036,854,775,808).

    'object',   # An object Is used for data plugs used to permit data extensions
                # outside the scope of the OSIDs. A Type is used to identify the
                # specification of the plug.

    'string',   # A string is a sequence of zero or more display characters. Each
                # display character should support an international character set.
                # OSIDs should avoid using strings to transmit data on which an
                # OSID Consumer operates in any way other than to display. OSID
                # methods should utilize Types, Ids, and other primtiives where an
                # OSID Consumer performs a check or comparison as strings may be
                # modified or translated.

    'timestamp'  # A timestamp is a date and time with millisecond precision
                 # supporting the Quaternary period of the Cenozoic era
                 # (2,000,000B.C..2,000,000A.D) . When this period will end is a
                 # simple approximation and perhaps wishful thinking. Providers,
                 # however, may select to narrow the scope to the Holocene epoch
                 # of this era (10,000B.C) .
                 # Providers should use timestamp when expressing an actual
                 # recorded date and time. In most cases, the granularity of a
                 # date is variable where an osid.calendaring.DateTime should be
                 # specified to not imply millisecond precision where it does
                 # not exist.
]
