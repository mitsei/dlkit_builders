# -*- coding: utf-8 -*-
OSID_PACKAGE_PATH = 'osid_kit.osid_federator'

# Edit the following list to add or delete provider implementations
# known to this osid service federator by identifying the modules
# where the implementations' managers live. The first implementation
# manager listed will be the one that deals with default catalogs.
PROVIDER_MANAGER_MODULE_PATHS = [
'learning_kit.az_learning.managers',
'learning_kit.sc_learning.managers'
]