
from abcbinder_settings import XOSIDNAMESPACEURI as ns
from abcbinder_settings import XOSIDDIRECTORY as xosidDir
from abcbinder_settings import XOSIDFILESUFFIX as xosidSuffix
from abcbinder_settings import ABCPREFIX as abcPrefix
from abcbinder_settings import ABCROOTPACKAGE as abcPkgName
from abcbinder_settings import FIRSTDOCINDENTSTR as indentStr
from djbuilder_settings import ENCODING as utfStr
from djbuilder_settings import APPNAMEPREFIX as appPrefix
from djbuilder_settings import APPNAMESUFFIX as appSuffix
from djbuilder_settings import PACKAGEPREFIX as prefix
from djbuilder_settings import PACKAGESUFFIX as suffix
from djbuilder_settings import SUBPACKAGEPREFIX as subPrefix
from djbuilder_settings import SUBPACKAGESUFFIX as subSuffix
pkgScheme = 'verbose'

def make_djosids(makeModels=False):
    import time
    import os
    global _totalMethodCount
    global _implementedMethodCount
    global _totalInterfaceCount
    global _implementedInterfaceCount
    global _packageInterfaceCount
    global _packageImplementedInterfaceCount
    global _packageImplementedMethodCount
    global _packageMethodCount
    
    # Iterate over each xosid.xml package in the xosid directory:
    startTime = time.time()
    packageCount = 0
    _totalMethodCount = 0
    _implementedMethodCount = 0
    _totalInterfaceCount = 0
    _implementedInterfaceCount = 0
    
    for xosidFile in os.listdir(xosidDir):
        packageCount += 1
        if xosidFile.endswith(xosidSuffix):
            make_djosid(xosidDir + '/' + xosidFile, makeModels)
            _totalMethodCount = _totalMethodCount + _packageMethodCount
            _implementedMethodCount = _implementedMethodCount + _packageImplementedMethodCount
            _totalInterfaceCount = _totalInterfaceCount + _packageInterfaceCount
            _implementedInterfaceCount = _packageImplementedInterfaceCount
            
    # When done, report out implementation statistics:
    print (str(packageCount) + ' osid packages built in ' + 
                          str(time.time() - startTime) + ' seconds.\n' +
           str(_implementedMethodCount) + ' of ' + 
           str(_totalMethodCount) + ' methods (' + 
           "{0:.0f}%".format(float(_implementedMethodCount) /
                                  ( _totalMethodCount) * 100) + 
           ') implemented in ' +
           str(_implementedInterfaceCount) + ' of ' +
           str(_totalInterfaceCount) + ' interfaces.')
            
