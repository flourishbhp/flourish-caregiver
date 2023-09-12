from django.apps import apps as django_apps

from ..helper_classes.cohort_assignment import CohortAssignment
from ..models.maternal_dataset import MaternalDataset


def cohort_assigned(study_child_identifier, child_dob, enrollment_date):
    """Calculates participant's cohort based on the maternal and child dataset
    """
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
            maternal_dataset_obj = MaternalDataset.objects.get(
                study_maternal_identifier=getattr(
                    infant_dataset_obj, 'study_maternal_identifier', None))
        except MaternalDataset.DoesNotExist:
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
