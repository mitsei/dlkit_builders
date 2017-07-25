class GenericMetadata(object):
    get_element_id_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return self._kwargs['${var_name}']"""
        }
    }

    get_element_label_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        return DisplayText(self._kwargs['${var_name}'])"""
        }
    }

    get_minimum_cardinal_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise errors.IllegalState()
        return self._kwargs['${var_name}']"""
        }
    }

    supports_coordinate_type_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise errors.IllegalState()
        return ${arg0_name} in self.get_${var_name}"""
        }
    }

    get_existing_cardinal_values_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        ${pattern_name}
        # This template may only work well for very primitive return types, like string or cardinal.
        # Need to update it to support DisplayName, or Id etc.
        if self._kwargs['syntax'] not in ${syntax_list}:
            raise errors.IllegalState()
        return self._kwargs['${var_name}']"""
        }
    }
