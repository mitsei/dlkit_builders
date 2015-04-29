# -*- coding: utf-8 -*-

#
# This module contains primitives required by the authz_adapter implementation

from ..abstract_osid.id.primitives import Id as abc_id
from ..abstract_osid.osid import markers as abc_osid_markers
from .osid.osid_errors import *

#from .abstract_osid.abc_installation.primitives import Version as abc_version

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

    def __init__(self, idstr=None, authority=None, namespace=None, identifier=None, **kwargs):
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
