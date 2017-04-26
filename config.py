
packages_to_implement = [
    'assessment',
    'assessment.authoring',
    'authentication.process',
    'authentication',
    'authorization',
    'cataloging',
    'commenting',
    'grading',
    'hierarchy',
    'id',
    'learning',
    'locale',
    'logging',
    'mapping',
    'ontology',
    'osid',
    'proxy',
    'relationship',
    'repository',
    'resource',
    'rules',
    'type',
]

packages_to_test = [
    'assessment',
    'assessment.authoring',
    'authorization',
    'commenting',
    'grading',
    'learning',
    'logging',
    'repository',
    'resource',
]

managers_to_implement = [
    'assessment',
    'assessment.authoring',
    'authentication.process',
    'authentication',
    'authorization',
    'cataloging',
    'commenting',
    'grading',
    'hierarchy',
    'id',
    'learning',
    'logging',
    'locale',
    'osid',
    'proxy',
    'relationship',
    'repository',
    'resource',
    'type',
]

sessions_to_implement = [
    # assessment service:
    'AssessmentSession',
    'AssessmentResultsSession',
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
    # assessment authoring:
    'AssessmentPartLookupSession',
    'AssessmentPartAdminSession',
    'AssessmentPartItemSession',
    'AssessmentPartItemDesignSession',
    'SequenceRuleLookupSession',
    'SequenceRuleAdminSession',
    # authentication service:
    'AgentLookupSession',
    # authorization service:
    'AuthorizationSession',
    'AuthorizationLookupSession',
    'AuthorizationAdminSession',
    'AuthorizationQuerySession',
    'VaultLookupSession',
    'VaultAdminSession',
    'VaultQuerySession',
    # cataloging service:
    'CatalogSession',
    'CatalogAssignmentSession',
    'CatalogLookupSession',
    'CatalogAdminSession',
    'CatalogHierarchySession',
    'CatalogHierarchyDesignSession',
    # commenting service:
    'CommentLookupSession',
    'CommentQuerySession',
    'CommentAdminSession',
    'BookLookupSession',
    'BookAdminSession',
    'BookHierarchySession',
    'BookHierarchyDesignSession',
    # grading service:
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
    # hierarchy service:
    'HierarchyLookupSession',
    'HierarchyAdminSession',
    'HierarchyTraversalSession',
    'HierarchyDesignSession',
    # learning service:
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
    # logging service:
    'LoggingSession',
    'LogEntryLookupSession',
    'LogEntryAdminSession',
    'LogEntryQuerySession',
    'LogLookupSession',
    'LogAdminSession',
    # ontology service:
    'SubjectHierarchyDesignSession',
    # proxy service
    'ProxySession',
    # relationship service
    'RelationshipLookupSession',
    'RelationshipQuerySession',
    'RelationshipAdminSession',
    'FamilyLookupSession',
    'FamilyAdminSession',
    'FamilyHierarchySession',
    'FamilyHierarchyDesignSession',
    # repository service
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
    # resource service
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
    # assessment service:
    'Item',
    'Question',
    'Answer',
    'Assessment',
    'AssessmentSection',
    'AssessmentOffered',
    'AssessmentTaken',
    'Response',
    'Bank',
    # assessment authoring service:
    'AssessmentPart',
    'SequenceRule',
    # authentication_process:
    'Authentication',
    # authentication:
    'Agent',
    # authorization service:
    'Authorization',
    'Vault',
    # ctaloging service:
    'Catalog',
    # commenting service:
    'Comment',
    'Book',
    # grading service:
    'Grade',
    'GradeSystem',
    'GradeEntry',
    'GradebookColumn',
    'GradebookColumnSummary',
    'GradebookColumnCalculation',
    'Gradebook',
    # hierarchy service
    'Node',
    'Hierarchy',
    'HierarchyNode',
    # id service
    'Id',
    # learning service
    'Objective',
    'Activity',
    'ObjectiveBank',
    'Proficiency',
    # locale service
    'Locale',
    'LocaleList',
    # logging service
    'Log',
    'LogEntry',
    # ontology service
    'Subject',
    # proxy service
    'Proxy',
    'ProxyCondition',
    # relationship service
    'Relationship',
    'Family',
    # repository service
    'Asset',
    'AssetContent',
    'Composition',
    'Repository',
    # resource service
    'Resource',
    'Bin',
    # type service
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
