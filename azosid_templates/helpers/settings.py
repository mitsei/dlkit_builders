# -*- coding: utf-8 -*-

ANCHOR_PATH = 'dlkit.authz_adapter'

AUTHZ_MANAGER_MODULE_PATH = '..stupid_authz_impls.time_based_authz'

PROVIDER_MANAGER_MODULE_PATHS = {
    'assessment': '..mongo.assessment.managers',
    'authentication_process': '..mongo.authentication_process.managers',
    'authorization': '..mongo.authorization.managers',
    'commenting': '..mongo.commenting.managers',
    'grading': '..mongo.grading.managers',
    'hierarchy': '..mongo.hierarchy.managers',
    'id': '..mongo.id.managers',
    'learning': '..mongo.learning.managers',
    'locale': '..mongo.locale.managers',
    'mapping': '..mongo.mapping.managers',
    'proxy': '..mongo.proxy.managers',
    'relationship': '..mongo.relationship.managers',
    'repository': '..mongo.repository.managers',
    'resource': '..mongo.resource.managers',
    'type': '..mongo.type.managers',
    }
