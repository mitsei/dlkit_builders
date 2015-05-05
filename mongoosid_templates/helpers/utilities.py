"""Utilities for tests.py"""
# pylint: skip-file
#    This is ugly and will all be replaced with generated tests

from .learning.managers import LearningManager
from .repository.managers import RepositoryManager
from .assessment.managers import AssessmentManager
from .primitives import Id, Type, DisplayText
from .types import Genus
from .osid.osid_errors import AlreadyExists, NotFound

DEFAULT_TYPE = Type(**Genus().get_type_data('DEFAULT'))


def get_objective_bank_by_name(name):
    obls = LearningManager().get_objective_bank_lookup_session()
    for ob in obls.get_objective_banks():
        if ob.display_name.text == name:
            return ob
    raise NotFound()

def get_objective_by_bank_id_and_name(objective_bank_id, name):
    ols = LearningManager().get_objective_lookup_session_for_objective_bank(objective_bank_id)
    for o in ols.get_objectives():
        if o.display_name.text == name:
            return o
    raise NotFound()

def create_sandbox_objective_bank(display_name, description=None):
    if description is None:
        description = 'Catalog for ' + display_name
    lm = LearningManager()
    obas = lm.get_objective_bank_admin_session()
    obls = lm.get_objective_bank_lookup_session()
    for ob in obls.get_objective_banks():
        if ob.display_name.text == display_name:
            print 'A sandbox bank named', display_name, 'already exists.'
            return None
    obfc = obas.get_objective_bank_form_for_create([])
    obfc.display_name = display_name
    obfc.description = description
    obfc.genus_type = DEFAULT_TYPE
    return obas.create_objective_bank(obfc)

def delete_objective_bank_by_name(display_name):
    lm = LearningManager()
    obas = lm.get_objective_bank_admin_session()
    obls = lm.get_objective_bank_lookup_session()
    found = False
    for ob in obls.get_objective_banks():
        if ob.display_name.text == display_name:
            found = True
            ols = lm.get_objective_lookup_session_for_objective_bank(ob.ident)
            als = lm.get_activity_lookup_session_for_objective_bank(ob.ident)
            if ols.get_objectives().available() != 0:
                print 'can not delete objective bank \'' + ob.display_name.text + '\'. It still contains objectives.'
            elif als.get_activities().available() != 0:
                print 'can not delete objective bank \'' + ob.display_name.text + '\'. It still contains activities.'
            else:
                print 'deleting objective bank', ob
                obas.delete_objective_bank(ob.ident)
    if not found:
        print 'objective bank \'' + display_name + '\' not found.'


def create_objective(bank_id, display_name, description=None):
    if description is None:
        description = display_name + ' objective'
    lm = LearningManager()
    ols = lm.get_objective_lookup_session_for_objective_bank(bank_id)
    oas = lm.get_objective_admin_session_for_objective_bank(bank_id)
    for o in ols.get_objectives():
        if o.display_name.text == display_name:
            return o
    ofc = oas.get_objective_form_for_create([])
    ofc.display_name = display_name
    ofc.description = description
    return oas.create_objective(ofc)
    

def get_repository_by_name(name):
    rls = RepositoryManager().get_repository_lookup_session()
    for r in rls.get_repositories():
        if r.display_name.text == name:
            return r
    raise NotFound()

def get_asset_by_repository_id_and_name(repository_id, name):
    als = RepositoryManager().get_asset_lookup_session_for_repository(repository_id)
    for a in als.get_assets():
        if a.display_name.text == name:
            return a
    raise NotFound()

def create_sandbox_repository(display_name, description=None):
    if description is None:
        description = 'Catalog for ' + display_name
    rm = RepositoryManager()
    ras = rm.get_repository_admin_session()
    rls = rm.get_repository_lookup_session()
    for r in rls.get_repositories():
        if r.display_name.text == display_name:
            print 'A sandbox repository named', display_name, 'already exists.'
            return None
    rfc = ras.get_repository_form_for_create([])
    rfc.display_name = display_name
    rfc.description = description
    rfc.genus_type = DEFAULT_TYPE
    return ras.create_repository(rfc)