def make_djosid(fileName, makeModels=False, makePackage = True):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    import os
    from django.core import management
    from binder_helpers import wrap_and_indent
    global _packageInterfaceCount
    global _packageImplementedInterfaceCount
    global _packageImplementedMethodCount
    global _packageMethodCount    
    _packageMethodCount = 0
    _packageImplementedMethodCount = 0
    _packageInterfaceCount = 0
    _packageImplementedInterfaceCount = 0
    
    tree = ET.parse(fileName)
    root = tree.getroot()
    bodyStr = ''
    modelImportStr = 'from django.db import models\nimport osid_kit.models\n\n'
    thisModel = ''
    modelStr = ''
    modules = dict(objects = '', sessions = '', managers = '', 
                   primitives = '', records = '', other_please_move = '')
    for elem in root.iter(ns + 'osid'):
        ##
        # Get version and package name information from XML header and 
        # import osid package in all non-osid modules
        packageName = (elem.get(ns + 'name')).split('.')[-1]
        versionStr = wrap_and_indent((elem.get(ns + 'name')) +
                             ' ' + (elem.get(ns + 'version')), 
                             iIndent = indentStr) + '\n'
        importStr = ('import abc\nfrom ' + abcPkgName + ' import ' + 
                      abcPrefix + packageName + '\n')
        if packageName != 'osid':
            importStr = (importStr + 'from ' + appName('osid') + 
                                    ' import ' + pkgName('osid') + '\n')
        importStr = importStr + '\n\n'

    ##
    # Send the tree root through the three main documentation iterators
    # to build the basic package documentation strings.
    headStr = head_iterator(root, packageName, versionStr)
    licenseStr = license_iterator(root, packageName, versionStr)
    summaryString = summary_iterator(root, packageName, versionStr)

    ##
    # Check if there is already a Django app with this toolkit name.  If not,
    # invoke the Django manager startapp function to create one.
    if not os.path.exists(appName(packageName)):
        management.call_command('startapp', appName(packageName))

    ##
    # The real work starts here.  Iterate through all child elements in the 
    # tree root and invoke the interface_iterator to build all interfaces 
    # of this osid package.  The package strings are sorted into thier 
    # appropriate package modules.
    for child in root:
        if child.tag == (ns + 'interface'):
            interface = interface_iterator(child, packageName, root)
            moduleName = interface['moduleName']
            interfaceStr = interface['interfaceBody']
            modules[moduleName] = modules[moduleName] + interfaceStr
            if makeModels:
                modelStr = modelStr + model_iterator(child, packageName, root)

    ##
    # Save the model string to the models.py file in the appropriate Django app
    # making sure not to overwrite the osid_kit and type_kit models while we
    # are still trying to figure things out.    
    if packageName != 'osid' and packageName != 'type' and makeModels:
        print 'writing', appName(packageName), 'Django models'
        writeFile = open(appName(packageName) + '/models.py', 'w')
        writeFile.write((modelImportStr + modelStr).encode('utf-8'))
        writeFile.close

    ##
    # Finally create the modules for this osid package.  If older ones exist
    # this will overwrite them.
    print 'writing', appName(packageName), 'packages'
    if not os.path.exists(appName(packageName) + '/' + pkgName(packageName)):
        os.makedirs(appName(packageName) + '/' + pkgName(packageName))
        os.system('touch ' + appName(packageName) + '/' + 
                  pkgName(packageName) + '/__init__.py')
    
    for moduleName in modules:
        print moduleName
        writeFile = open(appName(packageName) + '/' + pkgName(packageName) +
                         '/' + moduleName + '.py', 'w')
        writeFile.write((headStr + importStr + modules[moduleName]).encode('utf-8'))
        writeFile.close

def head_iterator(root, packageName, versionStr):
    from binder_helpers import wrap_and_indent
    headStr = utfStr + '#\n#'
    ##
    # Iterate through the element tree searching for the 'title'.  That's all.
    # This used to do more, but now it only does this :(
    for child in root:
        if child.tag == (ns + 'title'):
            titleStr = (wrap_and_indent(child.text, indentStr)
                        + '\n' + indentStr + '\n' + indentStr + '\n')
    return versionStr + titleStr

def license_iterator(root, packageName, versionStr):
    from binder_helpers import wrap_and_indent
    headStr = utfStr + '#\n#'
    ##
    # Iterate through the element tree searching for the 'title', 'copyright'
    # and 'license' tags.  Returns the entire header string, including
    # the version string which is passed in.
    for child in root:
        if child.tag == (ns + 'title'):
            titleStr = (wrap_and_indent(child.text, indentStr)
                        + '\n' + indentStr + '\n' + indentStr + '\n')
        if child.tag == (ns + 'copyright'):
            legalStr = (process_text(child) + '\n'
                                 + indentStr + '\n' + indentStr + '\n')
        if child.tag == (ns + 'license'):
            legalStr = legalStr + process_text(child) +'\n\n\n'
    return headStr + versionStr + titleStr + legalStr

def summary_iterator(root, packageName, versionStr):
    from binder_helpers import wrap_and_indent
    headStr = utfStr + '#\n#'
    ##
    # Iterate through the element tree searching for the 'title', and
    # 'description' tags.  Returns the a string containing the summary,
    # documentation, including the version string which is passed in.
    for child in root:
        if child.tag == (ns + 'title'):
            titleStr = (wrap_and_indent(child.text, indentStr)
                        + '\n' + indentStr + '\n' + indentStr + '\n')
        if child.tag == (ns + 'description'):
            infoStr = (process_text(child) +'\n\n\n')
    return headStr + versionStr + titleStr + infoStr


