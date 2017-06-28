class SubjectHierarchyDesignSession:
    add_root_subject_template = """
        # From azosid_templates/ontology.py::SubjectHierarchyDesignSession::add_root_subject_template
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    can_modify_subject_hierarchy_template = """
        # From azosid_templates/ontology.py::SubjectHierarchyDesignSession::can_modify_subject_hierarchy_template
        return self._can('modify')"""

    remove_root_subject_template = """
        # From azosid_templates/ontology.py::SubjectHierarchyDesignSession::remove_root_subject_template
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    add_child_subject_template = """
        # From azosid_templates/ontology.py::SubjectHierarchyDesignSession::add_child_subject_template
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    remove_child_subjects_template = """
        # From azosid_templates/ontology.py::SubjectHierarchyDesignSession::remove_child_subjects_template
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    remove_child_subject_template = """
        # From azosid_templates/ontology.py::SubjectHierarchyDesignSession::remove_child_subject_template
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""