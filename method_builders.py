import string
from importlib import import_module

from binder_helpers import fix_reserved_word, under_to_caps, get_pkg_name, camel_to_under, \
    camel_to_mixed, under_to_mixed, make_plural, remove_plural, SkipMethod
from build_controller import Utilities, BaseBuilder, Templates
from config import sessions_to_implement


class MethodBuilder(BaseBuilder, Templates, Utilities):
    """class that builds methods"""
    def __init__(self, method_class=None, template_dir=None, *args, **kwargs):
        """method_class differentiates between different variations, i.e. abc
        looks different than mongo"""
        super(MethodBuilder, self).__init__()

        self._class = method_class or 'abc'
        self._ind = 4 * ' '
        self._dind = 2 * self._ind

        self._template_dir = template_dir

        if template_dir is not None:
            self._make_dir(template_dir)

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

    def _get_method_context(self, package_name, method, interface, patterns):
        """Get the method context vars, to be used in the template"""
        from interface_builders import is_manager_session

        def construct_arg_context(arg_number, arg_type_full):
            arg_type = self.last(arg_type_full).strip('[]')
            arg_context = {
                arg_number + '_type': arg_type,
                arg_number + '_type_under': camel_to_under(arg_type),
                arg_number + '_type_mixed': camel_to_mixed(arg_type),
                arg_number + '_abcapp_name': self._app_name(get_pkg_name(arg_type_full.strip('[]')), abstract=True),
                arg_number + '_abcpkg_name': self._abc_pkg_name(get_pkg_name(arg_type_full.strip('[]')), abc=False),
                arg_number + '_module': self.get_interface_module(
                    get_pkg_name(arg_type_full),
                    arg_type)
            }
            return arg_context

        context = {}

        if interface['shortname'] + '.' + method['name'] in patterns:
            context = patterns[interface['shortname'] + '.' + method['name']]['kwargs']

        arg_list = []
        for arg in method['args']:
            arg_list.append(arg['var_name'])
        context['arg_list'] = ', '.join(arg_list)

        if 'package_name' in context:
            # Add keyword arguments to template kwargs that are particular
            # to the mongo implementation
            context['app_name'] = self._app_name(context['package_name'])
            context['implpkg_name'] = self._abc_pkg_name(context['package_name'], abc=False)
            context['abcapp_name'] = self._app_name(context['package_name'])
            context['abcpkg_name'] = self._abc_pkg_name(context['package_name'], abc=False)
            context['interface_name_under'] = camel_to_under(context['interface_name'])
            context['interface_name_dot'] = '.'.join(context['interface_name_under'].split('_')[:-1])
            context['package_name_caps'] = package_name.title()
            context['package_name_upper'] = package_name.upper()

            if method['args']:
                 context['args_kwargs_or_nothing'] = '*args, **kwargs'
            else:
                 context['args_kwargs_or_nothing'] = ''

            if context['interface_name_under'].endswith('_session'):
                context['session_shortname_dot'] = '.'.join(context['interface_name_under'].split('_')[:-1])

            if 'arg0_type_full' in context:
                context.update(construct_arg_context('arg0',
                                                     context['arg0_type_full']))
            if 'arg1_type_full' in context:
                context.update(construct_arg_context('arg1',
                                                     context['arg1_type_full']))
            if 'arg2_type_full' in context:
                context.update(construct_arg_context('arg2',
                                                     context['arg2_type_full']))
            if 'arg3_type_full' in context:
                context.update(construct_arg_context('arg3',
                                                     context['arg3_type_full']))
            if 'arg0_object' in context:
                context['arg0_object_under'] = camel_to_under(context['arg0_object'])
                context['arg0_object_mixed'] = camel_to_mixed(context['arg0_object'])
            if 'return_type_full' in context:
                context['return_type'] = context['return_type_full'].split('.')[-1]
                context['return_pkg'] = get_pkg_name(context['return_type_full'])
                context['return_module'] = self.get_interface_module(
                    get_pkg_name(context['return_type_full']),
                    context['return_type_full'].split('.')[-1])
            if 'return_pkg' in context:
                context['return_app_name'] = self._app_name(context['return_pkg'])
                context['return_implpkg_name'] = self._abc_pkg_name(context['return_pkg'], abc=False)
                context['return_pkg_title'] = context['return_pkg'].title()
                context['return_pkg_caps'] = context['return_pkg'].upper()
            if 'return_cat_name' in context:
                context['return_cat_name_under'] = camel_to_under(context['return_cat_name'])
            if 'object_name_under' in context:
                context['object_name_upper'] = context['object_name_under'].upper()
                context['object_name_mixed'] = under_to_mixed(context['object_name_under'])
                # Might want to add creating kwargs['object_name' from this as well]
            if 'object_name' in context and 'package_name' in context:
                context['object_app_name'] = self._app_name(context['package_name'])
                context['object_implpkg_name'] = self._abc_pkg_name(context['package_name'], abc=False)
                context['object_module'] = self.get_interface_module('package_name', 'object_name')
            if 'var_name' in context:
                context['var_name_upper'] = context['var_name'].upper()
                context['var_name_mixed'] = under_to_mixed(context['var_name'])
                context['var_name_plural'] = make_plural(context['var_name'])
                context['var_name_plural_mixed'] = under_to_mixed(context['var_name_plural'])
                context['var_name_singular'] = remove_plural(context['var_name'])
                context['var_name_singular_mixed'] = under_to_mixed(context['var_name_singular'])
            if 'return_type' in context:
                context['return_type_under'] = camel_to_under(context['return_type'])
            if 'return_type' in context and context['return_type'].endswith('List'):
                context['return_type_list_object'] = context['return_type'][:-4]
                context['return_type_list_object_under'] = camel_to_under(context['return_type_list_object'])
                context['return_type_list_object_plural_under'] = make_plural(context['return_type_list_object_under'])
            if ('object_name' in context and
                    not 'object_name_under' in context and
                    not 'object_name_upper' in context):
                context['object_name_under'] = camel_to_under(context['object_name'])
                context['object_name_mixed'] = camel_to_mixed(context['object_name'])
                context['object_name_upper'] = camel_to_under(context['object_name']).upper()
            if 'object_name_under' in context:
                context['object_name_plural_under'] = make_plural(context['object_name_under'])
            if 'aggregated_object_name' in context:
                context['aggregated_object_name_under'] = camel_to_under(context['aggregated_object_name'])
                context['aggregated_object_name_mixed'] = camel_to_mixed(context['aggregated_object_name'])
                context['aggregated_objects_name_under'] = camel_to_under(make_plural(context['aggregated_object_name']))
                context['aggregated_objects_name_mixed'] = camel_to_mixed(make_plural(context['aggregated_object_name']))
            if 'source_name' in context:
                context['source_name_mixed'] = under_to_mixed(context['source_name'])
            if 'destination_name' in context:
                context['destination_name_mixed'] = under_to_mixed(context['destination_name'])
            if 'cat_name' in context:
                context['cat_name_under'] = camel_to_under(context['cat_name'])
                context['cat_name_lower'] = context['cat_name'].lower()
                context['cat_name_mixed'] = camel_to_mixed(context['cat_name'])
                context['cat_name_plural'] = make_plural(context['cat_name'])
                context['cat_name_plural_under'] = camel_to_under(context['cat_name_plural'])
                context['cat_name_plural_lower'] = context['cat_name_plural'].lower()
                context['cat_name_plural_mixed'] = camel_to_mixed(context['cat_name_plural'])
            if 'return_cat_name' in context:
                context['return_cat_name_under'] = camel_to_under(context['return_cat_name'])
                context['return_cat_name_lower'] = context['return_cat_name'].lower()
                context['return_cat_name_mixed'] = camel_to_mixed(context['return_cat_name'])
            if 'Proxy' in context['interface_name']:
                context['non_proxy_interface_name'] = ''.join(context['interface_name'].split('Proxy'))
            if ('return_pkg' in context and 'return_module' in context and
                    context['package_name'] == context['return_pkg'] and
                    context['module_name'] == context['return_module']):
                context['import_str'] = ''
            elif ('package_name' in context and 'return_pkg' in context and
                  'return_type' in context and 'return_module' in context):
                context['import_str'] = '{}from ..{}.{} import {}\n'.format(self._dind,
                                                                            context['return_implpkg_name'],
                                                                            context['return_module'],
                                                                            context['return_type'])

            if 'method_name' in context and context['method_name'].startswith('can_'):
                context['func_name'] = context['method_name'].split('_')[1]

            # Special one for services test builder:
            if is_manager_session(interface, patterns, package_name):
                context['svc_mgr_or_catalog'] = 'svc_mgr'
            else:
                context['svc_mgr_or_catalog'] = 'catalog'

        # Uncomment next line to identify on which method a KeyError is occurring
        #print interface['shortname'], method['name']
        return context

    def _make_method(self, method, package_name, interface, patterns):
        if self._is('abc'):
            decorator = self._ind + '@abc.abstractmethod'
            args = ['self']
            method_impl = self._make_method_impl(method, package_name, interface, patterns)

            for arg in method['args']:
                args.append(arg['var_name'])

            method_sig = '{}def {}({}):'.format(self._ind,
                                                method['name'],
                                                ', '.join(args))

            method_doc = self._build_method_doc(method)

            return (decorator + '\n' +
                    self._wrap(method_sig) + '\n' +
                    self._wrap(method_doc) + '\n' +
                    self._wrap(method_impl))
        elif self._is('mongo') or self._is('services') or self._is('authz') or self._is('tests'):
            args = ['self']
            decorator = ''
            method_sig = ''
            method_impl = self._make_method_impl(method, package_name, interface, patterns)

            if self._is('mongo'):
                if self.extra_templates_exists(package_name, method, interface, patterns, '_arg_template'):
                    arg_context = self._get_method_context(package_name, method, interface, patterns)
                    arg_default_map = self.get_arg_default_map(arg_context,
                                                               package_name,
                                                               method,
                                                               interface,
                                                               patterns)
                else:
                    arg_default_map = {}

                for arg in method['args']:
                    if arg['var_name'] in arg_default_map:
                        args.append(arg['var_name'] + '=' + arg_default_map[arg['var_name']])
                    else:
                        args.append(arg['var_name'])

                decorator = '{}@utilities.arguments_not_none'.format(self._ind)
                method_sig = '{}def {}({}):'.format(self._ind,
                                                    method['name'],
                                                    ', '.join(args))
            elif self._is('services'):
                # The following method sig builder specifically creates the arguments.  It
                # is the one used by most of the other builders.
                interface_name = interface['shortname']
                if interface_name.endswith('List') or method['name'] == 'initialize':
                    args += [arg['var_name'] for arg in method['args']]
                    method_sig = '{}def {}({}):'.format(self._ind,
                                                        method['name'],
                                                        ', '.join(args))
                # The following method sig builder uses *args, **kwargs for all methods. It is used
                # by the dlkit builder to pass arguments in the blind.
                elif (method['args'] or interface_name.endswith('Manager') and
                        not 'Runtime' in interface_name):
                    method_sig = '{}def {}(self, *args, **kwargs):'.format(self._ind,
                                                                           method['name'])
                else:
                    method_sig = '{}def {}(self):'.format(self._ind,
                                                          method['name'])
            elif self._is('authz'):
                args += [a['var_name'] for a in method['args']]
                method_sig = '{}def {}({}):'.format(self._ind,
                                                    method['name'],
                                                    ', '.join(args))
            elif self._is('tests'):
                method_sig = '{}def test_{}({}):'.format(self._ind,
                                                         method['name'],
                                                         ', '.join(args))

                if method_impl == '{}pass'.format(self._dind):
                    method_sig = '{}@unittest.skip(\'unimplemented test\')\n{}'.format(self._ind,
                                                                                       method_sig)

            detail_docs = filter(None, [method['arg_doc'].strip('\n'),
                                        method['return_doc'].strip('\n'),
                                        method['error_doc'].strip('\n'),
                                        method['compliance_doc'].strip('\n'),
                                        method['impl_notes_doc'].strip('\n')])

            if self._is('tests'):
                method_doc = '{}\"\"\"Tests {}\"\"\"'.format(self._dind,
                                                             method['name'])
            else:
                if method['doc']['body'].strip() == '' and not detail_docs:
                    method_doc = self._wrap('{}\"\"\"{}\"\"\"'.format(self._dind,
                                                                      method['doc']['headline']))
                elif method['doc']['body'].strip() == '':
                    method_doc = '{0}\"\"\"{1}\n\n{2}\n\n{0}\"\"\"'.format(self._dind,
                                                                           self._wrap(method['doc']['headline']),
                                                                           self._wrap('\n'.join(detail_docs)))
                else:
                    method_doc = '{0}\"\"\"{1}\n\n{2}\n\n{3}\n\n{0}\"\"\"'.format(self._dind,
                                                                                  self._wrap(method['doc']['headline']),
                                                                                  self._wrap(method['doc']['body']),
                                                                                  self._wrap('\n'.join(detail_docs)))

            if self._is('services') or self._is('authz'):
                return method_sig + '\n' + method_impl
            else:
                if len(args) > 1:
                    return decorator + '\n' + method_sig + '\n' + method_doc + '\n' + method_impl
                else:
                    return method_sig + '\n' + method_doc + '\n' + method_impl

    def _make_method_impl(self, method, package_name, interface, patterns):
        def stripn(_string):
            return _string.strip('\n')

        if self._is('abc'):
            if method['return_type'].strip():
                return '{}return # {}'.format(self._dind,
                                              method['return_type'])
            else:
                return '{}pass'.format(self._dind)
        else:
            impl = ''
            pattern = ''
            templates = None
            interface_sn = interface['shortname']
            method_n = method['name']

            if self._is('services'):
                if ('implemented_view_methods' in patterns and
                        method_n in patterns['implemented_view_methods']):
                    raise SkipMethod()
                elif 'implemented_view_methods' in patterns:
                    patterns['implemented_view_methods'].append(method_n)

            if interface_sn + '.' + method_n in patterns:
                pattern = patterns[interface_sn + '.' + method_n]['pattern']

            impl_class = self._load_impl_class(package_name, interface_sn)

            template_class = None
            if pattern:
                try:
                    templates = import_module(self._package_templates(self.first(pattern)))
                except ImportError:
                    pass
                else:
                    if hasattr(templates, pattern.split('.')[-2]):
                        template_class = getattr(templates, pattern.split('.')[-2])

            if self._is('services'):
                # Check if this method is marked to be skipped (the assumption
                # is that it will be implemented elsewhere, perhaps in an init.)
                if (impl_class and
                        hasattr(impl_class, method_n) and
                        getattr(impl_class, method_n) is None):
                    raise SkipMethod()

            context = self._get_method_context(package_name, method, interface, patterns)

            template_name = self.last(pattern) + '_template'

            if self._is('services'):
                if interface_sn.endswith('ProxyManager'):
                    pass
                elif interface_sn.endswith('Manager') and 'session' in method_n:
                    if patterns[method_n[4:].split('_for_')[0] + '.is_manager_session']:
                        template_name = self.last(pattern) + '_managertemplate'
                    elif patterns[method_n[4:].split('_for_')[0] + '.is_catalog_session']:
                        template_name = self.last(pattern) + '_catalogtemplate'

            # Check if there is a 'by hand' implementation available for this method
            if (impl_class and
                    hasattr(impl_class, method_n)):
                impl = stripn(getattr(impl_class, method_n))

            # If there is no 'by hand' implementation, get the template for the
            # method implementation that serves as the pattern, if one exists.
            elif (template_class and
                  hasattr(template_class, template_name)):

                if self._is('services') and getattr(template_class, template_name) is None:
                    raise SkipMethod()

                template_str = stripn(getattr(template_class, template_name))
                template = string.Template(template_str)
                impl = stripn(template.substitute(context))

            if self._is('mongo'):
                if impl == '':
                    impl = '{}raise errors.Unimplemented()'.format(self._dind)
                else:
                    if (interface['category'] in patterns['impl_log'] and
                            interface_sn in patterns['impl_log'][interface['category']]):
                        patterns['impl_log'][context['module_name']][interface_sn][method_n][1] = 'implemented'
            elif self._is('services'):
                un_impl_doc = '{}\"\"\"Pass through to provider unimplemented\"\"\"\n'.format(self._dind)

                if impl == '' and method['args']:
                    impl = ('{}{}raise Unimplemented(\'Unimplemented in dlkit.services - ' +
                            'args=\' + str(args) + \', kwargs=\' + str(kwargs))').format(un_impl_doc,
                                                                                         self._dind)
                elif impl == '' and not method['args']:
                    impl = '{}{}raise Unimplemented(\'Unimplemented in dlkit.services\')'.format(un_impl_doc,
                                                                                                 self._dind)
            elif self._is('authz'):
                if impl == '':
                    impl = '{}raise Unimplemented()'.format(self._dind)
            elif self._is('tests'):
                if impl == '':
                    impl = '{}pass'.format(self._dind)
                else:
                    if (interface['category'] in patterns['impl_log'] and
                            interface_sn in patterns['impl_log'][interface['category']]):
                        patterns['impl_log'][context['module_name']][interface_sn][method_n][1] = 'implemented'

            return impl

    def get_methods_templated_imports(self, package_name, interface, patterns):
        """get all the method-level imports that require arguments, and
        group them into a single interface-level import"""
        imports = []
        for method in interface['methods']:
            if (interface['category'] == 'managers' and
                    package_name != 'osid' and
                    interface['shortname'].endswith('Manager') and
                    method['name'].startswith('get') and
                    'session' in method['name'] and
                    self.last(method['return_type']) not in sessions_to_implement):
                continue
            if (interface['category'] == 'managers' and
                    package_name != 'osid' and
                    interface['shortname'].endswith('Profile') and
                    method['name'].startswith('supports_') and
                    under_to_caps(method['name'][9:]) + 'Session' not in sessions_to_implement):
                continue

            if self.extra_templates_exists(package_name, method, interface, patterns, '_import_templates'):
                arg_context = self._get_method_context(package_name, method, interface, patterns)
                imports += self.get_templated_imports(arg_context, package_name, method, interface, patterns)
            else:
                continue

        return imports

    def make_methods(self, package_name, interface, patterns):
        body = []

        for method in interface['methods']:
            if self._is('mongo') or self._is('tests'):
                if method['name'] == 'read' and interface['shortname'] == 'DataInputStream':
                    method['name'] = 'read_to_buffer'
            elif self._is('services'):
                if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentResultsSession':
                    method['name'] = 'get_taken_items'
                if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentBasicAuthoringSession':
                    method['name'] = 'get_assessment_items'

            if ((self._is('mongo') or self._is('services') or self._is('authz') or self._is('tests')) and
                    not build_this_method(package_name, interface, method)):
                continue

            try:
                body.append(self._make_method(method, package_name, interface, patterns))
            except SkipMethod:
                # Only expected from kitosid / services builder
                pass
            else:
                if not self._is('tests'):
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


def build_this_method(package_name, interface, method):
    if (interface['category'] == 'managers' and
            package_name != 'osid' and
            interface['shortname'].endswith('Manager') and
            method['name'].startswith('get') and
            'session' in method['name'] and
            method['return_type'].split('.')[-1] not in sessions_to_implement):
        return False

    if (interface['category'] == 'managers' and
            package_name != 'osid' and
            interface['shortname'].endswith('Profile') and
            method['name'].startswith('supports_') and
            under_to_caps(method['name'][9:]) + 'Session' not in sessions_to_implement):
        return False
    return True



def one_arg_set(method):
    return method['name'].startswith('set_') and len(method['args']) == 1

def set_and_del_property(method):
    prop = '    '
    method_name = strip_prefixes(method['name'])

    prop += fix_reserved_word(method_name)

    clear_method = 'clear_' + method_name
    set_method = 'set_' + method_name

    prop += ' = property(fset={}, fdel={})'.format(set_method,
                                                   clear_method)
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

    prop += ' = property(f{}={})'.format(prop_type,
                                         method_name)
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
