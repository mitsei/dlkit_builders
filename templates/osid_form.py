class GenericObjectForm:
    import_statements_pattern = {
        'python': {
            'json': [
                'import importlib',
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
                'from ..osid.metadata import Metadata',
                'from . import default_mdata',
                'from ..utilities import get_registry',
                'from ..utilities import update_display_text_defaults',
            ]
        }
    }

    init_template = {
        'python': {
            'json': """
    # From: templates/osid_form.py::GenericObjectForm::init_template
    _namespace = '${implpkg_name}.${object_name}'

    def __init__(self, **kwargs):
        ${init_object}.__init__(self, object_name='${object_name_upper}', **kwargs)
        self._mdata = default_mdata.get_${object_name_under}_mdata()
        self._init_metadata(**kwargs)
        if not self.is_for_update():
            self._init_map(**kwargs)

    def _init_metadata(self, **kwargs):
        \"\"\"Initialize form metadata\"\"\"
${metadata_super_initers}        ${init_object}._init_metadata(self, **kwargs)
        ${metadata_initers}
    def _init_map(self, record_types=None, **kwargs):
        \"\"\"Initialize form map\"\"\"
${map_super_initers}        ${init_object}._init_map(self, record_types=record_types)
${persisted_initers}"""
        }
    }

    # this needs to be re-designed to know about variable syntax type
    get_simple_attribute_metadata_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::get_simple_attribute_metadata_template
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${syntax_under}_values': self._my_map['${var_name_mixed}']})
        return Metadata(**metadata)"""
        }
    }

    get_id_attribute_metadata_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::get_id_attribute_metadata_template
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${syntax_under}_values': self._my_map['${var_name_mixed}Id']})
        return Metadata(**metadata)"""
        }
    }

    set_simple_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::set_simple_attribute_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type}(${arg0_name}):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""
        }
    }

    clear_simple_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::clear_simple_attribute_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""
        }
    }

    set_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::set_id_attribute_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${syntax_under}(${arg0_name}):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}Id'] = str(${arg0_name})"""
        }
    }

    clear_id_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::clear_id_attribute_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}Id'] = self._${var_name}_default"""
        }
    }

    get_object_form_record_template = {
        'python': {
            'json': """
    def ${method_name}(self, $arg0_name):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::get_object_form_record_template
        return self._get_record(${arg0_name})"""
        }
    }

    get_id_list_attribute_metadata_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::get_id_list_attribute_metadata_template
        metadata = dict(self._mdata['${var_name}'])
        metadata.update({'existing_${var_name}_values': self._my_map['${var_name_singular_mixed}Ids']})
        return Metadata(**metadata)"""
        }
    }

    set_id_list_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::set_id_list_attribute_template
        if not isinstance(${arg0_name}, list):
            raise errors.InvalidArgument()
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        idstr_list = []
        for object_id in ${arg0_name}:
            if not self._is_valid_id(object_id):
                raise errors.InvalidArgument()
            idstr_list.append(str(object_id))
        self._my_map['${var_name_singular_mixed}Ids'] = idstr_list"""
        }
    }

    clear_id_list_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::clear_id_list_attribute_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_singular_mixed}Ids'] = self._${var_name}_default"""
        }
    }

    set_display_text_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::set_display_text_attribute_template
        self._my_map['${var_name_mixed}'] = self._get_display_text(${arg0_name}, self.get_${var_name}_metadata())"""
        }
    }

    clear_display_text_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::clear_display_text_attribute_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess()
        self._my_map['${var_name_mixed}'] = dict(self._${var_name}_default)"""
        }
    }

    # Make this separate from ``set_simple_attribute_template`` because the string validation
    #   method has additional arguments
    set_string_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::set_string_attribute_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess()
        if not self._is_valid_${arg0_type}(
                ${arg0_name},
                self.get_${var_name}_metadata()):
            raise errors.InvalidArgument()
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""
        }
    }

    clear_string_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::clear_string_attribute_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry you cannot clear ${var_name}')
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""
        }
    }

    set_decimal_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::set_decimal_attribute_template
        if self.get_${var_name}_metadata().is_read_only():
            raise errors.NoAccess('Sorry, you cannot set ${arg0_name}')
        try:
            ${arg0_name} = float(${arg0_name})
        except ValueError:
            raise errors.InvalidArgument('${arg0_name} needs to be a float')
        if not self._is_valid_${arg0_type}(${arg0_name}, self.get_${var_name}_metadata()):
            raise errors.InvalidArgument('${arg0_name} is not a valid float')
        self._my_map['${var_name_mixed}'] = ${arg0_name}"""
        }
    }

    clear_decimal_attribute_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_form.py::GenericObjectForm::clear_decimal_attribute_template
        if (self.get_${var_name}_metadata().is_read_only() or
                self.get_${var_name}_metadata().is_required()):
            raise errors.NoAccess('Sorry, you cannot clear ${var_name}')
        self._my_map['${var_name_mixed}'] = self._${var_name}_default"""
        }
    }
