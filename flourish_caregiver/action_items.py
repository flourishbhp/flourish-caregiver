from edc_action_item import Action, site_action_items, HIGH_PRIORITY
from edc_locator.action_items import SubjectLocatorAction

CAREGIVEROFF_STUDY_ACTION = 'submit-caregiveroff-study'
CAREGIVER_LOCATOR_ACTION = 'submit-caregiver-locator'
ULTRASOUND_ACTION = 'submit-ultrasound'
MATERNAL_COVID_SCREENING_ACTION = 'update-maternal-covid-results'
MATERNAL_VISIT_ACTION = 'maternal-visit'
TB_OFF_STUDY_ACTION = 'submit-tb-off-study'


class CaregiverOffStudyAction(Action):
    name = CAREGIVEROFF_STUDY_ACTION
    display_name = 'Submit Caregiver Offstudy'
    reference_model = 'flourish_prn.caregiveroffstudy'
    admin_site_name = 'flourish_prn_admin'
    priority = HIGH_PRIORITY
    singleton = True


class CaregiverLocatorAction(SubjectLocatorAction):
    name = CAREGIVER_LOCATOR_ACTION
    display_name = 'Submit Caregiver Locator'
    reference_model = 'flourish_caregiver.caregiverlocator'
    admin_site_name = 'flourish_caregiver_admin'


class MaternalUltrasoundAction(Action):
    name = ULTRASOUND_ACTION
    display_name = 'Submit Maternal Ultrasound'
    reference_model = 'flourish_caregiver.ultrasound'
    admin_site_name = 'flourish_caregiver_admin'
    create_by_user = False

    def get_next_actions(self):
        actions = []

        # resave visit to update metadata
        self.reference_model_obj.maternal_visit.save()

        if self.reference_model_obj.number_of_gestations != '1':
            actions = [CaregiverOffStudyAction]
        else:
            self.delete_if_new(CaregiverOffStudyAction)
        return actions


class MaternalCovidScreeningAction(Action):
    name = MATERNAL_COVID_SCREENING_ACTION
    display_name = 'Update Maternal Covid Screening Test Results'
    reference_model = 'flourish_caregiver.maternalcovidscreening'
    admin_site_name = 'flourish_caregiver_admin'
    priority = HIGH_PRIORITY

    def close_action_item_on_save(self):
        """Returns True if action item for \'action_identifier\'
        is to be closed on post_save.
        """
        return self.reference_model_obj.covid_results != 'pending'


class TbOffStudyAction(Action):
    name = TB_OFF_STUDY_ACTION
    display_name = 'Submit Tb Offstudy'
    reference_model = 'flourish_caregiver.tboffstudy'
    admin_site_name = 'flourish_caregiver_admin'
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        self.delete_if_new(CaregiverOffStudyAction)
        return []


site_action_items.register(CaregiverLocatorAction)
site_action_items.register(TbOffStudyAction)
site_action_items.register(MaternalUltrasoundAction)
