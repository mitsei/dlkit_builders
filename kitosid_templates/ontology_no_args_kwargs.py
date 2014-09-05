
class SubjectHierarchySession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    get_subject_hierarchy_id_template = None # Need to put one of these elsewhere

    get_subject_hierarchy_template = None # Need to put one of these elsewhere

    can_access_subject_hierarchy_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.can_access_subject_hierarchy_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}()"""

    get_root_subject_ids_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_root_subject_ids_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}()"""

    get_root_subjects_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_root_subjects_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}()"""

    has_parent_subjects_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.has_parent_subjects_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    is_parent_of_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_parent_of_subject_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name}, ${arg1_name})"""

    get_parent_subject_ids_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_parent_subject_ids_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_parent_subjects_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_parent_subjects_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    is_ancestor_of_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_ancestor_of_subject_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name}, ${arg1_name})"""

    has_child_subjects_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.has_child_subjects_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    is_child_of_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_child_of_subject_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_child_subject_ids_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_child_subject_ids_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_child_subjects_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_child_subjects_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    is_descendant_of_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.is_descendant_of_subject_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name}, ${arg1_name})"""

    get_subject_node_ids_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_subject_node_ids_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    get_subject_nodes_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchySession.get_subject_nodes_template
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""


class SubjectHierarchyDesignSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_modify_subject_hierarchy_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.can_modify_subject_hierarchy
        return self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}()"""

    add_root_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.add_root_subject
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    remove_root_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.remove_root_subject
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""

    add_child_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.add_child_subject
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name}, ${arg1_name})"""

    remove_child_subject_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.remove_child_subject
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name}, ${arg1_name})"""

    remove_child_subjects_template = """
        # Implemented from kitosid template for -
        # osid.ontology.SubjectHierarchyDesignSession.remove_child_subjects_template
        self._get_provider_session('${interface_name_under}', '${object_name_under}').${method_name}(${arg0_name})"""
