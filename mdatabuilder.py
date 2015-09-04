from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder


class MDataBuilder(BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(MDataBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/mongo'
        self._template_dir = self._abs_path + '/builders/package_maps'

        self.interface_builder = InterfaceBuilder('mdata',
                                                  self._root_dir,
                                                  self._template_dir)

    def make(self):
        self.interface_builder.make_osids()