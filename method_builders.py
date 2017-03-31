import string
from importlib import import_module

from binder_helpers import fix_reserved_word, under_to_caps, get_pkg_name, camel_to_under, \
    camel_to_mixed, under_to_mixed, make_plural, remove_plural, SkipMethod
from build_controller import Utilities, BaseBuilder, Templates
from config import sessions_to_implement
from syntax_helpers import syntax_to_under


class MethodBuilder(BaseBuilder, Templates, Utilities):
    """class that builds methods"""
    def __init__(self, method_class=None, template_dir=None, *args, **kwargs):
        """method_class differentiates between different variations, i.e. abc
        looks different than json"""
        super(MethodBuilder, self).__init__()

    def _build_method_doc(self, method):
        detail_docs = self._get_method_doc(method)

        method_doc = '{0}\"\"\"{1}'.format(self._dind,
                                           method['doc']['headline'])

        if method['doc']['body'].strip() != '':
            method_doc += '\n\n{0}'.format(method['doc']['body'])

        if detail_docs:
            method_doc += '\n\n{0}\n\n'.format('\n'.join(detail_docs))

        method_doc += '{0}\"\"\"'.format(self._dind)
        return method_doc

    def _clean_up_impl(self, impl, interface, method):
        return impl

    def _compile_method(self, args, decorators, method_sig, method_doc, method_impl):
        if decorators:
            decorators = '\n'.join(decorators)
            return self._wrap('{0}\n{1}\n{2}\n{3}'.format(decorators,
                                                          method_sig,
                                                          method_doc,
                                                          method_impl))
        else:
            return self._wrap('{0}\n{1}\n{2}'.format(method_sig,
                                                     method_doc,
                                                     method_impl))

    def _confirm_build_method(self, impl_class, method_name):
        pass

    def _get_method_args(self, method, interface):
        return ['self']

    def _get_method_context(self, method, interface):
        """Get the method context vars, to be used in the template"""
        def construct_arg_context(arg_number, arg_type_full):
            arg_type = self.last(arg_type_full).strip('[]')
            arg_context = {
                arg_number + '_type': arg_type,
                arg_number + '_type_under': camel_to_under(arg_type),
                arg_number + '_type_mixed': camel_to_mixed(arg_type),
                arg_number + '_abcapp_name': self._app_name(package_name=get_pkg_name(arg_type_full.strip('[]')),
                                                            abstract=True),
                arg_number + '_abcpkg_name': self._abc_pkg_name(package_name=get_pkg_name(arg_type_full.strip('[]')),
                                                                abc=False),
                arg_number + '_module': self.get_interface_module(
                    self._abc_pkg_name(package_name=get_pkg_name(arg_type_full),
                                       abc=False),
                    arg_type)
            }
            return arg_context

        context = {}

        if interface['shortname'] + '.' + method['name'] in self.patterns:
            context = self.patterns[interface['shortname'] + '.' + method['name']]['kwargs']

        arg_list = []
        for arg in method['args']:
            arg_list.append(arg['var_name'])
        context['arg_list'] = ', '.join(arg_list)

        if 'package_name' in context:
            # Add keyword arguments to template kwargs that are particular
            # to the json implementation
            context['app_name'] = self._app_name()
            context['implpkg_name'] = self._abc_pkg_name(abc=False, reserved_word=False)
            context['abcapp_name'] = self._app_name()
            context['abcpkg_name'] = self._abc_pkg_name(abc=False)
            context['interface_name_under'] = camel_to_under(context['interface_name'])
            context['interface_name_dot'] = '.'.join(context['interface_name_under'].split('_')[:-1])
            context['package_name_caps'] = self.replace(self.package['name'].title(), desired='')
            context['package_name_upper'] = self.package['name'].upper()
            context['package_name_replace'] = self.replace(self.package['name'])
            context['package_name_replace_upper'] = self.replace(self.package['name']).upper()

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
                    self._abc_pkg_name(package_name=get_pkg_name(context['return_type_full']),
                                       abc=False),
                    context['return_type_full'].split('.')[-1])
            if 'return_pkg' in context:
                context['return_app_name'] = self._app_name(package_name=context['return_pkg'])
                context['return_implpkg_name'] = self._abc_pkg_name(package_name=context['return_pkg'],
                                                                    abc=False)
                context['return_pkg_title'] = context['return_pkg'].title()
                context['return_pkg_caps'] = context['return_pkg'].upper()
                context['return_pkg_replace_caps'] = self.replace(context['return_pkg'].upper())
                context['return_pkg_replace_title'] = self.replace(context['return_pkg'].title())
            if 'return_cat_name' in context:
                context['return_cat_name_under'] = camel_to_under(context['return_cat_name'])
            if 'object_name_under' in context:
                context['object_name_upper'] = context['object_name_under'].upper()
                context['object_name_mixed'] = under_to_mixed(context['object_name_under'])
                # Might want to add creating kwargs['object_name' from this as well]
            if 'object_name' in context and 'package_name' in context:
                context['object_app_name'] = self._app_name()
                context['object_implpkg_name'] = self._abc_pkg_name(abc=False)
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
            if ('containable_object_name' in context and
                    not 'containable_object_name_under' in context and
                    not 'containable_object_name_upper' in context):
                context['containable_object_name_under'] = camel_to_under(context['containable_object_name'])
                context['containable_object_name_plural'] = make_plural(context['containable_object_name'])
                context['containable_object_name_plural_under'] = camel_to_under(context['containable_object_name_plural'])
                context['containable_object_name_mixed'] = camel_to_mixed(context['containable_object_name'])
                context['containable_object_name_upper'] = camel_to_under(context['containable_object_name']).upper()
            if 'object_namespace' in context:
                context['object_package_name'] = '.'.join(context['object_namespace'].split('.')[:-1])
                context['object_package_name_replace'] = '_'.join(context['object_package_name'].split('.'))
                context['object_package_name_replace_upper'] = context['object_package_name_replace'].upper()
                context['object_namespace_replace'] = '_'.join(context['object_namespace'].split('.'))
            if ('object_name' in context and
                    not 'object_name_under' in context and
                    not 'object_name_upper' in context):
                context['object_name_plural'] = make_plural(context['object_name'])
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
                context['import_str'] = '{0}from ..{1}.{2} import {3}\n'.format(self._dind,
                                                                                context['return_implpkg_name'],
                                                                                context['return_module'],
                                                                                context['return_type'])

            if 'method_name' in context and context['method_name'].startswith('can_'):
                context['func_name'] = context['method_name'].split('_')[1]
            if 'method_name' in context:
                context['method_session_name'] = context['method_name'].replace('get_', '')
            if 'syntax' in context:
                context['syntax_under'] = syntax_to_under(context['syntax'])

            # Special one for services test builder:
            if self._is_manager_session(interface, self.package['name']):
                context['svc_mgr_or_catalog'] = 'svc_mgr'
            else:
                context['svc_mgr_or_catalog'] = 'catalog'
        return context

    def _get_method_decorators(self, method, interface, args):
        return ''

    @staticmethod
    def _get_method_doc(method):
        return filter(None, [method['arg_doc'].strip('\n'),
                             method['return_doc'].strip('\n'),
                             method['error_doc'].strip('\n'),
                             method['compliance_doc'].strip('\n'),
                             method['impl_notes_doc'].strip('\n')])

    def _get_method_sig(self, method, interface):
        pass

    def _get_pattern(self, method, interface):
        interface_sn = interface['shortname']
        method_n = method['name']
        if interface_sn + '.' + method_n in self.patterns:
            pattern = self.patterns[interface_sn + '.' + method_n]['pattern']
        else:
            pattern = ''
        return pattern

    def _get_template_name(self, pattern, interface_name, method_name):
        return self.last(pattern) + '_template'

    def _make_method(self, method, interface):
        args = self._get_method_args(method, interface)
        decorators = self._get_method_decorators(method, interface, args)
        method_sig = self._get_method_sig(method, interface)
        method_impl = self._make_method_impl(method, interface)
        method_doc = self._build_method_doc(method)

        return self._compile_method(args, decorators, method_sig, method_doc, method_impl)

    def _make_method_impl(self, method, interface):
        impl = ''
        templates = None
        interface_sn = interface['shortname']
        method_n = method['name']

        self._update_implemented_view_methods(method, interface)

        pattern = self._get_pattern(method, interface)
        impl_class = self._load_impl_class(interface_sn)

        template_class = None
        if pattern:
            try:
                templates = import_module(self._package_templates(self.first(pattern)))
            except ImportError:
                pass
            else:
                if hasattr(templates, pattern.split('.')[-2]):
                    template_class = getattr(templates, pattern.split('.')[-2])

        self._confirm_build_method(impl_class, method_n)

        context = self._get_method_context(method, interface)
        template_name = self._get_template_name(pattern, interface_sn, method_n)

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

        return self._clean_up_impl(impl, interface, method)

    def _update_implemented_view_methods(self, method, interface):
        pass

    def get_methods_templated_imports(self, package_name, interface):
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

            if self.extra_templates_exists(method, interface, '_import_templates'):
                arg_context = self._get_method_context(method, interface)
                imports += self.get_templated_imports(arg_context, package_name, method, interface)
            else:
                continue

        return imports

    def make_methods(self, interface, package_name=None):
        body = []
        if package_name is None:
            package_name = self.package['name']

        for method in interface['methods']:
            if self._in(['json', 'tests']):
                if method['name'] == 'read' and interface['shortname'] == 'DataInputStream':
                    method['name'] = 'read_to_buffer'
            elif self._in(['services']):
                if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentResultsSession':
                    method['name'] = 'get_taken_items'
                if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentBasicAuthoringSession':
                    method['name'] = 'get_assessment_items'
                if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentPartItemSession':
                    method['name'] = 'get_assessment_part_items'
                if method['name'] == 'get_items' and interface['shortname'] == 'AssessmentResultsSession':
                    method['name'] = 'get_assessment_taken_items'
                if method['name'] == 'get_responses' and interface['shortname'] == 'AssessmentResultsSession':
                    method['name'] = 'get_assessment_taken_responses'

            if (self._in(['json', 'services', 'authz', 'tests']) and
                    not build_this_method(package_name, interface, method)):
                continue
            if self._is('doc_dlkit') and not self.build_this_method(interface, method):
                continue

            try:
                body.append(self._make_method(method, interface))
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

def stripn(_string):
    return _string.strip('\n')