
def make_all():

    print "Creating Package Maps..."
    from builders.mappers import map_all
    map_all('all')

    print "Identifying Implementation Patterns..."
    from builders.mappers import make_patterns
    make_patterns()

    print "Creating Python Interface Bindings..."
    from builders.abcbinder import make_abcosids
    make_abcosids()

    print "Creating MongoDB Implementations..."
    from builders.mdatabuilder import make_mdata
    make_mdata()

    from builders.mongobuilder import make_mongoosids
    make_mongoosids()

#    print "Building Django Service Implementations..."
#    from builders.djbuilder import make_djosids
#    make_djosids()
    
#    print "Building Django Models..."
#    from builders.djmodelbuilder import make_djmodels
#    make_djmodels()

    print "Building Authorization Adapters..."
    from builders.azbuilder import make_azosids
    make_azosids()

#    print "Building Simple Federaters..."
#    from builders.fedbuilder import make_fedosids
#    make_fedosids()

    print "Building DLkit Developer API Layers..."
    from builders.kitbuilder import make_kitosids
    make_kitosids()

    print "Building DLkit Developer Reference Documentation..."
    from builders.kitdocbuilder import make_kitdocs
    make_kitdocs()
    from builders.osiddocbuilder import make_osiddocs
    make_osiddocs()

    print "Building DLkit Sphinx Documentation Source..."
    from builders.kitdocsourcebuilder import make_kitdocs
    make_kitdocs()

    #from builders.djmodelbuilder import make_djmodels
    #make_djmodels()

    from builders.mapcount import count_all
    count_all()
