from abcbinder_settings import XOSIDNAMESPACEURI as ns
from binder_helpers import wrap_and_indent

def make_models(osidPackage, interfaceName, inheritList, methodList, 
                      packageRoot):
    # inheritList is a list of full interface names (like 'osid.type.Type').
    # inheritList[element].split('.')[-1] provides the interface name.
    # inheritList[element].split('.')[-2] provides the interface package name.
    # methodList is a dict which includes a 'methodName': a 'returnType':
    # and a 'paramList':. The 'methodName': is camelCase and the 'returnType':
    # is the full interface name of the return type..  The 'paramList': is a 
    # list that will at least include 'self' and any additional parameter
    # names.  paramList does not include information about parameter types.
    # Should it?.  packageRoot is the ElementTree root of the entire osid 
    # package to be used for braoder inspections.
    import os
    from binder_helpers import camel_to_list
    from binder_helpers import get_return_type
    from binder_helpers import get_param_list
    from binder_helpers import make_plural
    from osid_kit.osid_meta import OSID_Language_Primitives
    
    interfaceShortName = interfaceName.split('.')[-1]

    # First, deal with interfaces that directly inherit from OsidObject 
    # and write more do when I know what I'm doing
    if 'OsidObject' in inheritList and osidPackage != 'osid':
        import string
        commentStr = 'Variables yet to consider:\n'
        modelTableStr = ''  ###### All these variables want to be moved up???###
        instanceVarStr = ''
        foreignTablesStr = ''
        modelStr = ''
        implementedVars = []
        
        print '\n'
        print osidPackage, interfaceName
        ##
        # First, iterate though the corresponding Form interface to develop
        # a list of variable names for data that should be persisted.
        for child in packageRoot:
            if child.tag == (ns + 'interface'):
                interfaceToTest = child.get(ns + 'name').split('.')[-1]
                interfaceToTestList = camel_to_list(interfaceToTest)
                interfaceShortNameToTest = ''.join(interfaceToTestList[:-1])
                if (interfaceShortNameToTest == interfaceShortName and
                    'Form' in interfaceToTestList and
                    'Record' not in interfaceToTestList):
                    formMethodNameList = []
                    for grandChild in child:
                        if grandChild.tag == (ns + 'method'):
                            formMethodNameList.append(grandChild.get(ns + 'name'))
                    formVariables = []
                    for formMethodName in formMethodNameList:
                        var = camel_to_list(formMethodName)[1:]
                        var[0] = var[0].lower()
                        if ''.join(var) not in formVariables:
                            formVariables.append(''.join(var))
                    variables = []
                    variablesInfo = []
                    allVariables = []
                    allVariablesInfo = []
                    for method in methodList:
                        var = camel_to_list(method['methodName'])[1:]
                        var[0] = var[0].lower()
                        allVariables.append(''.join(var))
                        allVariablesInfo.append(dict(varName = ''.join(var),
                                           returnType = method['returnType']))
                        if ''.join(var) not in variables:
                            variables.append(''.join(var))
                            variablesInfo.append(dict(varName = ''.join(var),
                                               returnType = method['returnType']))
