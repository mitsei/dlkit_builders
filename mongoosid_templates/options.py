METADATA_INITER = """
        self._${data_name}_metadata = {
        'element_id': Id(self._authority,
                         self._namespace,
                        '${data_name}')}
        self._${data_name}_metadata.update(mdata_conf.${data_name})"""
             
ID_METADATA ="""
            'value': (bool(self.my_model.options['${data_name}_authority']['default']) and
                      bool(self.my_model.options['${data_name}_namespace']['default']) and
                      bool(self.my_model.options['${data_name}_identifier']['default'])),
            'id_set': self.my_model.moptions['${data_name}']['id_set']"""

BOOLEAN_METADATA = """
            'value': self.my_model.moptions['${data_name}']['default'] != None"""

STRING_METADATA = """
            'value': bool(self.my_model.moptions['${data_name}']['default']),
            'minimum_string_length': self.my_model.moptions['${data_name}']['min_length'],
            'maximum_string_length': self.my_model.moptions['${data_name}']['max_length'],
            'string_set': self.my_model.moptions['${data_name}']['choices'],
            'string_match_types': self.my_model.moptions['${data_name}']['match_types']"""

COMMON_MDATA = """
    'element_label': '${element_label}',
    'instructions': '${instructions}',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': ${array},"""

BOOLEAN_MDATA = """
    'syntax': 'BOOLEAN',"""

STRING_MDATA = """
    'default_string_values': [''],
    'syntax': 'STRING',
    'minimum_string_length': 0,
    'maximum_string_length': ${max_length},
    'string_set': [],"""

DISPLAY_TEXT_MDATA = """
    'default_string_values': [{
        'text': '',
        'languageTypeId': str(default_language_type),
        'scriptTypeId': str(default_script_type),
        'formatTypeId': str(default_format_type),
        }],
    'syntax': 'STRING',
    'minimum_string_length': 0,
    'maximum_string_length': ${max_length},
    'string_set': [],"""

ID_MDATA = """
    'default_${id_type}_values': [''],
    'syntax': '${syntax}',
    '${id_type}_set': [],"""

ID_LIST_MDATA = """
    'default_${id_type}_values': [],
    'syntax': '${syntax}',
    '${id_type}_set': [],"""

TYPE_MDATA = """
    'default_${id_type}_values': [''],
    'syntax': '${syntax}',
    '${id_type}_set': [],"""

TYPE_LIST_MDATA = """
    'default_${id_type}_values': [],
    'syntax': '${syntax}',
    '${id_type}_set': [],"""

DATE_TIME_MDATA = """
    'default_date_time_values': [None],
    'syntax': 'DATETIME',
    'date_time_set': [],"""

DURATION_MDATA = """
    'default_duration_values': [None],
    'syntax': 'DURATION',
    'date_time_set': [],"""

OBJECT_MDATA = """
    'default_object_values': [''],
    'syntax': 'OBJECT',
    'object_types': [],
    'object_set': [],"""

#MODEL_FIELD_OPTIONS = """
#        verbose_name=options['${data_name}']['verbose_name'],
#        help_text=options['${data_name}']['help_text'],
#        blank=options['${data_name}']['blank'],
#        default=options['${data_name}']['default'],
#        editable=options['${data_name}']['editable'],
#        max_length=options['${data_name}']['max_length'],
#        choices=options['${data_name}']['choices']
#        """


