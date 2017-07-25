class GenericProfile(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from ..primitives import Type',
                'from ..type.objects import TypeList',
                'from . import sessions',
                'from dlkit.abstract_osid.osid import errors',
                'from . import profile',
                'from ..utilities import get_registry',
            ]
        }
    }

    supports_visible_federation_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return '${method_name}' in profile.SUPPORTS"""
        }
    }

    supports_object_lookup_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return '${method_name}' in profile.SUPPORTS"""
        }
    }

    get_object_record_types_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        record_type_maps = get_registry('${object_name_upper}_RECORD_TYPES', self._runtime)
        record_types = []
        for record_type_map in record_type_maps:
            record_types.append(Type(**record_type_maps[record_type_map]))
        return TypeList(record_types)"""
        }
    }

    supports_object_record_type_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        record_type_maps = get_registry('${object_name_upper}_RECORD_TYPES', self._runtime)
        supports = False
        for record_type_map in record_type_maps:
            if (${arg0_name}.get_authority() == record_type_maps[record_type_map]['authority'] and
                    ${arg0_name}.get_identifier_namespace() == record_type_maps[record_type_map]['namespace'] and
                    ${arg0_name}.get_identifier() == record_type_maps[record_type_map]['identifier']):
                supports = True
        return supports"""
        }
    }

    get_type_list_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return TypeList([])"""
        }
    }

    supports_type_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return False"""
        }
    }


class GenericManager(object):

    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    def __init__(self):
        osid_managers.OsidManager.__init__(self)"""
        }
    }

    get_object_lookup_session_template = {
        'python': {
            'json': """
    def ${method_name}(self, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(proxy=kwargs['proxy'], runtime=self._runtime)
        return ${return_module}.${return_type}(runtime=self._runtime)"""
        }
    }

    get_object_admin_session_template = get_object_lookup_session_template

    get_object_lookup_session_for_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(
                ${arg0_name},
                proxy=kwargs['proxy'],
                runtime=self._runtime)
        return ${return_module}.${return_type}(${arg0_name}, runtime=self._runtime)"""
        }
    }

    get_object_admin_session_for_catalog_template = get_object_lookup_session_for_catalog_template

    get_object_notification_session_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        # pylint: disable=no-member
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(
                proxy=kwargs['proxy'],
                runtime=self._runtime,
                receiver=${arg0_name})
        return ${return_module}.${return_type}(runtime=self._runtime, receiver=${arg0_name})"""
        }
    }

    get_object_notification_session_for_catalog_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}, ${arg1_name}, **kwargs):
        ${doc_string}
        ${pattern_name}
        if not self.supports_${support_check}():
            raise errors.Unimplemented()
        ##
        # Also include check to see if the catalog Id is found otherwise raise errors.NotFound
        ##
        # pylint: disable=no-member
        if 'proxy' in kwargs:
            return ${return_module}.${return_type}(
                catalog_id=${arg1_name},
                proxy=kwargs['proxy'],
                runtime=self._runtime,
                receiver=${arg0_name})
        return ${return_module}.${return_type}(
            catalog_id=${arg1_name},
            runtime=self._runtime,
            receiver=${arg0_name})"""
        }
    }


class GenericProxyManager(object):
    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    def __init__(self):
        osid_managers.OsidProxyManager.__init__(self)"""
        }
    }
