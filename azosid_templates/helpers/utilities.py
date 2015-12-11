"""helper utilities for the authz adapter implementation"""

class QueryWrapper(object):
    def __init__(self, provider_query):
        self.__class__ = type(provider_query.__class__.__name__,
                              (self.__class__, provider_query.__class__),
                              {})
        self.__dict__ = provider_query.__dict__
        self._provider_query = provider_query
        self.cat_id_args_list = []
