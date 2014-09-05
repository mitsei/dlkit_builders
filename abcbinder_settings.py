##
# This module contains a number of setting for use by the abcbinder.py code
# and any interface builders that need to know where to find the xosid
# specs as well as the package and module names for inheriting the python
# osid abstract base classes.

##
# The xosid namespace prefix (this may be aquired from the xml somehow?).
XOSIDNAMESPACEPREFIX = 'xosid'

##
# The xosid namespace URI (this may be aquired from the xml somehow?).
XOSIDNAMESPACEURI = '{urn:inet:osid.org:schemas/osid/3}'

##
# The suffix of the xosid package files downloaded from Assembla.  This is 
# used to iterate over the approprite files in the XOSIDDIRECTORY.
XOSIDFILESUFFIX = 'xosid.xml'

##
# The directory path where the *.xosid.xml files for service to be built.  
# Copy osid definition files to this directory for processing.
XOSIDDIRECTORY = 'xosid'

##
# The directory path where the osid package json files for service are stored.  
# These get build from the xosids via the mappers.
PKGMAPSDIRECTORY = './builders/package_maps'

##
# The directory path where the json files that hold osid interface category
# mappings live.  One can also find this information in the json osid
# packages, but these are smaller and perhaps quicker to load when needed
# and will take up less memory if you want to keep some around for awhile.  
# These get build from the xosids via the mappers.
INTERFACMAPSDIRECTORY = './builders/interface_maps'

##
# The packate name to be used for the abstract base class osids if the
# intention is to create all the abc osids in one package.  The 
# binder will create a directory of this name if it doesn't already 
# exist and insert a __init__.py file to create the package.  If None
# is specified, then the abc_binder will distribute abcs based on the
# kit package name specified elsewhere
ABCROOTPACKAGE = './dlkit/abstract_osid'

##
# The prefix, if any, to be given to all abstract base class osid modules:
ABCPREFIX = ''

##
# The suffix, if any, to be given to all abstract base class osid modules:
ABCSUFFIX = ''

##
# The utf encoding to be declared by all abc osid modules:
ENCODING = '# -*- coding: utf-8 -*-\n'

##
# The indent string for first-level documentation indentation:
MAINDOCINDENTSTR = ''

##
# The utf encoding comment line to be declared by all djosid modules:
ENCODING = '# -*- coding: utf-8 -*-\n'

