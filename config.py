
packages_to_implement = [
    'assessment',
    'authentication.process',
    'authorization',
    'commenting',
    'grading',
    'hierarchy',
    'id',
    'learning',
    'locale',
    'mapping',
    'ontology',
    'osid',
    'proxy',
    'relationship',
    'repository',
    'resource',
    'type',
]

packages_to_test = [
    'assessment',
    'authorization',
    'commenting',
    'grading',
    'learning',
    'repository',
    'resource',
]

managers_to_implement = [
    'assessment',
    'authorization',
    'commenting',
    'grading',
    'hierarchy',
    'learning',
    'osid',
    'proxy',
    'relationship',
    'repository',
    'resource',
    'type',
]

sessions_to_implement = [
    ### assessment service:
    'AssessmentSession',
    'ItemLookupSession',
    'ItemQuerySession',
    'ItemSearchSession',
    'ItemAdminSession',
    'ItemNotificationSession',
    'ItemBankSession',
    'ItemBankAssignmentSession',
    'AssessmentLookupSession',
    'AssessmentQuerySession',
    'AssessmentAdminSession',
    'AssessmentBankSession',
    'AssessmentBankAssignmentSession',
    'AssessmentBasicAuthoringSession',
    'AssessmentOfferedLookupSession',
    'AssessmentOfferedQuerySession',
    'AssessmentOfferedAdminSession',
    'AssessmentOfferedBankSession',
    'AssessmentOfferedBankAssignmentSession',
    'AssessmentTakenLookupSession',
    'AssessmentTakenQuerySession',
    'AssessmentTakenAdminSession',
    'AssessmentTakenBankSession',
    'AssessmentTakenBankAssignmentSession',
    'BankLookupSession',
    'BankQuerySession',
    'BankAdminSession',
    'BankHierarchySession',
    'BankHierarchyDesignSession',
    ### authorization service:
    'AuthorizationSession',
    'AuthorizationLookupSession',
    'AuthorizationAdminSession',
    'VaultLookupSession',
    'VaultAdminSession',
    ### commenting service:
    'CommentLookupSession',
    'CommentQuerySession',
    'CommentAdminSession',
    'BookLookupSession',
    'BookAdminSession',
    'BookHierarchySession',
    'BookHierarchyDesignSession',
    ### grading service:
    'GradebookLookupSession',
    'GradebookAdminSession',
    'GradeSystemLookupSession',
    'GradeSystemAdminSession',
    'GradeSystemQuerySession',
    'GradeEntryLookupSession',
    'GradeEntryAdminSession',
    'GradeEntryQuerySession',
    'GradebookColumnLookupSession',
    'GradebookColumnAdminSession',
    'GradebookColumnQuerySession',
    'GradebookColumnCalculationLookupSession',
    'GradebookColumnCalculationAdminSession',
    ### hierarchy service:
    'HierarchyLookupSession',
    'HierarchyAdminSession',
    'HierarchyTraversalSession',
    'HierarchyDesignSession',
    ### learning service:
    'ObjectiveLookupSession',
    'ObjectiveQuerySession',
    'ObjectiveAdminSession',
    'ObjectiveObjectiveBankSession',
    'ObjectiveObjectiveBankAssignmentSession',
    'ObjectiveHierarchySession',
    'ObjectiveHierarchyDesignSession',
    'ObjectiveSequencingSession',
    'ObjectiveRequisiteSession',
    'ObjectiveRequisiteAssignmentSession',
    'ActivityLookupSession',
    'ActivityAdminSession',
    'ActivityObjectiveBankSession',
    'ActivityObjectiveBankAssignmentSession',
    'ObjectiveBankLookupSession',
    'ObjectiveBankAdminSession',
    'ObjectiveBankHierarchySession',
    'ObjectiveBankHierarchyDesignSession',
    'ProficiencyLookupSession',
    'ProficiencyAdminSession',
    'ProficiencyQuerySession',
    ## ontology service:
    'SubjectHierarchyDesignSession',
    ### proxy service
    'ProxySession',
    ### relationship service
    'RelationshipLookupSession',
    'RelationshipQuerySession',
    'RelationshipAdminSession',
    'FamilyLookupSession',
    'FamilyAdminSession',
    'FamilyHierarchySession',
    'FamilyHierarchyDesignSession',
    ### repository service
    'AssetLookupSession',
    'AssetQuerySession',
    'AssetSearchSession',
    'AssetAdminSession',
    'AssetNotificationSession',
    'AssetRepositorySession',
    'AssetRepositoryAssignmentSession',
    'AssetCompositionSession',
    'AssetCompositionDesignSession',
    'CompositionLookupSession',
    'CompositionAdminSession',
    'CompositionQuerySession',
    'CompositionSearchSession',
    'CompositionRepositorySession',
    'CompositionRepositoryAssignmentSession',
    'RepositoryLookupSession',
    'RepositoryAdminSession',
    'RepositoryQuerySession',
    'RepositoryHierarchySession',
    'RepositoryHierarchyDesignSession',
    ## resource service
    'ResourceLookupSession',
    'ResourceQuerySession',
    'ResourceSearchSession',
    'ResourceAdminSession',
    'ResourceBinSession',
    'ResourceBinAssignmentSession',
    'ResourceAgentSession',
    'ResourceNotificationSession',
    'ResourceAgentAssignmentSession',
    'BinLookupSession',
    'BinAdminSession',
    'BinQuerySession',
    'BinHierarchySession',
    'BinHierarchyDesignSession',
]

objects_to_implement = [
    ### assessment service:
    'Item',
    'Question',
    'Answer',
    'Assessment',
    'AssessmentSection',
    'AssessmentOffered',
    'AssessmentTaken',
    'Response',
    'Bank',
    ### authentication_process:
    'Authentication',
    ### authorization service:
    'Authorization',
    'Vault',
    ### commenting service:
    'Comment',
    'Book',
    ### grading service:
    'Grade',
    'GradeSystem',
    'GradeEntry',
    'GradebookColumn',
    'GradebookColumnSummary',
    'GradebookColumnCalculation',
    'Gradebook',
    ### hierarchy service
    'Node',
    'Hierarchy',
    'HierarchyNode',
    ### id service
    'Id',
    ### learning service
    'Objective',
    'Activity',
    'ObjectiveBank',
    'Proficiency',
    ### locale service
    'Locale',
    'LocaleList',
    ### ontology service
    'Subject',
    ### proxy service
    'Proxy',
    'ProxyCondition',
    ### relationship service
    'Relationship',
    'Family',
    ### repository service
    'Asset',
    'AssetContent',
    'Composition',
    'Repository',
    ### resource service
    'Resource',
    'Bin',
    ### type service
    'Type',
]

variants_to_implement = [
    'Form',
    'Record',
    'FormRecord',
    'Query',
    'QueryRecord',
    'QueryFormRecord',
    'Search',
    'SearchRecord',
    'SearchResults',
    'SearchFormRecord',
    'List',
    'Node',
    'NodeList',
    'Search',
]
