from copy import deepcopy


class GenericCatalogQuery(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from ..primitives import Id',
                'from ..id.objects import IdList',
                'from ..utilities import get_registry',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self, runtime):
        self._runtime = runtime
        record_type_data_sets = get_registry('${cat_name_upper}_RECORD_TYPES', runtime)
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidCatalogQuery.__init__(self, runtime)

    def _get_descendant_catalog_ids(self, catalog_id):
        hm = self._get_provider_manager('HIERARCHY')
        hts = hm.get_hierarchy_traversal_session_for_hierarchy(
            Id(authority='${pkg_name_upper}',
               namespace='CATALOG',
               identifier='${cat_name_upper}')
        )  # What about the Proxy?
        descendants = []
        if hts.has_children(catalog_id):
            for child_id in hts.get_children(catalog_id):
                descendants += list(self._get_descendant_catalog_ids(child_id))
                descendants.append(child_id)
        return IdList(descendants)"""
        }
    }

    clear_simple_terms_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._clear_terms('${var_name_mixed}')"""
        }
    }


class GenericObjectQuery(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..utilities import get_registry',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self, runtime):
        self._namespace = '${pkg_name_replaced}.${object_name}'
        self._runtime = runtime
        record_type_data_sets = get_registry('${object_name_upper}_RECORD_TYPES', runtime)
        self._all_supported_record_type_data_sets = record_type_data_sets
        self._all_supported_record_type_ids = []
        for data_set in record_type_data_sets:
            self._all_supported_record_type_ids.append(str(Id(**record_type_data_sets[data_set])))
        osid_queries.OsidObjectQuery.__init__(self, runtime)"""
        }
    }

    clear_simple_terms_template = deepcopy(GenericCatalogQuery.clear_simple_terms_template)

    match_catalog_id_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        self._add_match('assigned${cat_name}Ids', str(${arg0_name}), ${arg1_name})"""
        }
    }

    clear_catalog_id_terms_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        self._clear_terms('assigned${cat_name}Ids')"""
        }
    }

    match_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}):
        ${doc_string}
        ${pattern_name}
        self._add_match('${var_name_mixed}', str(${arg0_name}), ${arg1_name})"""
        }
    }

    clear_id_attribute_terms_template = clear_simple_terms_template

    match_date_time_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, match):
        ${doc_string}
        ${pattern_name}
        self._match_minimum_date_time('${var_name_mixed}', ${arg0_name}, match)
        self._match_maximum_date_time('${var_name_mixed}', ${arg1_name}, match)"""
        }
    }