def interface_iterator(root, packageName, packageRoot, makePackage = False):
    global _packageInterfaceCount
    global _packageImplementedInterfaceCount
    from djinitmaker import make_init_methods
    from djmodelmaker import make_models
    from binder_helpers import get_return_type
    from binder_helpers import get_param_list
    interfaceStr = root.get(ns + 'name').split('.')[-1]
    inheritStr = append_impl_str(abcPrefix + packageName 
                                + '.' + interfaceStr, '')
    inheritList = []
    docStr = '##\n'
    methodStr = ''
    methodList = []
    initMethods = ''
    for child in root:
        if child.tag == (ns + 'implements'):
            implName = child.get(ns + 'interface').split('.')[-1]
            if implName:
                inheritList.append(implName)
                implPkg = child.get(ns + 'interface').split('.')[-2]
                if packageName != implPkg:
                    implName = pkgName(implPkg) + '.' + implName
                inheritStr = append_impl_str(implName, inheritStr)
        if child.tag == (ns + 'description'):
            docStr = docStr + process_text(child)
        if child.tag == (ns + 'method'):
            methodList.append(dict(methodName = child.get(ns + 'name'), 
                                   returnType = get_return_type(child),
                                   paramList = get_param_list(child)))
            methodStr = methodStr + method_iterator(child, packageName, 
                                    interfaceStr, inheritList, root,
                                    packageRoot) + '\n\n'
    if inheritStr:
        inheritStr = '(' + inheritStr + ')'
    classStr = 'class ' + interfaceStr + inheritStr + ':'
    initMethods = make_init_methods(packageName, interfaceStr, 
                                    inheritList, methodList, packageRoot)
    if initMethods:
        initMethods = initMethods + '\n'
    if not methodStr:
        methodStr = '    pass\n\n'
        _packageImplementedInterfaceCount += 1
    _packageInterfaceCount += 1

    return dict(interfaceBody = (docStr + '\n\n' + classStr + '\n\n' + 
                initMethods + methodStr + '\n'), 
                moduleName = spiType(inheritList, interfaceStr))

def model_iterator(root, packageName, packageRoot):
    from djmodelmaker import make_models
    from binder_helpers import get_return_type
    from binder_helpers import get_param_list
    interfaceStr = root.get(ns + 'name').split('.')[-1]
    inheritStr = ''
    inheritList = []
    methodList = []
    for child in root:
        if child.tag == (ns + 'implements'):
            implName = child.get(ns + 'interface').split('.')[-1]
            if implName:
                inheritList.append(implName)
                implPkg = child.get(ns + 'interface').split('.')[-2]
                if packageName != implPkg:
                    implName = appName(implPkg) + '.models.' + implName
                inheritStr = append_impl_str(implName, inheritStr)
        if child.tag == (ns + 'method'):
            methodList.append(dict(methodName = child.get(ns + 'name'), 
                                   returnType = get_return_type(child),
                                   paramList = get_param_list(child)))
    inheritStr = append_impl_str('models.Model', inheritStr)
    if inheritStr:
        inheritStr = '(' + inheritStr + ')'
    classStr = 'class ' + interfaceStr + inheritStr + ':'
    modelStr = make_models(packageName, interfaceStr, 
                                    inheritList, methodList, packageRoot)
    if modelStr:
        return (classStr + '\n' + modelStr + '\n')
    else:
        return ''

def method_iterator(root, packageName, interfaceName, inheritList, interfaceRoot, packageRoot):
    from djimplmaker import make_method_impl
    from binder_helpers import fix_reserved_word
    from binder_helpers import get_return_type
    from binder_helpers import camel_to_under
    global _packageImplementedMethodCount
    global _packageMethodCount
    methodName = root.get(ns + 'name')
    defStr = '    def ' + camel_to_under(methodName)
    implStr = ''
    docStr = '    ##\n'
    paramStr = '(self'
    paramList = ['self']
    errorList = []
    returnStr = '        pass'
    returnType = get_return_type(root)
    for child in root:
        if child.tag == (ns + 'description'):
            docStr = docStr + process_text(child, '    # ') + '\n    #\n'
        if child.tag == (ns + 'parameter'):
            param = child.get(ns + 'name')
            param = fix_reserved_word(param)
            paramList.append(param)
            paramStr = paramStr + ', ' + param
            docStr = append_method_param_doc_str(child, docStr)
        if child.tag == (ns + 'return'):
            docStr = append_method_return_doc_str(child, docStr)
            returnStr = '        return'
        if child.tag == (ns + 'error'):
            errorList.append(child.get(ns + 'type'))
            docStr = append_method_error_doc_str(child, docStr)
        if child.tag == (ns + 'compliance'):
            docStr = append_method_compliance_doc_str(child, docStr)
        if child.tag == (ns + 'implNotes'):
            docStr = append_method_implnotes_doc_str(child, docStr)
    implStr = make_method_impl(packageName, interfaceName, 
                               inheritList, methodName, paramList, 
                               returnType, errorList, interfaceRoot,
                               packageRoot)
    if not implStr:
        implStr = returnStr
    else:
        _packageImplementedMethodCount += 1
    _packageMethodCount += 1
    defStr = defStr + paramStr + '):'
    return docStr + '\n' + defStr + '\n' + implStr

