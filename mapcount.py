
import time
import os
import json
import string
from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import XOSIDDIRECTORY as xosid_dir
from abcbinder_settings import PKGMAPSDIRECTORY as pkg_maps_dir
from abcbinder_settings import INTERFACMAPSDIRECTORY as interface_maps_dir
from abcbinder_settings import XOSIDFILESUFFIX as xosid_suffix
from abcbinder_settings import ABCROOTPACKAGE as abc_root_pkg
from abcbinder_settings import ABCPREFIX as abc_prefix
from abcbinder_settings import ABCSUFFIX as abc_suffix
from abcbinder_settings import MAINDOCINDENTSTR as main_doc_indent
from abcbinder_settings import ENCODING as utf_code
from djbuilder_settings import ROOTPACKAGE as root_pkg
from djbuilder_settings import APPNAMEPREFIX as app_prefix
from djbuilder_settings import APPNAMESUFFIX as app_suffix
from djbuilder_settings import PACKAGEPREFIX as pkg_prefix
from djbuilder_settings import PACKAGESUFFIX as pkg_suffix
from djbuilder_settings import PATTERN_DIR as pattern_dir
from djbuilder_settings import TEMPLATE_DIR as template_dir
template_pkg = '.'.join(template_dir.split('/'))


def count_all(build_abc=False, re_index=False, re_map=False):
    # This is the entry point for counting mapped patterns across all mapped
    # osids

    total_count = [0, 0]
    for json_file in os.listdir(pattern_dir):
        if json_file.endswith('.json'):
            count_map = count(pattern_dir + '/' + json_file)
            total_count[0] += count_map[0]
            total_count[1] += count_map[1]
    print('Total {0} out of {1} methods mapped.'.format(str(total_count[0]),
                                                        str(total_count[1])))


def count(file_name):
    # This is the entry point for counting mapped patterns in one osid map

    read_file = open(file_name, 'r')
    pattern = json.load(read_file)
    read_file.close()

    mapped = 0
    all_ = 0

    for category in pattern['impl_log']:
        for interface in pattern['impl_log'][category]:
            for method in pattern['impl_log'][category][interface]:
                if 'mapped' in pattern['impl_log'][category][interface][method]:
                    mapped += 1
                all_ += 1

    mapped = float(mapped)
    all_ = float(all_)

    return [mapped, all_]
