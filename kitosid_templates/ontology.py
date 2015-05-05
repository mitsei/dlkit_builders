
class SubjectHierarchySession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    get_subject_hierarchy_id_template = None # Need to put one of these elsewhere

    get_subject_hierarchy_template = None # Need to put one of these elsewhere

    can_access_subject_hierarchy_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.can_access_subject_hierarchy_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_root_subject_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_root_subject_ids_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_root_subjects_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_root_subjects_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    has_parent_subjects_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.has_parent_subjects_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_parent_of_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_parent_of_subject_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_parent_subject_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_parent_subject_ids_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_parent_subjects_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_parent_subjects_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_ancestor_of_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_ancestor_of_subject_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    has_child_subjects_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.has_child_subjects_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_child_of_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_child_of_subject_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_child_subject_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_child_subject_ids_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_child_subjects_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_child_subjects_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_descendant_of_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_descendant_of_subject_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_subject_node_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_subject_node_ids_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_subject_nodes_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_subject_nodes_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class SubjectHierarchyDesignSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_modify_subject_hierarchy_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.can_modify_subject_hierarchy
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    add_root_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.add_root_subject
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    remove_root_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.remove_root_subject
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    add_child_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.add_child_subject
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    remove_child_subject_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.remove_child_subject
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    remove_child_subjects_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.remove_child_subjects_template
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""
