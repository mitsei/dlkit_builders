COMMON_METADATA = """
            'element_id': Id(self._authority,
                             self._namespace,
                             '${data_name}'),
            'element_label': self.my_model.moptions['${data_name}']['verbose_name'],
            'instructions': DisplayText(self.my_model.moptions['${data_name}']['help_text']),
            'required': not self.my_model.moptions['${data_name}']['blank'],
            'read_only': not self.my_model.moptions['${data_name}']['editable'],
            'linked': self.my_model.moptions['${data_name}']['linked'],
            'syntax': self.my_model.moptions['${data_name}']['syntax'],
            'array': self.my_model.moptions['${data_name}']['array'],"""

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

COMMON_FIELD_OPTIONS = """
            'verbose_name': '${verbose_name}',
            'help_text': '${help_text}',
            'blank': True,
            'editable': True,"""

COMMON_OSID_OPTIONS = """
            'linked': False,
            'array': False,"""

BOOLEAN_FIELD_OPTIONS = """
            'default': False,"""

BOOLEAN_OSID_OPTIONS = """
            'syntax': 'BOOLEAN',"""

STRING_FIELD_OPTIONS = """
            'default': '',
            'max_length': ${max_length},
            'choices': OrderedDict(),"""

STRING_OSID_OPTIONS = """
            'syntax': 'STRING',
            'min_length': 0,
            'match_types': [],"""

ID_OSID_OPTIONS = """
            'syntax': 'ID',
            '${id_type}_set': [],"""

MODEL_FIELD_OPTIONS = """
        verbose_name=options['${data_name}']['verbose_name'],
        help_text=options['${data_name}']['help_text'],
        blank=options['${data_name}']['blank'],
        default=options['${data_name}']['default'],
        editable=options['${data_name}']['editable'],
        max_length=options['${data_name}']['max_length'],
        choices=options['${data_name}']['choices']
        """


