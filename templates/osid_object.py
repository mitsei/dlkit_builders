class GenericObject(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..utilities import get_registry']
        }
    }

    # Note: self._catalog_name = '${cat_name_under}' below is currently
    # only for osid.OsidObject.get_object_map() setting the now deprecated
    # ${cat_name}Id element and may be removed someday
    init_template = {
        'python': {
            'json': """
    # From: templates/osid_object.py::GenericObject::init_template
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
        # From: templates/osid_object.py::GenericObject::is_attribute_boolean_template
        return bool(self._my_map['${var_name_mixed}'])"""
        }
    }

    can_attribute_boolean_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_object.py::GenericObject::can_attribute_boolean_template
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
        # From: templates/osid_object.py::GenericObject::has_id_attribute_template
        return bool(self._my_map['${var_name_mixed}Id'])"""
        }
    }

    get_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_object.py::GenericObject::get_id_attribute_template
        if not bool(self._my_map['${var_name_mixed}Id']):
            raise errors.IllegalState('this ${object_name} has no ${var_name}')
        else:
            return Id(self._my_map['${var_name_mixed}Id'])"""
        }
    }

    get_id_attribute_object_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_object.py::GenericObject::get_id_attribute_object_template
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
        # From: templates/osid_object.py::GenericObject::get_object_record_template
        return self._get_record(${arg0_name})"""
        }
    }