##
# This function iterates through the method tree and appends the docs
# regarding method parameters to the documentation string
def append_method_param_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    paramStr = 'arg:    ' + root.get(ns + 'name')
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            paramStr = paramStr + ' (' + child.get(ns + 'type') + '): '
        if child.tag == (ns + 'primitiveType'):
            paramStr = paramStr + ' (' + child.get(ns + 'type') + '): '
        if child.tag == (ns + 'description'):
            paramStr = paramStr + process_text(child, '', '')
    return docStr + wrap_and_indent(paramStr.strip(),
                                    '    # ',
                                    '    #         ') + '\n'

##
# This function iterates through the method tree and appends the docs
# regarding the method return type to the documentation string
def append_method_return_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    returnStr = 'return: '
    for child in root:
        if child.tag == (ns + 'interfaceType'):
            returnStr = returnStr + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'primitiveType'):
            returnStr = returnStr + '(' + child.get(ns + 'type') + ') - '
        if child.tag == (ns + 'description'):
            returnStr = returnStr + process_text(child, '', '')
            return docStr + wrap_and_indent(returnStr.strip(),
                                            '    # ',
                                            '    #         ') + '\n'

##
# This function iterates through the method tree and appends the docs
# regarding the possible exceptions raised by this method.
def append_method_error_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    errorStr = 'raise:  ' + root.get(ns + 'type') + ' - '
    for child in root:
        if child.tag == (ns + 'description'):
            errorStr = errorStr + process_text(child, '', '')
    return docStr + wrap_and_indent(errorStr.strip(),
                                    '    # ',
                                    '    #         ') + '\n'

##
# This function iterates through the method tree and appends the docs
# regarding the comliance required for this method.
def append_method_compliance_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    compStr = 'compliance: ' + root.get(ns + 'type') + ' - '
    for child in root:
        if child.tag == (ns + 'description'):
            compStr = compStr + process_text(child, '', '')
    return docStr + wrap_and_indent(compStr.strip(),
                                    '    # ',
                                    '    #             ') + '\n'

##
# This function iterates through the method tree and appends the docs
# pertaining to implementation notes for this method.
def append_method_implnotes_doc_str(root, docStr):
    from binder_helpers import wrap_and_indent
    noteStr = 'implementation notes: '
    noteStr = noteStr + process_text(root, '', '')
    return docStr + wrap_and_indent(noteStr.strip(),
                                    '    # ',
                                    '    # ') + '\n'
##
# Send any text blocks to this function that includes text tags for things
# like copyright symbols, paragraphs breaks, headings, tokens and code blocks
# and outlines.  Outlines are dispatched to make_outline which isn't afraid 
# to deal with them (but it should be).
def process_text(root, iIndent = '# ', sIndent = None):
    from binder_helpers import wrap_and_indent
    from binder_helpers import reindent
    from binder_helpers import camel_to_under
    
    if not sIndent:
        sIndent = iIndent
    makeStr = ''
    iterStr = ' '.join(root.text.split())
    for child in root:
        if child.tag == (ns + 'copyrightSymbol'):
            iterStr = iterStr + ' (c) ' + ' '.join(child.tail.split()) + ' '
        if child.tag == (ns + 'pbreak'):
            makeStr = (makeStr + wrap_and_indent(iterStr, 
                                    iIndent, sIndent)) + '\n' + iIndent +'\n'
            iterStr = ' '.join(child.tail.split())
        if child.tag == (ns + 'heading'):
            iterStr = iterStr + ' '.join(str(child.text).split())
            iterStr = iterStr + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'token'):
            if '()' in str(child.text):
                convertedText = camel_to_under(child.text)
            else:
                convertedText = child.text
            iterStr = iterStr + ' ' + ' '.join(str(convertedText).split()) + ' '
            iterStr = iterStr + '' + ' '.join(str(child.tail).split()) + ''
        if child.tag == (ns + 'code'):
            makeStr = (makeStr + wrap_and_indent(iterStr,
                                        iIndent, sIndent)).strip() + '\n'
            iterStr = reindent(child.text.strip(), iIndent + '  ')
            makeStr = makeStr + iterStr + iIndent + '\n'
            iterStr = ' '.join(child.tail.split())
        if child.tag == (ns + 'outline'):
            makeStr = (makeStr + wrap_and_indent(iterStr, 
                                        iIndent, sIndent)).strip() + '\n'
            iterStr = make_outline(child, iIndent + '  * ',
                                         iIndent + '    ')
            makeStr = makeStr + iterStr.strip()
            iterStr = ' '.join(child.tail.split())
    return makeStr + wrap_and_indent(iterStr, iIndent, sIndent)

