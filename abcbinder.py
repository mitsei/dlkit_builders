from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder
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

        self._root_dir = build_dir + '/abstract_osids'
        self._make_dir(self._root_dir)

        self.interface_builder = InterfaceBuilder('abc',
                                                  self._root_dir)

    def make(self):
        self.interface_builder.make_osids(build_abc=True)



