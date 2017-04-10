from abcbinder_settings import XOSIDNAMESPACEURI as ns
from binder_helpers import wrap_and_indent


def make_models(osid_package, interface_name, inherit_list, method_list,
                package_root):
    # inherit_list is a list of full interface names (like 'osid.type.Type').
    # inherit_list[element].split('.')[-1] provides the interface name.
    # inherit_list[element].split('.')[-2] provides the interface package name.
    # method_list is a dict which includes a 'methodName': a 'returnType':
    # and a 'paramList':. The 'methodName': is camelCase and the 'returnType':
    # is the full interface name of the return type..  The 'paramList': is a
    # list that will at least include 'self' and any additional parameter
    # names.  paramList does not include information about parameter types.
    # Should it?.  package_root is the ElementTree root of the entire osid
    # package to be used for braoder inspections.
    import os
    from binder_helpers import camel_to_list
    from binder_helpers import get_return_type
    from binder_helpers import get_param_list
    from binder_helpers import make_plural
    from osid_kit.osid_meta import OSID_Language_Primitives

    interface_short_name = interface_name.split('.')[-1]

    # First, deal with interfaces that directly inherit from OsidObject
    # and write more do when I know what I'm doing
    if 'OsidObject' in inherit_list and osid_package != 'osid':
        import string
        comment_str = 'Variables yet to consider:\n'
        model_table_str = ''  # All these variables want to be moved up???###
        instance_var_str = ''
        foreign_tables_str = ''
        model_str = ''
        implemented_vars = []

        print '\n'
        print osid_package, interface_name
        ##
        # First, iterate though the corresponding Form interface to develop
        # a list of variable names for data that should be persisted.
        for child in package_root:
            if child.tag == (ns + 'interface'):
                interface_to_test = child.get(ns + 'name').split('.')[-1]
                interface_to_test_list = camel_to_list(interface_to_test)
                interface_short_name_to_test = ''.join(interface_to_test_list[:-1])
                if (interface_short_name_to_test == interface_short_name and
                        'Form' in interface_to_test_list and
                        'Record' not in interface_to_test_list):
                    form_method_name_list = []
                    for grand_child in child:
                        if grand_child.tag == (ns + 'method'):
                            form_method_name_list.append(grand_child.get(ns + 'name'))
                    form_variables = []
                    for form_method_name in form_method_name_list:
                        var = camel_to_list(form_method_name)[1:]
                        var[0] = var[0].lower()
                        if ''.join(var) not in form_variables:
                            form_variables.append(''.join(var))
                    variables = []
                    variables_info = []
                    all_variables = []
                    all_variables_info = []
                    for method in method_list:
                        var = camel_to_list(method['methodName'])[1:]
                        var[0] = var[0].lower()
                        all_variables.append(''.join(var))
                        all_variables_info.append(dict(varName=''.join(var),
                                                  returnType=method['returnType']))
                        if ''.join(var) not in variables:
                            variables.append(''.join(var))
                            variables_info.append(dict(varName=''.join(var),
                                                  returnType=method['returnType']))
