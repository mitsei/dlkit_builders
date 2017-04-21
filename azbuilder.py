from build_dlkit import BaseBuilder
from interface_builders import InterfaceBuilder


class AZBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(AZBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/authz_adapter'
        self._template_dir = self._abs_path + '/builders/azosid_templates'

        self._class = 'authz'

    def _clean_up_impl(self, impl, interface, method):
        if impl == '':
            impl = '{}raise Unimplemented()'.format(self._dind)
        return impl

    def _get_method_decorators(self, method, interface, args):
        # This should be re-implemented to template patterns somehow
        decorators = []
        if len(args) > 1:
            decorators.append('{0}@raise_null_argument'.format(self._ind))
        return decorators

    def _compile_method(self, args, decorators, method_sig, method_doc, method_impl):
        if decorators:
            decorators = '\n'.join(decorators)
            return decorators + '\n' + method_sig + '\n' + method_impl
        else:
            return method_sig + '\n' + method_impl

    def _get_method_args(self, method, interface):
        args = ['self']
        args += [a['var_name'].strip() for a in method['args']]
        return args

    def _get_method_sig(self, method, interface):
        args = self._get_method_args(method, interface)
        method_sig = '{}def {}({}):'.format(self._ind,
                                            method['name'],
                                            ', '.join(args))
        return method_sig

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']

        self.append(imports, self._abc_package_imports(interface))
        self._append_pattern_imports(imports, interface)
        inherit_category = self._append_inherited_imports(imports, interface)

        package = self.package['name']
        cat = interface['category']

        if package == 'osid' and cat not in ['markers', 'sessions']:
            # Add the osid_error import
            self.append(imports,
                        'from ..osid.osid_errors import Unimplemented, IllegalState, NullArgument')
            # Add the primitive import
            self.append(imports, 'from ..primitives import Id')
        elif package == 'osid' and cat == 'markers':
            # Add the osid_error import
            self.append(imports, 'from ..osid.osid_errors import Unimplemented')
        elif package == 'osid' and cat == 'sessions':
            # Add the osid_error import
            self.append(imports, 'from ..osid.osid_errors import IllegalState, Unimplemented')
            # Add the primitive import
            self.append(imports, 'from ..primitives import Id')
        elif cat == 'managers' and inherit_category != 'UNKNOWN_MODULE':
            # Add the osid_error import
            self.append(imports, 'from ..osid.osid_errors import Unimplemented, OperationFailed')
            # Add the session import
            self.append(imports, 'from . import sessions')
            # Add the primitive import
            self.append(imports, 'from ..primitives import Id')
        elif cat == 'sessions' and not package == 'osid' and inherit_category != 'UNKNOWN_MODULE':
            # Add the primitive import
            self.append(imports, 'from ..primitives import Id')
            # Add the osid_error import
            self.append(imports,
                        'from ..osid.osid_errors import PermissionDenied, NullArgument, Unimplemented')
        self.append(imports, 'from ..utilities import raise_null_argument')

        self._append_templated_imports(imports, interface)

    def build_this_interface(self, interface):
        return (self.package['name'] not in ['proxy'] and
                (interface['category'] in ['sessions', 'managers'] or
                interface['shortname'] in ['Sourceable']))

    def class_doc(self, interface):
        return ('{0}\"\"\"Adapts underlying {1} methods' +
                'with authorization checks.\"\"\"').format(self._ind,
                                                           interface['shortname'])

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return ('\"\"\"AuthZ Adapter implementations of ' + self.package['name'] + ' ' + module + '.\"\"\"\n' +
                '# pylint: disable=no-init\n' +
                '#     Numerous classes don\'t require __init__.\n' +
                '# pylint: disable=too-many-public-methods\n' +
                '#     Number of methods are defined in specification\n' +
                '# pylint: disable=too-many-ancestors\n' +
                '#     Inheritance defined in specification')
