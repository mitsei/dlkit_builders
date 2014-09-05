# -*- coding: utf-8 -*-

ANCHOR_PATH = 'dlkit.services'

LEARNING_PROVIDER_MANAGER_PATH = '..handcar.learning.managers'

REPOSITORY_PROVIDER_MANAGER_PATH = '..handcar.repository.managers'

TYPE_PROVIDER_MANAGER_PATH = '..handcar.type.managers'

ID_PROVIDER_MANAGER_PATH = '..handcar.id.managers'

GRADING_PROVIDER_MANAGER_PATH = '..handcar.grading.managers'

RELATIONSHIP_PROVIDER_MANAGER_PATH = '..handcar.relationship.managers'

PROXY_PROVIDER_MANAGER_PATH = '..services_impls.proxy.managers'

ASSESSMENT_PROVIDER_MANAGER_PATH = '..mongo.assessment.managers'

LANGUAGETYPE = {
    'identifier': 'ENG',
    'namespace': '639-2',
    'authority': 'ISO',
    # The following may be optional. Time will tell.
    'domain': 'DisplayText Languages',
    'display_name': 'English Text Language',
    'display_label': 'English',
    'description': 'The display text language type for the English language.'
    }

SCRIPTTYPE = {
    'identifier': 'LATN',
    'namespace': '15924',
    'authority': 'ISO',
    # The following may be optional. Time will tell.
    'domain': 'ISO Script Types',
    'display_name': 'Latin Text Script',
    'display_label': 'Latin',
    'description': 'The display text script type for the Latin script.'
    }

FORMATTYPE = {
    'identifier': 'PLAIN',
    'namespace': 'TextFormats',
    'authority': 'okapia.net',
    # The following may be optional. Time will tell.
    'domain': 'DisplayText Formats',
    'display_name': 'Plain Text Format',
    'display_label': 'Plain',
    'description': 'The display text format type for the Plain format.'
    }

