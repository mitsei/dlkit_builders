class SpatialUnit:

    init = """
    def __init__(self, center_coordinate = None,
                       bounding_coordinates = None):

        self._center_coordinate = center_coordinate
        self._bounding_coordinates = bounding_coordinates"""

    get_center_coordinate = """
        return self._center_coordinate"""

    get_bounding_coortinates = """
        return self._bounding_coordinates"""


class Coordinate:
    
    init = """
    def __init__(self, coordinate_type,
                       values,
                       uncertainty_minus = None,
                       uncertainty_plus = None):

        self._coordinate_type = coordinate_type
        self._values = values
        self._uncertainty_minus = uncertainty_minus
        self._uncertainty_plus = uncertainty_plus"""

    get_coordinate_type = """
        return self._coordinate_type"""

    get_dimensions = """
        return len(self._values)"""

    get_values = """
        return self._values"""

    defines_uncertainty = """
        return self._uncertainty_minus or self._uncertainty_plus"""

    get_uncertainty_minus = """
        return self._uncertainty_minus"""

    get_uncertainty_plus = """
        return self._uncertainty_plus"""
