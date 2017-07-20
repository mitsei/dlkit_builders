class GenericObjectList(object):
    import_statements_pattern = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
            ]
        }
    }

    get_next_object_template = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        # From: templates/osid_list.py::GenericObjectList::get_next_object_template
        return next(self)

    def next(self):
        return self._get_next_object(${return_type})

    __next__ = next"""
        }
    }

    get_next_objects_template = {
        'python': {
            'json': """
    def ${method_name}(self, ${arg0_name}):
        ${doc_string}
        # From: templates/osid_list.py::GenericObjectList::get_next_objects_template
        return self._get_next_n(${return_type}List, number=${arg0_name})"""
        }
    }
