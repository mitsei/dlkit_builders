from interface_builders import InterfaceBuilder
from build_controller import BaseBuilder

class MongoBuilder(BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(MongoBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/mongo'
        self._template_dir = self._abs_path + '/builders/mongoosid_templates'

        self.interface_builder = InterfaceBuilder('mongo',
                                                  self._root_dir,
                                                  self._template_dir)

    def make(self):
        self.interface_builder.make_osids()
