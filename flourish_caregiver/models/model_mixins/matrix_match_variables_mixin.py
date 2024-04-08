from django.apps import apps as django_apps
from edc_base.utils import age, get_utcnow


class MatrixMatchVariablesMixin:

    @property
    def child_clinical_measurements_cls(self):
        return django_apps.get_model('flourish_child.childclinicalmeasurements')
        
    @property
    def child_bmi(self):
        try:
            model_obj = self.child_clinical_measurements_cls.objects.filter(
                child_visit__subject_identifier=self.subject_identifier).latest(
                    'report_datetime')
        except self.child_clinical_measurements_cls.DoesNotExist:
            return None
        else:
            return model_obj.child_weight_kg / pow(model_obj.child_height/100, 2)

    @property
    def child_age(self):
        dob = getattr(self.caregiver_child_consent, 'child_dob', None)
        if not dob:
            return None
        _age = age(dob, get_utcnow().date())
        _age = _age.years + _age.months / 12 + _age.days / 365
        return _age

    @property
    def child_gender(self):
        return getattr(self.caregiver_child_consent, 'gender', None)
