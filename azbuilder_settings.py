##
# This module contains a number of setting for use by the djbuilder code

##
# The packate name to be used for the osid implementations if the
# intention is to create all the implementations in one package.  The 
# binder will create a directory of this name if it doesn't already 
# exist and insert a __init__.py file to create the package.  If None
# is specified, then the builder will distribute impls based on the
# kit package name specified elsewhere
ROOTPACKAGE = './dlkit/authz_adapter'

##
# The relative path to the azbuilder implementation root directory
ROOTPATH = '..'

##
# The prefix, if any, to be applied to the Django app for this toolkit:
APPNAMEPREFIX = ''

##
# The suffix, if any, to be applied to the Django app for this toolkit:
APPNAMESUFFIX = ''

##
# The prefix (if any) to be applied to Django-aware osid packages:
PACKAGEPREFIX = ''

##
# The suffix (if any) to be applied to Django-aware osid packages:
PACKAGESUFFIX = ''

##
# The prefix (if any) to be applied to Django-aware osid sub-packages:
SUBPACKAGEPREFIX = ''

##
# The suffix (if any) to be applied to Django-aware osid sub-packages:
SUBPACKAGESUFFIX = ''

##
# The root path for the abstract base class osids:
ABCROOTPACKAGE = '...abstract_osid'

##
# The prefix, if any, to be given to all abstract base class module variables
# for populating inheritance:
ABCPREFIX = ''

##
# The suffix, if any, to be given to all abstract base class module variables
# for populating inheritance:
ABCSUFFIX = ''

##
# The utf encoding comment line to be declared by all djosid modules:
ENCODING = '# -*- coding: utf-8 -*-\n'

##
# The location of the directory that contains the templates
TEMPLATEDIR = 'builders/azosid_templates'
