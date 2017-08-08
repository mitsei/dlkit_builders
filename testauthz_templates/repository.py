"""TestAuthZ templates for repository interfaces"""

from . import resource

class CompositionLookupSession:

    init_template = resource.ResourceLookupSession.init_template

    additional_methods_pattern = resource.ResourceLookupSession.additional_methods_pattern

    additional_classes_template = resource.ResourceLookupSession.additional_classes_template


