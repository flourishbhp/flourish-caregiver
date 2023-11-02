from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from ..helper_classes.cohort_assignment import CohortAssignment


def cohort_assigned(study_child_identifier, child_dob, enrollment_date):
    """Calculates participant's cohort based on the maternal and child dataset
    """

    maternal_dataset_cls = django_apps.get_model('flourish_caregiver.maternaldataset')
    infant_dataset_cls = django_apps.get_model('flourish_child.childdataset')
    infant_dataset_obj = None
    try:
        infant_dataset_obj = infant_dataset_cls.objects.get(
            study_child_identifier=study_child_identifier,
            dob=child_dob)
    except infant_dataset_cls.DoesNotExist:
        pass
    except infant_dataset_cls.MultipleObjectsReturned:
        infant_dataset_obj = infant_dataset_cls.objects.filter(
            study_child_identifier=study_child_identifier,
            dob=child_dob)[0]
    finally:
        try:
            maternal_dataset_obj = maternal_dataset_cls.objects.get(
                study_maternal_identifier=getattr(
                    infant_dataset_obj, 'study_maternal_identifier', None))
        except maternal_dataset_cls.DoesNotExist:
            return None
        else:
            cohort = CohortAssignment(
                child_dob=child_dob,
                enrolment_dt=enrollment_date,
                child_hiv_exposure=getattr(
                    infant_dataset_obj, 'infant_hiv_exposed', None),
                arv_regimen=getattr(
                    maternal_dataset_obj, 'mom_pregarv_strat', None), )
            return cohort.cohort_variable or None


def update_preg_screening_obj_child_pid(consent, child_subject_identifier):
    screening_model_cls = django_apps.get_model('flourish_caregiver.screeningpregwomen')
    screening_obj = screening_model_cls.objects.filter(
        screening_identifier=consent.screening_identifier).first()

    if screening_obj:
        try:
            screening_obj.screeningpregwomeninline_set.get(
                child_subject_identifier=child_subject_identifier)
        except ObjectDoesNotExist:
            screenings_without_child_pid = screening_obj.screeningpregwomeninline_set.filter(
                child_subject_identifier__isnull=True)
            if screenings_without_child_pid.exists():
                child_screening_obj = screenings_without_child_pid.first()
                child_screening_obj.child_subject_identifier = child_subject_identifier
                child_screening_obj.save()
