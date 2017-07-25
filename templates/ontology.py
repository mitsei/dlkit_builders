# class SubjectHierarchyDesignSession:
#     add_root_subject_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchyDesignSession.add_root_subject_template
#         return self._hierarchy_session.add_root(id_=${arg0_name})"""
#
#     add_child_subject_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchyDesignSession.add_child_subject_template
#         return self._hierarchy_session.add_child(id_=${arg0_name}, child_id=${arg1_name})"""
#
#     remove_root_subject_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchyDesignSession.remove_root_subject_template
#         return self._hierarchy_session.remove_root(id_=${arg0_name})"""
#
#     can_modify_subject_hierarchy_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchyDesignSession.can_modify_subject_hierarchy_template
#         return True"""
#
#     remove_child_subject_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchyDesignSession.remove_child_subject_template
#         return self._hierarchy_session.remove_child(id_=${arg0_name}, child_id=${arg1_name})"""
#
#     remove_child_subjects_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchyDesignSession.remove_child_subjects_template
#         return self._hierarchy_session.remove_children(id_=${arg0_name})"""


# class SubjectHierarchySession:
#     import_statements_pattern = [
#         'from dlkit.abstract_osid.osid import errors',
#         'from ..utilities import JSONClientValidated',
#     ]
#
#     get_root_subjects_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchySession.get_root_subjects_template
#         root_ids = self._hierarchy_session.get_roots()
#         collection = JSONClientValidated('${package_name_replace}',
#                                          collection='${object_name}',
#                                          runtime=self._runtime)
#         result = collection.find(
#             dict({'_id': {'$$in': [ObjectId(root_id.get_identifier()) for root_id in root_ids]}},
#                  **self._view_filter()))
#         return objects.${return_type}(
#             result,
#             runtime=self._runtime,
#             proxy=self._proxy)"""
#
#     get_child_subjects_template = """
#         # Implemented from template for
#         # osid.ontology.SubjectHierarchySession.get_child_subjects_template
#         if self._hierarchy_session.has_children(${arg0_name}):
#             child_ids = self._hierarchy_session.get_children(${arg0_name})
#             collection = JSONClientValidated('${package_name_replace}',
#                                              collection='${object_name}',
#                                              runtime=self._runtime)
#             result = collection.find(
#                 dict({'_id': {'$$in': [ObjectId(child_id.get_identifier()) for child_id in child_ids]}},
#                      **self._view_filter()))
#             return objects.${return_type}(
#                 result,
#                 runtime=self._runtime,
#                 proxy=self._proxy)
#         raise errors.IllegalState('no children')"""
