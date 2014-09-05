from abcbinder_settings import XOSIDDIRECTORY as xosid_dir
#from abcbinder_settings import XOSIDFILESUFFIX as xosid_suffix
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import INTERFACMAPSDIRECTORY as interface_maps_dir
from xosid_mapper import map_xosid
from collections import OrderedDict
import os
import json
xosid_suffix = 'xosid'

def map_all(map_type = 'all'):
    make_package_keywords = ['all', 'interface', 'i']
    make_interface_keywords = ['all', 'package', 'pkg', 'p']
    make_impl_pattern_keywords = ['all', 'impl', 'patterns']
    package = None
    for xosid_file in os.listdir(xosid_dir):
        if xosid_file.endswith(xosid_suffix):
            if map_type in make_package_keywords:
                print 'mapping osid package', xosid_file + '.'
                package = make_xosid_map(xosid_dir + '/' + xosid_file)
            if map_type in make_interface_keywords:
                print 'creating interface map for', xosid_file.split('.')[-2], 'osid.'
                make_interface_map(xosid_dir + '/' + xosid_file, package)
            if map_type in make_impl_pattern_keywords:
                print 'creating implementation pattern map for', xosid_file.split('.')[-2], 'osid.'
                make_interface_map(xosid_dir + '/' + xosid_file, package)

def make_patterns():
    sub_packages = []
    for json_file in os.listdir(pkg_maps_dir):
        if json_file.endswith('.json'):
            read_file = open(pkg_maps_dir + '/' + json_file, 'r')
            #print json_file
            package = json.load(read_file)
            read_file.close()
            if len(package['name'].split('.')) > 1:
                sub_packages.append(package)
            else:
                make_impl_pattern_map(package = package)
    for package in sub_packages:
        if package['name'].split('.')[0] + '.json' in os.listdir('./builders/pattern_maps'):
            read_file = open('./builders/pattern_maps/' + package['name'].split('.')[0] + '.json', 'r')
            base_package = json.load(read_file)
            read_file.close()
            make_impl_pattern_map(package = package, base_package = base_package)
        else:
            print 'Could not find pattern map', package['name'].split('.')[0], 'required for processing package', package['name']


def map(file_name = None, map_type = 'all'):
    package = None
    if map_type in make_package_keywords:
        print 'mapping osid package', xosid_file + '.'
        package = make_xosid_map(xosid_dir + '/' + file_name)
    if map_type in make_interface_keywords:
        print 'creating interface map', file_name.split('.')[-3], 'osid.'
        make_interface_map(xosid_dir + '/' + file_name)

def make_xosid_map(file_name):
    package = map_xosid(file_name)
    if not os.path.exists('./builders/package_maps'):
          os.system('mkdir ./builders/package_maps')
    write_file = open('./builders/package_maps/' +
                      package['name'] + '.json', 'w')
    json.dump(package, write_file, indent = 3)
    write_file.close
    return package

def make_interface_map(file_name = None, package = None):
    if package is None:
        package = map_xosid(file_name)
    if not os.path.exists('./builders/interface_maps'):
          os.system('mkdir ./builders/interface_maps')
    osid_type_index = OrderedDict()
    if package:
        for i in package['interfaces']:
            osid_type_index[package['name'] + '.' + i['shortname']] = i['category']
            if i['category'] == 'others_please_move':
                print 'Please move: ' + i['fullname']
        write_file = open('./builders/interface_maps/' +
                          package['name'] + '.json', 'w')
        json.dump(osid_type_index, write_file, indent = 3)
        write_file.close
    else:
        print 'No OSID package available.'
    return osid_type_index
    
def make_impl_pattern_map(file_name = None, package = None, **kwargs):
    from pattern_mapper import map_patterns
    if package is None:
        package = map_xosid(file_name)
    if not os.path.exists('./builders/pattern_maps'):
          os.system('mkdir ./builders/pattern_maps')
    pattern_index = OrderedDict()
    if package:
        pattern_index = map_patterns(package, pattern_index, **kwargs)
        write_file = open('./builders/pattern_maps/' +
                          package['name'] + '.json', 'w')
        json.dump(pattern_index, write_file, indent = 3)
        write_file.close
    return # pattern_index
