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

    def formInline(self):
        """
        Returns a list of form inline if the form has inlines
        """
        pass

    @property
    def inlines(self):
        """
        Returns a list of possible inline forms found in child crfs
        """
        return ['chronicconditions', 'childmedications', 'wcsdxadult', 'childdiseases',
                'childcovidsymptoms', 'childcovidsymptomsafter14days', 'solidfoods']

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

    def get_fk_models(self, model_obj):
        """
        Returns foreign key models of a specific model
        """
        fk_models = []
        [fk_models.append(f.related_model._meta.label_lower) for f in
         model_obj._meta.get_fields() if
         isinstance(f, models.ForeignKey)]
        return fk_models

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
        Get and save fields of a specific model
        """
        kwargs = model_to_dict(model_obj,
                               fields=[field.name for field in
                                       model_obj._meta.fields],
                               exclude=['id', 'maternal_visit_id',
                                        'maternal_visit'])
        temp_obj = model_cls.objects.create(**kwargs,
                                            maternal_visit_id=self.id,
                                            maternal_visit=self.instance)

        for key in self.get_many_to_many_fields(model_obj):
            # breakpoint()
            setattr(temp_obj, key, self.get_many_to_many_fields(model_obj).get(key))
        temp_obj.save()
