import json
import string

from binder_helpers import camel_to_caps_under
from build_controller import BaseBuilder
from interface_builders import InterfaceBuilder


class MDataBuilder(InterfaceBuilder, BaseBuilder):
    def __init__(self, build_dir=None, *args, **kwargs):
        super(MDataBuilder, self).__init__(*args, **kwargs)
        if build_dir is None:
            build_dir = self._abs_path
        self._build_dir = build_dir
        self._root_dir = self._build_dir + '/mongo'
        self._template_dir = self._abs_path + '/builders/package_maps'

        self._class = 'mdata'

    def _make_mdata(self, file_name):
        with open(file_name, 'r') as read_file:
            self.package = json.load(read_file)

        if not self._package_to_be_implemented():
            return

        print "Building {0} for {1}".format(self._class,
                                            self.package['name'])

        self.patterns = self._patterns()

        import_str = self.module_header('')
        self._initialize_directories()

        ##
        # The real work starts here.  Iterate through all interfaces to build
        # all the model classes for this osid package.
        for interface in self.package['interfaces']:
            ##
            # Check to see if this interface is meant to be implemented.
            if self.package['name'] != 'osid' and not self._build_this_interface(interface):
                continue

            if (interface['shortname'] in self.patterns['package_objects_caps'] or
                    interface['shortname'] in self.patterns['package_relationships_caps'] or
                    interface['shortname'] == 'OsidObject' or
                    interface['category'] == 'markers' or
                    interface['shortname'] == self.patterns['package_catalog_caps']):
                imports = []

                impl_class = self._impl_class(interface)

                ##
                # Build all mdata maps, checking to see if there is a hand built
                # mdata implementation available
                if not hasattr(impl_class, 'mdata'):
                    mdata_maps = self._make_mdata_maps(interface)
                else:
                    mdata_maps = getattr(impl_class, 'mdata')
                ##
                # Assemble complete mdata string to be saved as mdata.py
                mdata = '\n{1}\n'.format(mdata_maps)

                ##
                # Finally, save the mdata to the appropriate mdata_conf.py file.
                if mdata.strip() != '':
                    with open(self._abc_module('mdata_conf'), 'wb') as write_file:
                        write_file.write((import_str + '\n'.join(imports) + '\n\n' +
                                         mdata).encode('utf-8'))

    def _make_mdata_maps(self, interface):
        from builders.mongoosid_templates import options
        pd = interface['shortname'] + '.persisted_data'
        rt = interface['shortname'] + '.return_types'
        mdata = ''
        if pd in self.patterns and self.patterns[pd] != {}:
            for data_name in self.patterns[pd]:
                if self.patterns[pd][data_name] == 'OsidCatalog':
                    pass
                elif (rt in self.patterns and
                      data_name in self.patterns[rt] and
                      self.patterns[rt][data_name] == 'osid.locale.DisplayText'):
                    mdata += self._make_mdata_map(interface['shortname'],
                                                  data_name,
                                                  'DisplayText',
                                                  options) + '\n'
                else:
                    mdata += self._make_mdata_map(interface['shortname'],
                                                  data_name,
                                                  self.patterns[pd][data_name],
                                                  options) + '\n'
        return mdata

    def _make_mdata_map(self, interface_name, data_name, data_type, options):
        def construct_data(opt, context):
            template = string.Template(options.COMMON_MDATA + opt)
            return template.substitute(context)

        mdata = None

        ctxt = {
            'element_identifier': data_name,
            'element_label': ' '.join(data_name.split('_'))
        }

        if data_type == 'boolean':
            ctxt.update({
                'instructions': 'enter either true or false.',
                'array': 'False'
            })
            mdata = construct_data(options.BOOLEAN_MDATA, ctxt)
        elif data_type == 'string':
            ctxt.update({
                'instructions': 'enter no more than 256 characters.',
                'max_length': 256,
                'array': 'False'
            })
            mdata = construct_data(options.STRING_MDATA, ctxt)
        elif data_type == 'decimal':
            ctxt.update({
                'instructions': 'enter a decimal value.',
                'array': 'False'
            })
            mdata = construct_data(options.DECIMAL_MDATA, ctxt)
        elif data_type == 'DisplayText':
            ctxt.update({
                'instructions': 'enter no more than 256 characters.',
                'max_length': 256,
                'array': 'False'
            })
            mdata = construct_data(options.DISPLAY_TEXT_MDATA, ctxt)
        elif data_type in ['osid.id.Id']:
            ctxt.update({
                'instructions': 'accepts an ' + data_type + ' object',
                'syntax': self.last(data_type).upper(),
                'id_type': self.last(data_type).lower(),
                'array': 'False'
            })
            mdata = construct_data(options.ID_MDATA, ctxt)
        elif data_type in ['osid.type.Type']:
            ctxt.update({
                'instructions': 'accepts an ' + data_type + ' object',
                'syntax': data_type.split('.')[-1].upper(),
                'id_type': data_type.split('.')[-1].lower(),
                'array': 'False'
            })
            mdata = construct_data(options.TYPE_MDATA, ctxt)
        elif data_type in ['osid.id.Id[]', 'osid.type.Type[]']:
            ctxt.update({
                'instructions': 'accepts an ' + data_type + ' object',
                'syntax': self.last(data_type).strip('[]').upper(),
                'id_type': self.last(data_type).strip('[]').lower(),
                'array': 'True'
            })
            mdata = construct_data(options.ID_LIST_MDATA, ctxt)
        elif data_type in ['osid.calendaring.DateTime', 'timestamp']:
            ctxt.update({
                'instructions': 'enter a valid datetime object.',
                'array': 'False'
            })
            mdata = construct_data(options.DATE_TIME_MDATA, ctxt)
        elif data_type == 'osid.calendaring.Duration':
            ctxt.update({
                'instructions': 'enter a valid duration object.',
                'array': 'False'
            })
            mdata = construct_data(options.DURATION_MDATA, ctxt)
        elif data_type == 'osid.transport.DataInputStream':
            ctxt.update({
                'instructions': 'accepts a valid data input stream.',
                'array': 'False'
            })
            mdata = construct_data(options.OBJECT_MDATA, ctxt)

        if mdata is not None:
            return '{0}_{1} = {{2}\n}\n'.format(camel_to_caps_under(interface_name),
                                                data_name.upper(),
                                                mdata)
        else:
            return ''

    def make(self):
        self.make_osids()

    def module_header(self, module):
        return ('\"\"\"Mongo osid metadata configurations for ' + self.package['name'] + ' service.\"\"\"\n\n' +
                '\"\"\"\nfrom .. import types\n' +
                'from ..primitives import Type\n' +
                'DEFAULT_LANGUAGE_TYPE = Type(**types.Language().get_type_data("DEFAULT"))\n' +
                'DEFAULT_SCRIPT_TYPE = Type(**types.Script().get_type_data("DEFAULT"))\n' +
                'DEFAULT_FORMAT_TYPE = Type(**types.Format().get_type_data("DEFAULT"))\n' +
                'DEFAULT_GENUS_TYPE = Type(**types.Genus().get_type_data("DEFAULT"))\"\"\"\n')