"""Utilities for manipulating lists of ids"""

def move_id_ahead(element_id, reference_id, idstr_list):
    """Moves element_id ahead of referece_id in the list"""
    if element_id == reference_id:
        return idstr_list
    idstr_list.remove(str(element_id))
    reference_index = idstr_list.index(str(reference_id))
    print reference_index
    idstr_list.insert(reference_index, str(element_id))
    return idstr_list

def move_id_behind(element_id, reference_id, idstr_list):
    """Moves element_id behind referece_id in the list"""
    if element_id == reference_id:
        return idstr_list
    idstr_list.remove(str(element_id))
    reference_index = idstr_list.index(str(reference_id))
    idstr_list.insert(reference_index + 1, str(element_id))
    return idstr_list
