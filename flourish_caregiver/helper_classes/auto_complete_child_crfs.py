from copy import deepcopy

from django.apps import apps as django_apps
from edc_metadata import REQUIRED, KEYED
from edc_metadata.models import CrfMetadata

from flourish_caregiver.models import MaternalVisit


class AutoCompleteChildCrfs:

    def __init__(self, instance):
        self.subject_identifier = instance.subject_identifier
        self.visit_code = instance.visit_code
        self.schedule_name = instance.schedule_name
        self.id = instance.id
        self.instance = instance

    def pre_fill_crfs(self):
        # check clone the copleted crfs into the current visit
        for crf in self.completed_crfs:
            if crf.model in self.visit_crfs:
                model_cls = django_apps.get_model(crf.model)
                try:
                    model_obj = model_cls.objects.get(
                        maternal_visit__subject_identifier=self.subject_identifier,
                        maternal_visit__visit_code=self.visit_code)
                except model_cls.DoesNotExist:
                    pass
                else:
                    self.save_model(model_obj=model_obj)

    @property
    def inlines(self):
        """
        Returns a list of possible inline forms found in child crfs
        """
        return {
            'cliniciannotesimage': 'clinician_notes',
            'maternalarv': 'maternal_arv_during_preg'}

    @property
    def completed_crfs(self):
        """all the completed crfs for the first child visit"""
        return CrfMetadata.objects.filter(
            subject_identifier=self.subject_identifier,
            visit_code=self.visit_code,
            schedule_name=self.first_visit.schedule_name,
            entry_status=KEYED)

    @property
    def visit_crfs(self):
        """getting all the required crfs in the current visit"""
        try:
            visit_crfs = CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_code,
                schedule_name=self.schedule_name,
                entry_status=REQUIRED).values_list('model', flat=True)
        except CrfMetadata.DoesNotExist:
            return []
        else:
            return visit_crfs

    @property
    def first_visit(self):
        """
        tow children, the first child is the one whose visit was done first and the
        parent's crf were captured on that visit, the second child the forms are still
        blank get the visit of the first child"""
        try:
            first_visit = MaternalVisit.objects.filter(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_code).earliest('report_datetime')
        except MaternalVisit.DoesNotExist:
            return []
        else:
            return first_visit

    def inline_cls(self, inline):
        return django_apps.get_model(f'flourish_caregiver.{inline}')

    def inline_objs(self, model_obj, value, key):
        filters = {value: model_obj}
        return self.inline_cls(key).objects.filter(**filters)

    def save_inlines(self, new_obj, model_obj):
        """
        takes tow params, new obj and model_obj then saves the inline models of the new
        obj based on the values of the old model
        """
        for key in self.inlines:
            if new_obj.__class__.__name__.lower()[:7] in self.inlines.get(key):
                for child_inline in self.inline_objs(
                        model_obj, self.inlines.get(key), key):
                    copy_child_inline = deepcopy(child_inline)
                    setattr(copy_child_inline, self.inlines.get(key), new_obj)
                    copy_child_inline.id = None
                    copy_child_inline.save()

    def save_model(self, model_obj):
        """
        Get an existing model object as params and copy and save the model copy to create
        copy of the existing object
        """
        new_obj = deepcopy(model_obj)
        new_obj.maternal_visit_id = self.id
        new_obj.maternal_visit = self.instance
        new_obj.id = None
        new_obj.save()
        self.save_inlines(new_obj, model_obj)
