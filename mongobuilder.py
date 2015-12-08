import sys
import pprint
import string
import datetime

from importlib import import_module

from binder_helpers import under_to_caps
from build_controller import BaseBuilder
from config import sessions_to_implement
from interface_builders import InterfaceBuilder


class MongoBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(MongoBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/mongo'
        self._template_dir = self._abs_path + '/builders/mongoosid_templates'

        self._class = 'mongo'

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
                sys.path.insert(0, self._abs_path)
            profile_module = '{}.{}.profile'.format(self._import_path(self._root_dir, limited=False),
                                                    self._abc_pkg_name(abc=False))
            old_profile = import_module(profile_module)
        except ImportError:
            print 'Old Profile not found:', self._abc_pkg_name(abc=False)
        else:
            if hasattr(old_profile, 'VERSIONCOMPONENTS'):
                profile['VERSIONCOMPONENTS'] = old_profile.VERSIONCOMPONENTS

            if hasattr(old_profile, 'SUPPORTS'):
                old_supports = old_profile.SUPPORTS

        profile['VERSIONCOMPONENTS'][2] += 1
        profile['RELEASEDATE'] = str(datetime.date.today())
        profile['SUPPORTS'].extend(['# Remove the # when implementations exist:',
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
                if '-'+ method['name'] in old_supports:
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
            from mongoosid_templates import package_profile
            template = string.Template(package_profile.PROFILE_TEMPLATE)
        except (ImportError, AttributeError):
            return ''
        else:
            return template.substitute({'osid_package': osid_package,
                                        'version_str': profile['VERSIONCOMPONENTS'],
                                        'release_str': profile['RELEASEDATE'],
                                        'supports_str': profile['SUPPORTS']})

    def build_this_interface(self, interface):
        return self._build_this_interface(interface)

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return ('\"\"\"Mongodb implementations of ' + self.package['name'] + ' ' + module + '.\"\"\"\n\n' +
                '# pylint: disable=no-init\n' +
                '#     Numerous classes don\'t require __init__.\n' +
                '# pylint: disable=too-many-public-methods,too-few-public-methods\n' +
                '#     Number of methods are defined in specification\n' +
                '# pylint: disable=protected-access\n' +
                '#     Access to protected methods allowed in package mongo package scope\n' +
                '# pylint: disable=too-many-ancestors\n' +
                '#     Inheritance defined in specification\n')

    def write_license_file(self):
        with open(self._abc_module('summary_doc', abc=False), 'w') as write_file:
            write_file.write((self._utf_code + '\"\"\"' +
                              self.package['title'] + '\n' +
                              self.package['name'] + ' version ' +
                              self.package['version'] + '\n\n' +
                              self.package['summary'] + '\n\n\"\"\"').encode('utf-8') +
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
        elif isinstance(v, list) or isinstance(v, dict):
            return_dict[k] = k + ' = ' + ppr.pformat(v)

    return return_dict