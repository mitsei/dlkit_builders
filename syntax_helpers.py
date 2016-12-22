
SYNTAX_MAP = {
    'none': 'NONE',
    'boolean': 'BOOLEAN',
    'byte': 'BYTE',
    'cardinal': 'CARDINAL',
    'osid.mapping.Coordinate': 'COORDINATE',
    'osid.financials.Currency': 'CURRENCY',
    'osid.calendaring.DateTime': 'DATETIME',
    'decimal': 'DECIMAL',
    'osid.locale.DisplayText': 'DISPLAYTEXT',
    'osid.mapping.Distance': 'DISTANCE',
    'osid.calendaring.Duration': 'DURATION',
    'osid.mapping.Heading': 'HEADING',
    'osid.id.Id': 'ID',
    'integer': 'INTEGER',
    'osid.mapping.SpatialUnit': 'SPATIALUNIT',
    'osid.mapping.Speed': 'SPEED',
    'string': 'STRING',
    'osid.calendaring.Time': 'TIME',
    'osid.type.Type': 'TYPE',
    'osid.installation.Version': 'VERSION',
    }

def get_syntax_for_arg_type(arg_type):
    """returns the osid sytax string for a given argument type."""
    if arg_type in SYNTAX_MAP:
        return SYNTAX_MAP[arg_type]
    return 'OBJECT'

def syntax_to_under(syntax):
    """returns underscore string for given syntax string."""
    if syntax == 'DATETIME':
        return 'date_time'
    elif syntax == 'DISPLAYTEXT':
        return 'display_text'
    elif syntax == 'SPATIALUNIT':
        return 'spatial_unit'
    else:
        return syntax.lower()
