class GenericObjectSearch(object):

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid import searches as osid_searches',
                'from ..utilities import get_registry',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self, runtime):
        self._namespace = '${pkg_name}.${object_name}'
        self._runtime = runtime
        record_type_data_sets = get_registry('RESOURCE_RECORD_TYPES', runtime)
        self._record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        self._id_list = None
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_searches.OsidSearch.__init__(self, runtime)"""
        }
    }

    search_among_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        self._id_list = ${arg0_name}"""
        }
    }


class GenericObjectSearchResults(object):

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from . import objects',
                'from . import queries',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self, results, query_terms, runtime):
        # if you don't iterate, then .count() on the cursor is an inaccurate representation of limit / skip
        # self._results = [r for r in results]
        self._namespace = '${pkg_name}.${object_name}'
        self._results = results
        self._query_terms = query_terms
        self._runtime = runtime
        self.retrieved = False"""
        }
    }

    get_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if self.retrieved:
            raise errors.IllegalState('List has already been retrieved.')
        self.retrieved = True
        return objects.${return_type}(self._results, runtime=self._runtime)"""
        }
    }

    get_object_query_inspector_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return queries.${return_type}(self._query_terms, runtime=self._runtime)"""
        }
    }
