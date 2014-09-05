# -*- coding: utf-8 -*-

# This module contains all the osid_error exception classes and can be
# used by any python implementations that need to throw an osid error

"""
Errors are specified in each method specification. Only the specified 
errors are permitted as error conditions in OSID method contracts with 
exceptions noted in the descriptions below. Provider Contract errors are 
never specified but may be returned at any time by an OSID Runtime. An 
OSID Provider implementation is only permitted to return those errors 
specified in a method contract however, some Consumer Contract errors may 
be automatically handled in an OSID Runtime. Errors should result when the 
contract of the interface as been violated or cannot be fulfilled and it 
is necessary to disrupt the flow of control for an OSID Consumer. Different 
errors are specified where it is forseen that an OSID Consumer may wish 
to execute a different action without violating the encapsulation of 
internal OSID Provider operations. Such actions do not include debugging 
or other detailed information which is the responsibility of the OSID 
Provider to manage. As such, the number of errors defined across all 
the interfaces is kept to a minimum and the context of the error may vary 
from method to method in accordance with the OSID specification.

"""

from ..abstract_osid.osid import errors

""" User Errors:

User errors are only permitted where specified in method signatures and 
should be handled directly by a consumer application.

"""
class AlreadyExists(errors.AlreadyExists, Exception):
    pass


class NotFound(errors.NotFound, Exception):
    pass


class PermissionDenied(errors.PermissionDenied, Exception):
    pass

""" Operational Errors:	

Operational errors result from failures in the system. These errors are 
only permitted where specified and should be handled directly by the 
consumer application.

"""

class ConfigurationError(errors.ConfigurationError, Exception):
    pass


class OperationFailed(errors.OperationFailed, Exception):
    pass


class TransactionFailure(errors.TransactionFailure, Exception):
    pass

""" ConsumerContract:

Errors in programming resulting from an incorrect use of the OSIDs. 
Application code should be checked for accuracy. These errors should be 
avoided by using the defined interoperability and flow control tests.

"""

class IllegalState(errors.IllegalState, Exception):
    pass


class InvalidArgument(errors.InvalidArgument, Exception):
    pass


class InvalidMethod(errors.InvalidMethod, Exception):
    pass


class NoAccess(errors.NoAccess, Exception):
    pass


class NullArgument(errors.NullArgument, Exception):
    pass


class Unimplemented(errors.Unimplemented, Exception):
    pass


class Unsupported(errors.Unsupported, Exception):
    pass
