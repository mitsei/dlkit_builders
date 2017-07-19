import os
import sys
import pprint
import string
import datetime

from importlib import import_module

from binder_helpers import under_to_caps
from build_dlkit import BaseBuilder
from config import sessions_to_implement
from interface_builders import InterfaceBuilder


class JSONBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(JSONBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/json_'
        self._template_dir = self._abs_path + '/templates'

        self._class = 'json'

    def _clean_up_impl(self, impl, interface, method):
        if impl == '':
            impl = '{}raise errors.Unimplemented()'.format(self._dind)
        else:
            context = self._get_method_context(method, interface)
            interface_sn = interface['shortname']
            method_n = method['name']
            interface_cat = interface['category']
            if (interface_cat in self.patterns['impl_log'] and
                    interface_sn in self.patterns['impl_log'][interface_cat]):
                self.patterns['impl_log'][context['module_name']][interface_sn][method_n][1] = 'implemented'
        return impl

    def _get_method_args(self, method, interface):
        args = ['self']
        if self.extra_templates_exists(method, interface, '_arg_template'):
            arg_context = self._get_method_context(method, interface)
            arg_default_map = self.get_arg_default_map(arg_context,
                                                       method,
                                                       interface)
        else:
            arg_default_map = {}

        for arg in method['args']:
            if arg['var_name'] in arg_default_map:
                args.append(arg['var_name'] + '=' + arg_default_map[arg['var_name']])
            else:
                args.append(arg['var_name'])

        if 'args' in arg_default_map and arg_default_map['args']:
            args.append('*args')
        if 'kwargs' in arg_default_map and arg_default_map['args']:
            args.append('**kwargs')
        return args

    def _get_method_decorators(self, method, interface, args):
        # This should be re-implemented to template patterns somehow
        decorators = []
        if 'OsidManager' in interface['inherit_shortnames'] and 'session' in method['name']:
            decorators.append('{0}@utilities.remove_null_proxy_kwarg'.format(self._ind))
        if len(args) > 1:
            decorators.append('{0}@utilities.arguments_not_none'.format(self._ind))
        if method['name'] in ['create_assessment_part_for_assessment',
                              'create_assessment_part_for_assessment_part',
                              'delete_assessment_part']:
            decorators.append('{0}@utilities.handle_simple_sequencing'.format(self._ind))
        if interface['shortname'] == 'AssessmentSession' and method['name'] in [
                'get_first_assessment_section',
                'has_next_assessment_section',
                'get_next_assessment_section',
                'has_previous_assessment_section',
                'get_previous_assessment_section',
                'get_assessment_section',
                'get_assessment_sections',
                'get_incomplete_assessment_sections',
                'finished_assessment_section',
                'requires_synchronous_responses',
                'get_first_question',
                'has_next_question',
                'get_next_question',
                'has_previous_question',
                'get_previous_question',
                'get_question',
                'get_questions',
                'get_response_form',
                'submit_response',
                'skip_item',
                'is_question_answered',
                'get_unanswered_questions',
                'has_unanswered_questions',
                'get_first_unanswered_question',
                'has_next_unanswered_question',
                'get_next_unanswered_question',
                'has_previous_unanswered_question',
                'get_previous_unanswered_question',
                'get_response',
                'get_responses',
                'finish_assessment_section',
                'finish_assessment',
                'is_answer_available',
                'get_answers']:
            decorators.append('{0}@check_effective'.format(self._ind))
        return decorators

    def _get_method_sig(self, method, interface):
        args = self._get_method_args(method, interface)
        method_sig = '{0}def {1}({2}):'.format(self._ind,
                                               method['name'],
                                               ', '.join(args))
        return method_sig

    def _make_profile_py(self):
        """create the profile.py file for this package"""
        profile = {
            'VERSIONCOMPONENTS': [0, 1, 0],
            'RELEASEDATE': '',
            'SUPPORTS': []
        }
        old_supports = []
        osid_package = self.package['name']
        try:
            # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            if self._root_dir not in sys.path:
                parent_path = os.path.abspath(os.path.join(self._abs_path, os.pardir))
                sys.path.insert(0, parent_path)
            dlkit_parent_dir = os.path.abspath(os.path.join(self._build_dir, os.pardir))
            if dlkit_parent_dir not in sys.path:
                sys.path.insert(0, dlkit_parent_dir)
            profile_module = '{}.{}.profile'.format(self._import_path(self._root_dir, limited=False),
                                                    self._abc_pkg_name(abc=False))
            old_profile = import_module(profile_module)
        except ImportError:
            print('Old Profile not found: {0}'.format(self._abc_pkg_name(abc=False)))
        else:
            if hasattr(old_profile, 'VERSIONCOMPONENTS'):
                profile['VERSIONCOMPONENTS'] = old_profile.VERSIONCOMPONENTS

            if hasattr(old_profile, 'SUPPORTS'):
                old_supports = old_profile.SUPPORTS

        profile['VERSIONCOMPONENTS'][2] += 1
        profile['RELEASEDATE'] = str(datetime.date.today())
        profile['SUPPORTS'].extend(["# Remove the # when implementations exist:",
                                    "#supports_journal_rollback",
                                    "#supports_journal_branching"])

        # Find the Profile interface for this package
        if not any('OsidProfile' in i['inherit_shortnames'] for i in self.package['interfaces']):
            return ''
        else:
            profile_interface = [i for i in self.package['interfaces']
                                 if 'OsidProfile' in i['inherit_shortnames']][0]

        for method in profile_interface['methods']:
            if (len(method['args']) == 0 and
                    method['name'].startswith('supports_')):
                supports_str = ''
                # Check to see if support flagged in builder config OR
                # Check to see if someone activated support by hand
                if '-{0}'.format(method['name']) in old_supports:
                    supports_str += '-'
                elif (under_to_caps(method['name'])[8:] + 'Session' in sessions_to_implement or
                        method['name'] in old_supports):
                    pass
                # Check to see if someone de-activated support by hand OR
                elif method['name'] not in old_supports:
                    supports_str += '#'
                else:  # Add check for session implementation flags here
                    supports_str += '#'

                supports_str += method['name']
                profile['SUPPORTS'].append(str(supports_str))

        profile = serialize(profile)

        try:
            from jsonosid_templates import package_profile
            template = string.Template(package_profile.PROFILE_TEMPLATE)
        except (ImportError, AttributeError):
            return ''
        else:
            return template.substitute({'osid_package': osid_package,
                                        'version_str': profile['VERSIONCOMPONENTS'],
                                        'release_str': profile['RELEASEDATE'],
                                        'supports_str': profile['SUPPORTS']})

    def _update_module_imports(self, modules, interface):
        imports = modules[interface['category']]['imports']

        self.append(imports, self._abc_package_imports(interface))
        self._append_inherited_imports(imports, interface)
        self._append_pattern_imports(imports, interface)
        # add the none-argument check import if not already present
        self.append(imports, 'from .. import utilities')
        self._append_templated_imports(imports, interface)

    def build_this_interface(self, interface):
        return self._build_this_interface(interface)

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return ('\"\"\"JSON implementations of ' + self.package['name'] + ' ' + module + '.\"\"\"\n\n' +
                '# pylint: disable=no-init\n' +
                '#     Numerous classes don\'t require __init__.\n' +
                '# pylint: disable=too-many-public-methods,too-few-public-methods\n' +
                '#     Number of methods are defined in specification\n' +
                '# pylint: disable=protected-access\n' +
                '#     Access to protected methods allowed in package json package scope\n' +
                '# pylint: disable=too-many-ancestors\n' +
                '#     Inheritance defined in specification')

    def write_license_file(self):
        with open(self._abc_module('summary_doc', abc=False, extension='txt'), 'w') as write_file:
            write_file.write((self._utf_code +
                              self.package['title'] + '\n' +
                              self.package['name'] + ' version ' +
                              self.package['version'] + '\n\n' +
                              self._wrap(self.package['summary'])).encode('utf-8') +
                             '\n')

    def write_profile_file(self):
        # Assemble and write profile.py file for this package.
        new_profile = self._make_profile_py()
        with open(self._abc_module('profile', abc=False), 'w') as write_file:
            write_file.write(new_profile)


def serialize(var_dict):
    """an attempt to make the builders more variable-based, instead of
    purely string based..."""
    return_dict = {}
    ppr = pprint.PrettyPrinter(indent=4)

    for k, v in var_dict.iteritems():
        if isinstance(v, basestring):
            return_dict[k] = k + ' = "' + str(v) + '"'
        elif isinstance(v, list) and len(v) <= 3:  # this is stupid and horrible, I know
            return_dict[k] = k + ' = ' + str(v)
        elif isinstance(v, list):
            # manually do lists instead of using pprint because
            # the first line indentation was breaking pep8 checks
            return_dict[k] = '{0} = [  # \'{1}\'\n'.format(k, v[0][2::])
            for value in v[1::]:
                if '#' in value:
                    return_dict[k] += '    # \'{0}\',\n'.format(value.replace('#', ''))
                else:
                    return_dict[k] += '    \'{0}\',\n'.format(value)
            return_dict[k] += ']'
        elif isinstance(v, dict):
            return_dict[k] = k + ' = ' + ppr.pformat(v)

    return return_dict
