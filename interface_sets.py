
MARKERS = set(['OsidPrimitive',
               'Identifiable',
               'Extensible',
               'Browsable',
               'Suppliable',
               'Temporal',
               'Subjugateable',
               'Aggregateable',
               'Containable',
               'Sourceable',
               'Federateable',
               'Operable'])

MANAGERS = set(['OsidProfile',
                'OsidManager',
                'OsidProxyManager',
                'OsidRuntimeProfile',
                'OsidRuntimeManager'])

SESSIONS = set(['OsidSession'])

OBJECTS = set(['OsidObject',
               'OsidRelationship',
               'OsidCatalog',
               'OsidRule',
               'OsidEnabler',
               'OsidConstrainer',
               'OsidProcessor',
               'OsidGovernator',
               'OsidCapsule',
               'OsidForm',
               'OsidIdentifiableForm',
               'OsidExtensibleForm',
               'OsidBrowsableForm',
               'OsidTemporalForm',
               'OsidAggregateableForm',
               'OsidContainableForm',
               'OsidSourceableForm',
               'OsidFederateableForm',
               'OsidOperableForm',
               'OsidObjectForm',
               'OsidRelationshipForm',
               'OsidCatalogForm',
               'OsidRuleForm',
               'OsidEnablerForm',
               'OsidConstrainerForm',
               'OsidProcessorForm',
               'OsidGovernatorForm',
               'OsidCapsuleForm',
               'OsidList',
               'OsidNode',
               'CalendarInfo',
               'TimeInfo',
               'CalendarUnit',
               'Locale',
               'LocaleList',
               'Authentication',
               'Challenge',
               'DateTimeInterval',
               'DirectoryEntry',
               'DirectoryEntryForm',
               'Request',
               'DataInputStream',
               'DataOutputStream',
               'OsidCompendium'])

RECORDS = set(['OsidRecord'])

QUERIES = set(['OsidQuery',
               'OsidIdentifiableQuery',
               'OsidExtensibleQuery',
               'OsidBrowsableQuery',
               'OsidTemporalQuery',
               'OsidAggregateableQuery',
               'OsidContainableQuery',
               'OsidSourceableQuery',
               'OsidFederateableQuery',
               'OsidOperableQuery',
               'OsidObjectQuery',
               'OsidRelationshipQuery',
               'OsidCatalogQuery',
               'OsidRuleQuery',
               'OsidEnablerQuery',
               'OsidConstrainerQuery',
               'OsidProcessorQuery',
               'OsidGovernatorQuery',
               'OsidCapsuleQuery',
               'DirectoryEntryQuery'])

QUERY_INSPECTORS = set(['OsidQueryInspector',
                        'OsidIdentifiableQueryInspector',
                        'OsidExtensibleQueryInspector',
                        'OsidBrowsableQueryInspector',
                        'OsidTemporalQueryInspector',
                        'OsidAggregateableQueryInspector',
                        'OsidContainableQueryInspector',
                        'OsidSourceableQueryInspector',
                        'OsidFederateableQueryInspector',
                        'OsidOperableQueryInspector',
                        'OsidObjectQueryInspector',
                        'OsidRelationshipQueryInspector',
                        'OsidCatalogQueryInspector',
                        'OsidRuleQueryInspector',
                        'OsidEnablerQueryInspector',
                        'OsidConstrainerQueryInspector',
                        'OsidProcessorQueryInspector',
                        'OsidGovernatorQueryInspector',
                        'OsidCapsuleQueryInspector',
                        'DirectoryEntryQueryInspector'])

SEARCH_ORDERS = set(['OsidSearchOrder',
                     'OsidIdentifiableSearchOrder',
                     'OsidExtensibleSearchOrder',
                     'OsidBrowsableSearchOrder',
                     'OsidTemporalSearchOrder',
                     'OsidAggregateableSearchOrder',
                     'OsidContainableSearchOrder',
                     'OsidSourceableSearchOrder',
                     'OsidFederateableSearchOrder',
                     'OsidOperableSearchOrder',
                     'OsidObjectSearchOrder',
                     'OsidRelationshipSearchOrder',
                     'OsidCatalogSearchOrder',
                     'OsidRuleSearchOrder',
                     'OsidEnablerSearchOrder',
                     'OsidConstrainerSearchOrder',
                     'OsidProcessorSearchOrder',
                     'OsidGovernatorSearchOrder',
                     'OsidCapsuleSearchOrder',
                     'DirectoryEntrySearchOrder'])

SEARCHES = set(['OsidSearch',
               'OsidSearchResults'])
              
RULES = set(['OsidCondition',
            'OsidInput',
            'OsidResult'
            ##### NEEED MORE ????
            ##### SHOULD I CONSIDER RE-ORGANIZING EVERYTHING
            ##### AROUND OBJECTS, RULES, RELATIONSHIPS, ETC????
            ])
            
METADATA = set(['Metadata'])

RECEIVERS = set(['OsidReceiver'])

PRIMITIVES = set(['OsidPrimitives',
                  'DateTime'])

PROPERTIES = set(['Property',
                  'PropertyList'])

