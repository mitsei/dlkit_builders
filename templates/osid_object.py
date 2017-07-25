class GenericObject(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id, DateTime, Duration, DisplayText',
                'from ..utilities import get_registry',
                'from decimal import Decimal']
        }
    }

    # Note: self._catalog_name = '${cat_name_under}' below is currently
    # only for osid.OsidObject.get_object_map() setting the now deprecated
    # ${cat_name}Id element and may be removed someday
    init_template = {
        'python': {
            'json': """
    ${pattern_name}
    _namespace = '${implpkg_name}.${interface_name}'

    def __init__(self, **kwargs):
        osid_objects.OsidObject.__init__(self, object_name='${object_name_upper}', **kwargs)
        self._catalog_name = '${cat_name}'
${instance_initers}"""
        }
    }

    is_attribute_boolean_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return bool(self._my_map['${var_name_mixed}'])"""
        }
    }

    is_object_based_object_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return bool(self._my_map['${var_name}Ids'])"""
        }
    }

    can_attribute_boolean_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if self._my_map['${var_name_mixed}'] is None:
            raise errors.IllegalState()
        else:
            return self._my_map['${var_name_mixed}']"""
        }
    }

    has_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return bool(self._my_map['${var_name_mixed}Id'])"""
        }
    }

    get_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not bool(self._my_map['${var_name_mixed}Id']):
            raise errors.IllegalState('${var_name} not set')
        else:
            return ${return_type}(self._my_map['${var_name_mixed}Id'])"""
        }
    }

    get_id_attribute_object_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not bool(self._my_map['${var_name_mixed}Id']):
            raise errors.IllegalState('this ${object_name} has no ${var_name}')
        mgr = self._get_provider_manager('${return_pkg_caps}')
        if not mgr.supports_${return_type_under}_lookup():
            raise errors.OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        lookup_session = mgr.get_${return_type_under}_lookup_session(proxy=getattr(self, "_proxy", None))
        lookup_session.use_federated_${return_cat_name_under}_view()
        osid_object = lookup_session.get_${return_type_under}(self.get_${var_name}_id())
        return osid_object"""
        }
    }

    get_object_record_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        ${pattern_name}
        return self._get_record(${arg0_name})"""
        }
    }

    has_simple_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        try:
            return bool(self._my_map['${var_name_mixed}'])
        except KeyError:
            pass
        return False"""
        }
    }

    get_display_text_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return DisplayText(display_text_map=self._my_map['${var_name_mixed}'])"""
        }
    }

    has_display_text_attribute_template = has_simple_attribute_template

    get_string_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not self.has_${var_name}():
            raise errors.IllegalState('${var_name} not set')
        return self._my_map['${var_name_mixed}']"""
        }
    }

    get_decimal_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not self.has_${var_name}():
            raise errors.IllegalState('${var_name} not set')
        return Decimal(str(self._my_map['${var_name_mixed}']))"""
        }
    }

    has_decimal_attribute_template = has_simple_attribute_template

    get_cardinal_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not self.has_${var_name}():
            raise errors.IllegalState('${var_name} not set')
        return int(self._my_map['${var_name_mixed}'])"""
        }
    }

    has_cardinal_attribute_template = has_simple_attribute_template

    get_type_attribute_template = get_id_attribute_template

    get_date_time_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not self.has_${var_name}():
            raise errors.IllegalState('${var_name} not set')
        dt = self._my_map['${var_name_mixed}']
        return DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)"""
        }
    }

    has_date_time_attribute_template = has_simple_attribute_template

    get_duration_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not self.has_${var_name}():
            raise errors.IllegalState('${var_name} not set')
        return Duration(**self._my_map['${var_name_mixed}'])"""
        }
    }

    has_duration_attribute_template = has_simple_attribute_template

    get_id_list_attribute_same_package_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        id_list = []
        for ${var_name} in self.get_${var_name_plural}():
            id_list.append(${var_name}.get_id())
        return IdList(id_list)"""
        }
    }

    get_id_list_attribute_different_package_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return IdList(self._my_map['${var_name_mixed}Ids'])"""
        }
    }

    get_initialized_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return Id(self._my_map['${var_name_mixed}Id'])"""
        }
    }

    get_aggregated_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return ${aggregated_object_name}List(
            self._my_map['${var_name_plural_mixed}'],
            runtime=self._runtime,
            proxy=self._proxy)

    def _delete(self):
        for ${aggregated_object_name_under} in self.get_${aggregated_objects_name_under}():
            ${aggregated_object_name_under}._delete()
        osid_objects.OsidObject._delete(self)"""
        }
    }

    get_id_list_objects_different_package_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if not bool(self._my_map['${var_name_singular_mixed}Ids']):
            raise errors.IllegalState('no ${var_name_singular_mixed}Ids')
        mgr = self._get_provider_manager('${return_pkg_caps}')
        if not mgr.supports_${return_type_list_object_under}_lookup():
            raise errors.OperationFailed('${return_pkg_title} does not support ${return_type_list_object} lookup')

        # What about the Proxy?
        lookup_session = mgr.get_${return_type_list_object_under}_lookup_session(proxy=getattr(self, "_proxy", None))
        lookup_session.use_federated_${return_cat_name_under}_view()
        return lookup_session.get_${return_type_list_object_plural_under}_by_ids(self.get_${var_name_singular}_ids())"""
        }
    }
