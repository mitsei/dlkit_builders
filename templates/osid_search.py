class GenericObjectSearch(object):

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid import searches as osid_searches',
                'from ..utilities import get_registry',
            ],
            'tests': [
                'from dlkit.runtime import PROXY_SESSION, proxy_example',
                'from dlkit.runtime.managers import Runtime',
                'REQUEST = proxy_example.SimpleRequest()',
                'CONDITION = PROXY_SESSION.get_proxy_condition()',
                'CONDITION.set_http_request(REQUEST)',
                'PROXY = PROXY_SESSION.get_proxy(CONDITION)\n',
                'from dlkit.primordium.id.primitives import Id',
                'from dlkit.primordium.type.primitives import Type',
                'DEFAULT_TYPE = Type(**{\'identifier\': \'DEFAULT\', \'namespace\': \'DEFAULT\', \'authority\': \'DEFAULT\'})',
                'from dlkit.abstract_osid.osid import errors',
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
        osid_searches.OsidSearch.__init__(self, runtime)""",
            'tests': """
@pytest.fixture(scope="class",
                params=${test_service_configs})
def ${interface_name_under}_class_fixture(request):
    # From test_templates/resource.py::ResourceSearch::init_template
    request.cls.service_config = request.param
    request.cls.svc_mgr = Runtime().get_service_manager(
        '${pkg_name_upper}',
        proxy=PROXY,
        implementation=request.cls.service_config)
    create_form = request.cls.svc_mgr.get_${cat_name_under}_form_for_create([])
    create_form.display_name = 'Test catalog'
    create_form.description = 'Test catalog description'
    request.cls.catalog = request.cls.svc_mgr.create_${cat_name_under}(create_form)

    def class_tear_down():
        request.cls.svc_mgr.delete_${cat_name_under}(request.cls.catalog.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def ${interface_name_under}_test_fixture(request):
    # From test_templates/resource.py::ResourceSearch::init_template
    request.cls.search = request.cls.catalog.get_${object_name_under}_search()"""
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
