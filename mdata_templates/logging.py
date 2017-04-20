class Logging:
    import_statements = [
        'import datetime'
    ]

    init = """
MIN_DATETIME = {
    'year': datetime.datetime.min.year,
    'month': datetime.datetime.min.month,
    'day': datetime.datetime.min.day,
    'hour': datetime.datetime.min.hour,
    'minute': datetime.datetime.min.minute,
    'second': datetime.datetime.min.second,
    'microsecond': datetime.datetime.min.microsecond,
}"""

    LOG_ENTRY_TIMESTAMP = """
            'element_label': 'timestamp',
            'instructions': 'enter a valid datetime object.',
            'required': False,
            'read_only': False,
            'linked': False,
            'array': False,
            'default_date_time_values': [MIN_DATETIME],
            'syntax': 'DATETIME',
            'date_time_set': []"""
