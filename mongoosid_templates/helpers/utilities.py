"""mongo utilities.py"""
from .osid.osid_errors import NullArgument, NotFound, OperationFailed
from dlkit.primordium.calendaring.primitives import DateTime

from . import MONGO_CLIENT


class MongoClientValidated(object):
    """automatically validates the insert_one, find_one, and delete_one methods"""
    def __init__(self, db, collection=None):
        if collection is None:
            self._mc = MONGO_CLIENT.mongo_client[db]
        else:
            self._mc = MONGO_CLIENT.mongo_client[db][collection]

    def _validate_write(self, result):
        try:
            if not result.acknowledged or result.inserted_id is None:
            # if (('writeErrors' in result and len(result['writeErrors']) > 0) or
            #         ('writeConcernErrors' in result and len(result['writeConcernErrors']) > 0)):
                raise OperationFailed(str(result))
        except AttributeError:
            # account for deprecated save() method
            if result is None:
                raise OperationFailed('Nothing saved to database.')

    def count(self):
        return self._mc.count()

    def delete_one(self, query):
        result = self._mc.delete_one(query)
        if result is None or result.deleted_count == 0:
            raise NotFound(str(query) + ' returned None.')
        return result

    def find(self, query=None):
        if query is None:
            return self._mc.find()
        else:
            return self._mc.find(query)

    def find_one(self, query):
        result = self._mc.find_one(query)
        if result is None:
            raise NotFound(str(query) + ' returned None.')
        return result

    def insert_one(self, doc):
        result = self._mc.insert_one(doc)
        self._validate_write(result)
        return result

    def raw(self):
        """ return the raw mongo client object...used for GridFS
        """
        return self._mc

    def save(self, doc):
        result = self._mc.save(doc)
        self._validate_write(result)
        return result

def arguments_not_none(func):
    """decorator, to check if any arguments are None; raise exception if so"""
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                raise NullArgument()
        for arg, val in kwargs.iteritems():
            if val is None:
                raise NullArgument()
        try:
            return func(*args, **kwargs)
        except TypeError as ex:
            if 'takes exactly' in ex.args[0]:
                raise NullArgument('Wrong number of arguments provided: ' + str(ex.args[0]))
            else:
                raise TypeError(*ex.args)

    return wrapper

def overlap(start1, end1, start2, end2):
    """
    Does the range (start1, end1) overlap with (start2, end2)?
    
    From Ned Batchelder
    http://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    
    """
    return not (end1 < start2 or end2 < start1)

def now_map():
    now = DateTime.utcnow()
    return {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'microsecond': now.microsecond,
    }