#                    print variables
#                    print formVariables
                    for v in variablesInfo:

                        ##
                        # First, look for variables that represent osid things
                        # that are stored by Ids
                        if ((v['varName'] in formVariables or
                            v['varName'] + 'Id' in formVariables) and
                            v['varName'] + 'Id' in variables and
                            v['varName'] not in implementedVars and
                            v['varName'] + 'Id' not in implementedVars):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + 'Authority = models.CharField(max_length=128)\n' +
    '    ' + v['varName'] + 'NameSpace = models.CharField(max_length=128)\n' +
    '    ' + v['varName'] + 'Identifier = models.CharField(max_length=64)\n')
                            implementedVars.append(v['varName'])
                            implementedVars.append(v['varName'] + 'Id')

                        ##
                        # Next, look for model variables that return boolean
                        # and don't represent fields that returns an object Id
                        elif (v['returnType'] == 'Id' and
                              v['varName'] + 'Id' in implementedVars):
                              implementedVars.append(v['varName'])

                        ##
                        # Next, look for model variables that return boolean
                        # and don't represent fields that returns an object Id
                        elif (v['varName'] in formVariables and
                              v['returnType'] == 'boolean' and
                              allVariables.count(v['varName']) == 1 and
                              v['varName'] not in implementedVars):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + ' = models.NullBooleanField(null = True)\n')
                            implementedVars.append(v['varName'])

                        ##
                        # Next, look for model variables that return boolean
                        # and may represent fields that returns an object Id
                        elif (v['varName'] in formVariables and
                              v['returnType'] == 'boolean' and
                              allVariables.count(v['varName']) > 1 and
                              v['varName'] not in implementedVars):
                            for a in allVariablesInfo:
                                if (a['returnType'] == 'osid.id.Id' and
                                    a['varName'] not in implementedVars):
                                    modelTableStr = (modelTableStr +
    '    ' + v['varName'] + 'Authority = models.CharField(max_length=128)\n' +
    '    ' + v['varName'] + 'NameSpace = models.CharField(max_length=128)\n' +
    '    ' + v['varName'] + 'Identifier = models.CharField(max_length=64)\n')
                            implementedVars.append(v['varName'])

                        ##
                        # Look for methods that return Time objects
                        elif (v['varName'] in formVariables and
                             v['returnType'] == 'osid.calendaring.Time'):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + ' = models.TimeField()\n')
                            implementedVars.append(v['varName'])

                        ##
                        # Look for methods that return DateTime objects
                        elif (v['varName'] in formVariables and
                             v['returnType'] == 'osid.calendaring.DateTime'):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + ' = models.DateTimeField()\n')
                            implementedVars.append(v['varName'])

                        ##
                        # Look for integers or cardinals
                        elif (v['varName'] in formVariables and
                             (v['returnType'] == 'integer' or
                              v['returnType'] == 'cardinal')):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + ' = models.IntegerField()\n')
                            implementedVars.append(v['varName'])

                        ##
                        # Look for decimals
                        elif (v['varName'] in formVariables and
                              v['returnType'] == 'decimal'):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + ' = models.DecimalField()\n')
                            implementedVars.append(v['varName'])

                        ##
                        # Look for strings 
                        elif (v['varName'] in formVariables and
                              v['returnType'] == 'string'):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + ' = models.CharField(max_length=256)\n')# WHAT SHOULD MAX LENGTH BE!!!!!!
                            implementedVars.append(v['varName'])

                        ##
                        # Look for things that return IdLists and make 
                        # foreign key tables while we're at it.
                        elif (make_plural(''.join(camel_to_list(v['varName'])[0:-1]))
                                           in formVariables and
                              v['returnType'] == 'osid.id.IdList'):
                            varName = camel_to_list(v['varName'])[0:-1]
                            varName[0] = varName[0].title()
                            foreignTablesStr = (foreignTablesStr +
    'class ' + interfaceName + '_' + ''.join(varName) + '(models.Model):\n' +
    '    ' + interfaceName.lower() + ' = models.ForeignKey(' + interfaceName + ')\n' +
    '    authority = models.CharField(max_length=128)\n' +
    '    nameSpace = models.CharField(max_length=128)\n' +
    '    identifier = models.CharField(max_length=64)\n\n')
                            print '    ', v['varName']
                            implementedVars.append(v['varName'])
                            implementedVars.append(''.join(camel_to_list(v['varName'])[0:-1]))
                            implementedVars.append(make_plural(''.join(camel_to_list(v['varName'])[0:-1])))

                        ##
                        # Look for those pesky somethingBasedSomethingelse
                        # boolean checks that may only occur in learning
                        # Activity objects
                        elif ('Based' + interfaceName in v['varName'] and
                              v['returnType'] == 'boolean'):
                            modelTableStr = (modelTableStr +
    '    ' + v['varName'] + ' = models.NullBooleanField(null = True)\n')
                            implementedVars.append(v['varName'])

                        ##
                        # There seem to be some methods that return IdLists
                        # that don't have setters in the corresponding
                        # Form objects. For the time-being we will make 
                        # foreign-key tables for them as well.
                        elif v['returnType'] == 'osid.id.IdList':
                            varName = camel_to_list(v['varName'])[0:-1]
                            varName[0] = varName[0].title()
                            foreignTablesStr = (foreignTablesStr +
    'class ' + interfaceName + '_' + ''.join(varName) + '(models.Model):\n' +
    '    ' + interfaceName.lower() + ' = models.ForeignKey(' + interfaceName + ')\n' +
    '    authority = models.CharField(max_length=128)\n' +
    '    nameSpace = models.CharField(max_length=128)\n' +
    '    identifier = models.CharField(max_length=64)\n\n')
                            implementedVars.append(v['varName'])
                            implementedVars.append(''.join(camel_to_list(v['varName'])[0:-1]))
                            implementedVars.append(make_plural(''.join(camel_to_list(v['varName'])[0:-1])))

                        ##
                        # Look for method variables that deal with DisplayText 
                        elif (v['varName'] in formVariables and
                              v['returnType'] == 'osid.locale.DisplayText'):
                            modelTableStr = (modelTableStr +         # HOW LONG FOR STRINGS
    '    ' + v['varName'] + ' = models.CharField(max_length=512)\n') # PERHAPS SETTINGS FOR LONG, MED, SHORT?
                            implementedVars.append(v['varName'])

                        ##
                        # Check for templates for customized modelTableStrs
                        # foreignTableStrs and instanceTableStrs. Some of 
                        # these may simply be empty strings for the sole 
                        # purpose of logging uncaught model implementations in
                        # the implementedVars list.
                        elif v['varName'] not in implementedVars:
                            if os.path.exists('dj_osid_templates/' + osidPackage + 
                                         '/model/model_tables/' + v['varName'] + '.txt'):
                                f = open('dj_osid_templates/' + osidPackage + 
                                         '/model/model_tables/' + v['varName'] + '.txt', 'r')
                                modelTableStr = modelTableStr + f.read()
                                f.close()
                                implementedVars.append(v['varName'])
                            if os.path.exists('dj_osid_templates/' + osidPackage + 
                                         '/model/foreign_tables/' + v['varName'] + '.txt'):
                                f = open('dj_osid_templates/' + osidPackage + 
                                         '/model/foreign_tables/' + v['varName'] + '.txt', 'r')
                                foreignTableStr = foreignTableStr + f.read()
                                f.close()
                                implementedVars.append(v['varName'])
                            if os.path.exists('dj_osid_templates/' + osidPackage + 
                                         '/model/instance_vars/' + v['varName'] + '.txt'):
                                f = open('dj_osid_templates/' + osidPackage + 
                                         '/model/instance_vars/' + v['varName'] + '.txt', 'r')
                                instanceVarStr = instanceVarStr + f.read()
                                f.close()
                                implementedVars.append(v['varName'])

                        print implementedVars
                    for v in variablesInfo:
                        if v['varName'] not in implementedVars:
                            commentStr = commentStr + v['varName'] + ', '
                    if commentStr:
                        commentStr = wrap_and_indent(commentStr.strip(), '    # ')
                    if modelTableStr or commentStr:
                        modelStr = (commentStr + '\n' + modelTableStr + '\n' + 
                                            instanceVarStr + '\n' + foreignTablesStr + '\n')
                    return modelStr

#                            print v['varName']
#                            print formVariables
#                            print variables