##
# This function is used to properly process outline tagged text
def make_outline(root, iIndent, sIndent = None):
    from binder_helpers import wrap_and_indent
    if not sIndent:
        sIndent = iIndent
    outlineStr = ''
    iterStr = ''
    for child in root:
        if child.tag == (ns + 'element'):
            iterStr = ' '.join(child.text.split())
            for elem in child.iter():
                if elem.tag == (ns + 'token'):
                    iterStr = iterStr + ' ' + ' '.join(str(elem.text).split()) + ' '
                    iterStr = iterStr + '' + ' '.join(str(elem.tail).split()) + ''
            iterStr = wrap_and_indent(iterStr, iIndent, sIndent)
            outlineStr = outlineStr + iterStr + '\n'
    return outlineStr

##
# This little function simply appends the class inheritance string (implStr) 
# with each of the osid classes (impl's) sent to it by the method iterator
def append_impl_str(impl, implStr):
    if implStr:
        implStr = implStr + ', ' + impl
    else:
        implStr = implStr + impl
    return implStr

##
# The following functions return the app name and package name strings
# by prepending and appending the appropriate suffixes and prefixes.
def appName(string):
    return appPrefix + string + appSuffix
    
def pkgName(string):
    return prefix + string + suffix

def subPkgName(string):
    return subPrefix + string + subSuffix

##
# This function returns a string the represents the type of osid interface,
# like object, session, primitive, for creating a package sructure.  If the
# global flag pkgScheme is set to 'verbose', then this function will simply 
# return the camelToUnderscore name of the interface, resulting in every
# interface living in its own sub-package
def spiType(inheritList, interfaceStr):
    from binder_helpers import camel_to_list
    if ('OsidObject' in inheritList or 
        'OsidObjectQuery' in inheritList or 
        'OsidObjectQueryInspector' in inheritList or 
        'OsidForm' in inheritList or 
        'OsidObjectForm' in inheritList or 
        'OsidObjectSearchOrder' in inheritList or 
        'OsidSearch' in inheritList or 
        'OsidSearchResults' in inheritList or 
        'OsidReceiver' in inheritList or 
        'OsidList' in inheritList or 
        'OsidNode' in inheritList or 
        'OsidRelationship' in inheritList or
        'OsidRelationshipQuery' in inheritList or 
        'OsidRelationshipQueryInspector' in inheritList or
        'OsidRelationshipForm' in inheritList or 
        'OsidRelationshipSearchOrder' in inheritList or
        'OsidCatalog' in inheritList or 
        'OsidCatalogQuery' in inheritList or
        'OsidCatalogQueryInspector' in inheritList or 
        'OsidCatalogForm' in inheritList or
        'OsidCatalogSearchOrder' in inheritList):
        return 'objects'
    elif ('OsidSession' in inheritList or
          camel_to_list(interfaceStr)[-1] == 'Session'):
        return 'sessions'
    elif ('OsidProfile' in inheritList or 
          'OsidManager' in inheritList or 
          'OsidProxyManager' in inheritList):
        return 'managers'
    elif ('OsidPrimitive' in inheritList):
        return 'primitives'
    elif ('OsidRecord' in inheritList):
        return 'records'
    else:
        return 'other_please_move'

