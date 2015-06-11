import os
import json
import glob

from method_builders import MethodBuilder
from build_controller import BaseBuilder
from mappers import Mapper

# These next two are here for the purpose of loading abc modules
# in a django app, where the goal is to distribute the abc osids
# across the service kit packages.
# from djbuilder_settings import APPNAMEPREFIX as app_prefix
# from djbuilder_settings import APPNAMESUFFIX as app_suffix


class ABCBuilder(Mapper, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(ABCBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path

        self.method_builder = MethodBuilder(method_class='abc')

        self._abc_dir = build_dir + '/abstract_osids'
        self._app_prefix = ''
        self._abc_prefix = ''
        self._app_suffix = ''
        self._abc_suffix = ''
        self._make_dir(self._abc_dir)

    # The following functions return the app name and module name strings
    # by prepending and appending the appropriate suffixes and prefixes. Note
    # that the django app_name() function is included to support building of
    # the abc osids into a Django project environment.
    def _abc_pkg_name(self, string):
        return self._abc_prefix + '_'.join(string.split('.')) + self._abc_suffix

    def _app_name(self, package):
        if self._abc_dir:
            return self._abc_dir
        else:
            return self._app_prefix + package['name'] + self._app_suffix

    def _abc_module(self, package, module):
        return self._abc_pkg_path(package) + '/' + module + '.py'

    def _abc_pkg_path(self, package):
        return self._app_name(package) + '/' + self._abc_pkg_name(package['name'])


