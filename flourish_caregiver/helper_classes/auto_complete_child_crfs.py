from copy import deepcopy

from django.apps import apps as django_apps
from django.db import models
from django.forms import model_to_dict
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
                    self.save_model(model_obj=model_obj, model_cls=model_cls)

    @property
    def maternal_inlines_crfs(self):
        """
        Returns a list of possible inline forms found in child crfs
        """
        return {
            'cliniciannotesimage': ['cliniciannotesimage', 'clinician_notes'],
            'maternalarvduringpreg': ['maternalarv', 'maternal_arv_durg_preg']}

    @property
    def completed_crfs(self):
        """all the completed crfs for the first child visit"""
        if self.first_visit:
            return CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier,
                visit_code=self.visit_code,
                schedule_name=self.first_visit.schedule_name,
                entry_status=KEYED)
        else:
            return []

    @property
    def visit_crfs(self):
        """getting all the required crfs in the current visit"""
        return CrfMetadata.objects.filter(
            subject_identifier=self.subject_identifier,
            visit_code=self.visit_code,
            schedule_name=self.schedule_name,
            entry_status=REQUIRED).values_list('model', flat=True)

    @property
    def first_visit(self):
        """
        two children, the first child is the one whose visit was done first and the
        parent's crf were captured on that visit, the second child the forms are still
        blank get the visit of the first child"""
        return MaternalVisit.objects.filter(
            subject_identifier=self.subject_identifier,
            visit_code=self.visit_code).earliest('report_datetime')

    def inline_cls(self, inline):
        return django_apps.get_model(f'flourish_caregiver.{inline}')

    def inline_objs(self, model_obj, value, key):
        filters = {value: model_obj}
        return self.inline_cls(key).objects.filter(**filters)

    def save_inlines(self, new_obj, model_obj):
        """
        takes two params, new obj and model_obj then saves the inline models of the new
        obj based on the values of the old model
        """
        for key in self.maternal_inlines_crfs:
            if (new_obj._meta.label_lower.split('.')[1] in
                    self.maternal_inlines_crfs.get(key)[0]):
                for maternal_inline in self.inline_objs(
                        model_obj, self.maternal_inlines_crfs.get(key)[1],
                        self.maternal_inlines_crfs.get(key)[0]):
                    copy_maternal_inline = deepcopy(maternal_inline)
                    setattr(copy_maternal_inline,
                            self.maternal_inlines_crfs.get(key)[1],
                            new_obj)
                    copy_maternal_inline.id = None
                    copy_maternal_inline.save()

    def get_many_to_many_fields(self, model_obj):
        """
        Return a dictionary of many-to-many fields in a model
        """
        return model_to_dict(model_obj,
                             fields=[field.name for field in
                                     model_obj._meta.get_fields() if
                                     isinstance(field, models.ManyToManyField)])

    def save_model(self, model_obj, model_cls):
        """
        Get an existing model object as params and copy and save the model copy to create
        copy of the existing object
        """
        kwargs = model_to_dict(model_obj,
                               fields=[field.name for field in
                                       model_obj._meta.fields],
                               exclude=['id', 'maternal_visit_id',
                                        'maternal_visit'])
        new_obj = model_cls.objects.create(**kwargs,
                                           maternal_visit_id=self.id,
                                           maternal_visit=self.instance)
        for key in self.get_many_to_many_fields(model_obj):
            getattr(new_obj, key).set(self.get_many_to_many_fields(model_obj).get(key))
        new_obj.save()
        self.save_inlines(new_obj, model_obj)