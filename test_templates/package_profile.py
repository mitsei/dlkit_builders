"""Profile template for package profiles"""

PROFILE_TEMPLATE = """\"\"\"Mongo osid profile elements for ${osid_package} service packages\"\"\"
# -*- coding: utf-8 -*-
# pylint: disable=unused-import
#    importing common values to be used by ${osid_package}.ProfileManger implementation

from ..profile import ID
from ..profile import LANGUAGETYPE
from ..profile import SCRIPTTYPE
from ..profile import FORMATTYPE
from ..profile import VERSIONSCHEME
from ..profile import LOCALES
from ..profile import LICENSE
from ..profile import PROVIDERID
from ..profile import OSIDVERSION

DISPLAYNAME = 'Mongo ${osid_package}'

DESCRIPTION = 'MongoDB based ${osid_package} implementation'

${version_str}

${release_str}
${supports_str}
"""
