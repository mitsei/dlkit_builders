class SubjectHierarchyDesignSession:
    add_root_subject_template = """
        # Implemented from template for
        # osid.ontology.SubjectHierarchyDesignSession.add_root_subject_template
        return self._hierarchy_session.add_root(id_=${arg0_name})"""

    add_child_subject_template = """
        # Implemented from template for
        # osid.ontology.SubjectHierarchyDesignSession.add_child_subject_template
        return self._hierarchy_session.add_child(id_=${arg0_name}, child_id=${arg1_name})"""

    remove_root_subject_template = """
        # Implemented from template for
        # osid.ontology.SubjectHierarchyDesignSession.remove_root_subject_template
        return self._hierarchy_session.remove_root(id_=${arg0_name})"""

    can_modify_subject_hierarchy_template = """
        # Implemented from template for
        # osid.ontology.SubjectHierarchyDesignSession.can_modify_subject_hierarchy_template
        return True"""

    remove_child_subject_template = """
        # Implemented from template for
        # osid.ontology.SubjectHierarchyDesignSession.remove_child_subject_template
        return self._hierarchy_session.remove_child(id_=${arg0_name}, child_id=${arg1_name})"""

    remove_child_subjects_template = """
        # Implemented from template for
        # osid.ontology.SubjectHierarchyDesignSession.remove_child_subjects_template
        return self._hierarchy_session.remove_children(id_=${arg0_name})"""
