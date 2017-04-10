
class OsidProfile:

    import_statements = [
        'from ..osid.osid_errors import Unimplemented',
    ]


class OsidManager:

    import_statements = [
        'from ..osid.osid_errors import Unimplemented',
    ]


class OsidProxyManager:

    import_statements = [
        'from .osid_errors import Unimplemented',
    ]


class Sourceable:

    import_statements = [
        'from .osid_errors import Unimplemented',
    ]


class OsidList:

    init = """
    def __init__(self, iter_object=None, count=None, db_prefix='', runtime=None):
        if iter_object is None:
            iter_object = []
        if count != None:
            self._count = count
        elif isinstance(iter_object, dict) or isinstance(iter_object, list):
            self._count = len(iter_object)
        else:
            self._count = None
        self._runtime = runtime
        self._db_prefix = db_prefix
        self._iter_object = iter(iter_object)

    def __iter__(self):
        return self

    def next(self):
        \"\"\"Iterator 'next' method\"\"\"
        try:
            next_object = self._iter_object.next()
        except:
            raise
        if self._count != None:
            self._count -= 1
        return next_object

    def len(self):
        return self.available()
"""

    has_next = """
        if self._count != None:
            # If count is available, use it
            return bool(self._count)
        else:
            # otherwise we have no idea
            return True"""

    available = """
        if self._count != None:
            # If count is available, use it
            return self._count
        else:
            # We have no idea.
            return 0  # Don't know what to do here"""

    skip = """
        ### STILL NEED TO IMPLEMENT THIS ###
        pass"""
