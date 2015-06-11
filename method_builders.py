from binder_helpers import fix_reserved_word

from build_controller import Utilities


class MethodBuilder(Utilities):
    """class that builds methods"""
    def __init__(self, method_class=None, *args, **kwargs):
        """method_class differentiates between different variations, i.e. abc
        looks different than mongo"""
        self._class = method_class or 'abc'
        self._ind = 4 * ' '
        self._dind = 2 * self._ind
        super(MethodBuilder, self).__init__()

    def _is(self, desired_type):
        return self._class == str(desired_type)

    def _build_method_doc(self, method):
        if self._is('abc'):
            detail_docs = filter(None, [method['sphinx_param_doc'].strip('\n'),
                                        method['sphinx_return_doc'].strip('\n'),
                                        method['sphinx_error_doc'].strip('\n') + '\n',
                                        method['compliance_doc'].strip('\n'),
                                        method['impl_notes_doc'].strip('\n')])
        else:
            # Mongo impl only?
            detail_docs = filter(None, [method['arg_doc'].strip('\n'),
                                        method['return_doc'].strip('\n'),
                                        method['error_doc'].strip('\n'),
                                        method['compliance_doc'].strip('\n'),
                                        method['impl_notes_doc'].strip('\n')])

        method_doc = self._dind + '\"\"\"' + method['doc']['headline']

        if method['doc']['body'].strip() != '':
            method_doc += '\n\n' + method['doc']['body']
        if detail_docs:
            method_doc += '\n\n' + '\n'.join(detail_docs) + '\n\n'

        method_doc += self._dind + '\"\"\"'
        return method_doc

    def _make_method(self, method):
        decorator = self._ind + '@abc.abstractmethod'
        args = ['self']
        method_impl = self._make_method_impl(method)

        for arg in method['args']:
            args.append(arg['var_name'])

        method_sig = (self._ind + 'def ' + method['name'] + '(' +
                      ', '.join(args) + '):')

        method_doc = self._build_method_doc(method)

        return (decorator + '\n' +
                self._wrap(method_sig) + '\n' +
                self._wrap(method_doc) + '\n' +
                self._wrap(method_impl))

    def _make_method_impl(self, method):
        if self._is('abc'):
            if method['return_type'].strip():
                return '        return # ' + method['return_type']
            else:
                return '        pass'
        else:
            pass

    def make_methods(self, package_name, interface, patterns):
        body = []
        for method in interface['methods']:
            body.append(self._make_method(method))

            # Here is where we add the Python properties stuff:
            if argless_get(method):
                body.append(simple_property('get', method))
            elif one_arg_set(method):
                if (simple_property('del', method)) in body:
                    body.remove(simple_property('del', method))
                    body.append(set_and_del_property(method))
                else:
                    body.append(simple_property('set', method))
            elif argless_clear(method):
                if (simple_property('set', method)) in body:
                    body.remove(simple_property('set', method))
                    body.append(set_and_del_property(method))
                else:
                    body.append(simple_property('del', method))

            if method['name'] == 'get_id':
                    body.append(simple_property('get', method, 'ident'))
            if method['name'] == 'get_identifier_namespace':
                    body.append(simple_property('get', method, 'namespace'))

        return '\n\n'.join(body)

def argless_clear(method):
    return method['name'].startswith('clear_') and method['args'] == []

def argless_get(method):
    return method['name'].startswith('get_') and method['args'] == []

def one_arg_set(method):
    return method['name'].startswith('set_') and len(method['args']) == 1

def set_and_del_property(method):
    prop = '    '
    method_name = strip_prefixes(method['name'])

    prop += fix_reserved_word(method_name)

    clear_method = 'clear_' + method_name
    set_method = 'set_' + method_name

    prop += ' = abc.abstractproperty(fset=' + set_method + ', fdel=' + clear_method + ')'
    return prop

def simple_property(prop_type, method, property_name=None):
    prop = '    '
    method_name = strip_prefixes(method['name'])

    if property_name is None:
        prop += fix_reserved_word(method_name)
    else:
        prop += property_name

    if prop_type == 'get':
        method_name = 'get_' + method_name
    elif prop_type == 'del':
        method_name = 'clear_' + method_name
    elif prop_type == 'set':
        method_name = 'set_' + method_name
    else:
        raise ValueError()

    prop += ' = abc.abstractproperty(f' + prop_type + '=' + method_name + ')'
    return prop

def strip_prefixes(name):
    try:
        if name.index('get_') == 0:
            return name.replace('get_', '', 1)
        else:
            raise ValueError
    except ValueError:
        try:
            if name.index('set_') == 0:
                return name.replace('set_', '', 1)
            else:
                raise ValueError
        except ValueError:
            if name.index('clear_') == 0:
                return name.replace('clear_', '', 1)
            else:
                raise ValueError