#                    print variables
#                    print form_variables
                    for v in variables_info:

                        # First, look for variables that represent osid things
                        # that are stored by Ids
                        if ((v['varName'] in form_variables or
                             v['varName'] + 'Id' in form_variables) and
                                v['varName'] + 'Id' in variables and
                                v['varName'] not in implemented_vars and
                                v['varName'] + 'Id' not in implemented_vars):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + 'Authority = models.CharField(max_length=128)\n' +
                                '    ' + v['varName'] + 'NameSpace = models.CharField(max_length=128)\n' +
                                '    ' + v['varName'] + 'Identifier = models.CharField(max_length=64)\n')
                            implemented_vars.append(v['varName'])
                            implemented_vars.append(v['varName'] + 'Id')

                        # Next, look for model variables that return boolean
                        # and don't represent fields that returns an object Id
                        elif (v['returnType'] == 'Id' and
                                v['varName'] + 'Id' in implemented_vars):
                            implemented_vars.append(v['varName'])

                        # Next, look for model variables that return boolean
                        # and don't represent fields that returns an object Id
                        elif (v['varName'] in form_variables and
                              v['returnType'] == 'boolean' and
                              all_variables.count(v['varName']) == 1 and
                              v['varName'] not in implemented_vars):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + ' = models.NullBooleanField(null = True)\n')
                            implemented_vars.append(v['varName'])

                        # Next, look for model variables that return boolean
                        # and may represent fields that returns an object Id
                        elif (v['varName'] in form_variables and
                              v['returnType'] == 'boolean' and
                              all_variables.count(v['varName']) > 1 and
                              v['varName'] not in implemented_vars):
                            for a in all_variables_info:
                                if (a['returnType'] == 'osid.id.Id' and
                                        a['varName'] not in implemented_vars):
                                    model_table_str = (
                                        model_table_str +
                                        '    ' + v['varName'] + 'Authority = models.CharField(max_length=128)\n' +
                                        '    ' + v['varName'] + 'NameSpace = models.CharField(max_length=128)\n' +
                                        '    ' + v['varName'] + 'Identifier = models.CharField(max_length=64)\n')
                            implemented_vars.append(v['varName'])

                        # Look for methods that return Time objects
                        elif (v['varName'] in form_variables and
                              v['returnType'] == 'osid.calendaring.Time'):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + ' = models.TimeField()\n')
                            implemented_vars.append(v['varName'])

                        # Look for methods that return DateTime objects
                        elif (v['varName'] in form_variables and
                              v['returnType'] == 'osid.calendaring.DateTime'):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + ' = models.DateTimeField()\n')
                            implemented_vars.append(v['varName'])

                        # Look for integers or cardinals
                        elif (v['varName'] in form_variables and
                              (v['returnType'] == 'integer' or
                               v['returnType'] == 'cardinal')):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + ' = models.IntegerField()\n')
                            implemented_vars.append(v['varName'])

                        # Look for decimals
                        elif (v['varName'] in form_variables and
                              v['returnType'] == 'decimal'):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + ' = models.DecimalField()\n')
                            implemented_vars.append(v['varName'])

                        # Look for strings
                        elif (v['varName'] in form_variables and
                              v['returnType'] == 'string'):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + ' = models.CharField(max_length=256)\n')  # WHAT SHOULD MAX LENGTH BE!!!!!!
                            implemented_vars.append(v['varName'])

                        # Look for things that return IdLists and make
                        # foreign key tables while we're at it.
                        elif (make_plural(''.join(camel_to_list(v['varName'])[0:-1]))
                                in form_variables and
                                v['returnType'] == 'osid.id.IdList'):
                            var_name = camel_to_list(v['varName'])[0:-1]
                            var_name[0] = var_name[0].title()
                            foreign_tables_str = (
                                foreign_tables_str +
                                'class ' + interface_name + '_' + ''.join(var_name) + '(models.Model):\n' +
                                '    ' + interface_name.lower() + ' = models.ForeignKey(' + interface_name + ')\n' +
                                '    authority = models.CharField(max_length=128)\n' +
                                '    nameSpace = models.CharField(max_length=128)\n' +
                                '    identifier = models.CharField(max_length=64)\n\n')
                            print('    {0}'.format(v['varName']))
                            implemented_vars.append(v['varName'])
                            implemented_vars.append(''.join(camel_to_list(v['varName'])[0:-1]))
                            implemented_vars.append(make_plural(''.join(camel_to_list(v['varName'])[0:-1])))

                        # Look for those pesky somethingBasedSomethingelse
                        # boolean checks that may only occur in learning
                        # Activity objects
                        elif ('Based' + interface_name in v['varName'] and
                              v['returnType'] == 'boolean'):
                            model_table_str = (
                                model_table_str +
                                '    ' + v['varName'] + ' = models.NullBooleanField(null = True)\n')
                            implemented_vars.append(v['varName'])

                        # There seem to be some methods that return IdLists
                        # that don't have setters in the corresponding
                        # Form objects. For the time-being we will make
                        # foreign-key tables for them as well.
                        elif v['returnType'] == 'osid.id.IdList':
                            var_name = camel_to_list(v['varName'])[0:-1]
                            var_name[0] = var_name[0].title()
                            foreign_tables_str = (
                                foreign_tables_str +
                                'class ' + interface_name + '_' + ''.join(var_name) + '(models.Model):\n' +
                                '    ' + interface_name.lower() + ' = models.ForeignKey(' + interface_name + ')\n' +
                                '    authority = models.CharField(max_length=128)\n' +
                                '    nameSpace = models.CharField(max_length=128)\n' +
                                '    identifier = models.CharField(max_length=64)\n\n')
                            implemented_vars.append(v['varName'])
                            implemented_vars.append(''.join(camel_to_list(v['varName'])[0:-1]))
                            implemented_vars.append(make_plural(''.join(camel_to_list(v['varName'])[0:-1])))

                        # Look for method variables that deal with DisplayText
                        elif (v['varName'] in form_variables and
                              v['returnType'] == 'osid.locale.DisplayText'):
                            model_table_str = (
                                model_table_str +         # HOW LONG FOR STRINGS
                                '    ' + v['varName'] + ' = models.CharField(max_length=512)\n')  # PERHAPS SETTINGS FOR LONG, MED, SHORT?
                            implemented_vars.append(v['varName'])

                        # Check for templates for customized model_table_strs
                        # foreign_table_strs and instanceTableStrs. Some of
                        # these may simply be empty strings for the sole
                        # purpose of logging uncaught model implementations in
                        # the implemented_vars list.
                        elif v['varName'] not in implemented_vars:
                            if os.path.exists('dj_osid_templates/' + osid_package +
                                              '/model/model_tables/' + v['varName'] + '.txt'):
                                f = open('dj_osid_templates/' + osid_package +
                                         '/model/model_tables/' + v['varName'] + '.txt', 'r')
                                model_table_str += f.read()
                                f.close()
                                implemented_vars.append(v['varName'])
                            if os.path.exists('dj_osid_templates/' + osid_package +
                                              '/model/foreign_tables/' + v['varName'] + '.txt'):
                                f = open('dj_osid_templates/' + osid_package +
                                         '/model/foreign_tables/' + v['varName'] + '.txt', 'r')
                                foreign_tables_str += f.read()
                                f.close()
                                implemented_vars.append(v['varName'])
                            if os.path.exists('dj_osid_templates/' + osid_package +
                                              '/model/instance_vars/' + v['varName'] + '.txt'):
                                f = open('dj_osid_templates/' + osid_package +
                                         '/model/instance_vars/' + v['varName'] + '.txt', 'r')
                                instance_var_str += f.read()
                                f.close()
                                implemented_vars.append(v['varName'])

                        print(implemented_vars)
                    for v in variables_info:
                        if v['varName'] not in implemented_vars:
                            comment_str = comment_str + v['varName'] + ', '
                    if comment_str:
                        comment_str = wrap_and_indent(comment_str.strip(), '    # ')
                    if model_table_str or comment_str:
                        model_str = (comment_str + '\n' + model_table_str + '\n' +
                                     instance_var_str + '\n' + foreign_tables_str + '\n')
                    return model_str

#                            print v['varName']
#                            print form_variables
#                            print variables
