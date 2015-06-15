
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
    'osid',
    'proxy',
    'relationship',
    'repository',
    'resource',
    'type',
]

packages_to_test = [
    'assessment',
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
    'ItemAdminSession',
    'AssessmentLookupSession',
    'AssessmentQuerySession',
    'AssessmentAdminSession',
    'AssessmentBasicAuthoringSession',
    'AssessmentOfferedLookupSession',
    'AssessmentOfferedQuerySession',
    'AssessmentOfferedAdminSession',
    'AssessmentTakenLookupSession',
    'AssessmentTakenQuerySession',
    'AssessmentTakenAdminSession',
    'BankLookupSession',
    'BankAdminSession',
    'BankHierarchySession',
    'BankHierarchyDesignSession',
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
    'GradeEntryLookupSession',
    'GradeEntryAdminSession',
    'GradebookColumnLookupSession',
    'GradebookColumnAdminSession',
    ### hierarchy service:
    'HierarchyLookupSession',
    'HierarchyAdminSession',
    'HierarchyTraversalSession',
    'HierarchyDesignSession',
    ### learning service:
    'ObjectiveLookupSession',
    'ObjectiveAdminSession',
    'ObjectiveHierarchySession',
    'ObjectiveHierarchyDesignSession',
    'ObjectiveSequencingSession',
    'ObjectiveRequisiteSession',
    'ObjectiveRequisiteAssignmentSession',
    'ActivityLookupSession',
    'ActivityAdminSession',
    'ObjectiveBankLookupSession',
    'ObjectiveBankAdminSession',
    'ObjectiveBankHierarchySession',
    'ObjectiveBankHierarchyDesignSession',
    ### proxy service
    'ProxySession',
    ### relationship service
    'RelationshipLookupSession',
    'RelationshipAdminSession',
    'FamilyLookupSession',
    'FamilyAdminSession',
    'FamilyHierarchySession',
    'FamilyHierarchyDesignSession',
    ### repository service
    'AssetLookupSession',
    'AssetQuerySession',
    'AssetAdminSession',
    'AssetCompositionSession',
    'AssetCompositionDesignSession',
    'CompositionLookupSession',
    'CompositionAdminSession',
    'RepositoryLookupSession',
    'RepositoryAdminSession',
    'RepositoryHierarchySession',
    'RepositoryHierarchyDesignSession',
    ## resource service
    'ResourceLookupSession',
    'ResourceAdminSession',
    'ResourceAgentSession',
    'ResourceAgentAssignmentSession',
    'BinLookupSession',
    'BinAdminSession',
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
    ### authentication_process
    'Authentication',
    ### commenting service:
    'Comment',
    'Book',
    ### grading service:
    'Grade',
    'GradeSystem',
    'GradeEntry',
    'GradebookColumn',
    'GradebookColumnSummary',
    'Gradebook',
    ### hierarchy service
    'Hierarchy',
    'HierarchyNode',
    ### id service
    'Id',
    ### learning service
    'Objective',
    'Activity',
    'ObjectiveBank',
    ### locale service
    'Locale',
    'LocaleList',
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
    'List',
]