def delete_repository_by_name(display_name):
    rm = RepositoryManager()
    ras = rm.get_repository_admin_session()
    rls = rm.get_repository_lookup_session()
    found = False
    for r in rls.get_repositories():
        if r.display_name.text == display_name:
            found = True
            als = rm.get_asset_lookup_session_for_repository(r.ident)
            if als.get_assets().available() != 0:
                print 'can not delete repository \'' + ob.display_name.text + '\'. It still contains assets.'
            else:
                print 'deleting repository', r
                ras.delete_repository(r.ident)
    if not found:
        print 'repository \'' + display_name + '\' not found.'


def create_asset(repository_id, display_name, description=None):
    if description is None:
        description = display_name + ' asset'
    rm = RepositoryManager()
    als = rm.get_asset_lookup_session_for_repository(repository_id)
    aas = rm.get_asset_admin_session_for_repository(repository_id)
    for a in als.get_assets():
        if a.display_name.text == display_name:
            return a
    afc = aas.get_asset_form_for_create([])
    afc.display_name = display_name
    afc.description = description
    return aas.create_asset(afc)
    


def get_bank_by_name(name):
    bls = AssessmentManager().get_bank_lookup_session()
    for b in bls.get_banks():
        if b.display_name.text == name:
            return b
    raise NotFound()

def get_item_by_bank_id_and_name(bank_id, name):
    ils = AssessmentManager().get_item_lookup_session_for_bank(bank_id)
    for i in ils.get_items():
        if i.display_name.text == name:
            return i
    raise NotFound()

def get_assessment_by_bank_id_and_name(bank_id, name):
    als = AssessmentManager().get_assessment_lookup_session_for_bank(bank_id)
    for a in als.get_assessments():
        if a.display_name.text == name:
            return a
    raise NotFound()

def get_assessment_offered_by_bank_id_and_name(bank_id, name):
    aols = AssessmentManager().get_assessment_offered_lookup_session_for_bank(bank_id)
    for ao in aols.get_assessments_offered():
        if ao.display_name.text == name:
            return ao
    raise NotFound()

def get_assessment_taken_by_bank_id_and_name(bank_id, name):
    atls = AssessmentManager().get_assessment_taken_lookup_session_for_bank(bank_id)
    for at in atls.get_assessments_taken():
        if at.display_name.text == name:
            return at
    raise NotFound()


def create_sandbox_bank(display_name, description=None):
    if description is None:
        description = 'Catalog for ' + display_name
    am = AssessmentManager()
    bas = am.get_bank_admin_session()
    bls = am.get_bank_lookup_session()
    for b in bls.get_banks():
        if b.display_name.text == display_name:
            print 'A sandbox bank named', display_name, 'already exists.'
            return None
    bfc = bas.get_bank_form_for_create([])
    bfc.display_name = display_name
    bfc.description = description
    bfc.genus_type = DEFAULT_TYPE
    return bas.create_bank(bfc)

def delete_bank_by_name(display_name):
    am = AssessmentManager()
    bas = rm.get_bank_admin_session()
    bls = rm.get_bank_lookup_session()
    found = False
    for b in rls.get_banks():
        if b.display_name.text == display_name:
            found = True
            ils = am.get_item_lookup_session_for_bank(b.ident)
            als = am.get_assessment_lookup_session_for_bank(b.ident)
            aols = am.get_assessment_offered_lookup_session_for_bank(b.ident)
            atls = am.get_assessment_taken_lookup_session_for_bank(b.ident)
            if ils.get_items().available() != 0:
                print 'can not delete bank \'' + ob.display_name.text + '\'. It still contains items.'
            if als.get_assessments().available() != 0:
                print 'can not delete bank \'' + ob.display_name.text + '\'. It still contains assessments.'
            if aols.get_assessments_offered().available() != 0:
                print 'can not delete bank \'' + ob.display_name.text + '\'. It still contains offered assessments.'
            if atls.get_assessments_taken().available() != 0:
                print 'can not delete bank \'' + ob.display_name.text + '\'. It still contains taken assessments.'
            else:
                print 'deleting bank', b
                bas.delete_bank(b.ident)
    if not found:
        print 'bank \'' + display_name + '\' not found.'

def get_item_by_bank_id_and_name(bank_id, name):
    ils = AssessmentManager().get_item_lookup_session_for_bank(bank_id)
    for i in ils.get_items():
        if i.display_name.text == name:
            return i
    raise NotFound()
