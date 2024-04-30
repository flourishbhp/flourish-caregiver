from django.apps import apps as django_apps
from django.db.models import (FileField, ForeignKey, ImageField, ManyToManyField,
                              ManyToOneRel, OneToOneField)
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils.translation import ugettext_lazy as _
from flourish_export.admin_export_helper import AdminExportHelper

from ..helper_classes import MaternalStatusHelper
from ..helper_classes.utils import get_child_subject_identifier_by_visit


class ExportActionMixin(AdminExportHelper):

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'subject_identifier': 'matpid',
                       'child_subject_identifier': 'childpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}
        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict

    def export_as_csv(self, request, queryset):
        records = []
    
        for obj in queryset:
            data = obj.__dict__.copy()

            subject_identifier = getattr(obj, 'subject_identifier', None)
            screening_identifier = self.screening_identifier(
                subject_identifier=subject_identifier)
            previous_study = self.previous_bhp_study(
                screening_identifier=screening_identifier)
            caregiver_hiv_status = self.caregiver_hiv_status(
                subject_identifier=subject_identifier)

            # Add subject identifier and visit code
            if getattr(obj, 'maternal_visit', None):
                data_copy = data.copy()
                data.clear()
                study_maternal_identifier = self.study_maternal_identifier(
                    screening_identifier=screening_identifier)

                data.update(
                    matpid=subject_identifier,
                    old_matpid=study_maternal_identifier,
                    visit_code=obj.maternal_visit.visit_code,
                    **data_copy)

            # Update variable names for study identifiers
            data = self.update_variables(data)

            data.update(previous_study=previous_study,)
            data.update(hiv_status=caregiver_hiv_status,)
            data.update(study_status=self.study_status(subject_identifier) or '')

            for field in self.get_model_fields:
                field_name = field.name
                if (field_name == 'consent_version') and self.is_visit(obj):
                    data.update({f'{field_name}': self.get_consent_version(obj)})
                    continue
                if isinstance(field, (ForeignKey, OneToOneField, OneToOneRel,)):
                    continue
                if isinstance(field, (FileField, ImageField,)):
                    file_obj = getattr(obj, field_name, '')
                    data.update({f'{field_name}': getattr(file_obj, 'name', '')})
                    continue
                if isinstance(field, ManyToManyField):
                    data.update(self.m2m_data_dict(obj, field))
                    continue
                if not (self.is_consent(obj) or self.is_visit(obj)) and isinstance(field, ManyToOneRel):
                    data.update(self.inline_data_dict(obj, field))
                    continue   
            
            ultrasound_model_cls = django_apps.get_model(
                'flourish_caregiver.ultrasound')
            if isinstance(obj, ultrasound_model_cls):
                maternal_delivery_obj = self.maternal_delivery_obj(
                    maternal_visit=obj.maternal_visit)
                field_value = getattr(obj, 'get_current_ga', '')
                delivery_dt = getattr(
                    maternal_delivery_obj, 'delivery_datetime', None)
                delivery_dt = delivery_dt.date() if delivery_dt else ''
                ga_birth_usconfirm = field_value if delivery_dt else ''
                

                data.update(current_ga=field_value,
                            ga_birth_usconfirm=ga_birth_usconfirm,
                            maternal_delivery_date=delivery_dt)
            
            # Exclude identifying values
            data = self.remove_exclude_fields(data)
            # Correct date formats
            data = self.fix_date_formats(data)
            records.append(data)
        response = self.write_to_csv(records)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def get_consent_version(self, obj):
        """
        Returns the consent version of an object
        """
        version_model = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')
        try:
            version = version_model.objects.get(
                screening_identifier=self.screening_identifier(
                    subject_identifier=obj.subject_identifier, ))
        except version_model.DoesNotExist:
            return ""
        else:
            return version.version

    def previous_bhp_study(self, screening_identifier=None):
        dataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')
        if screening_identifier:
            try:
                dataset_obj = dataset_cls.objects.get(
                    screening_identifier=screening_identifier)
            except dataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj.protocol

    def study_maternal_identifier(self, screening_identifier=None):
        dataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')
        if screening_identifier:
            try:
                dataset_obj = dataset_cls.objects.get(
                    screening_identifier=screening_identifier)
            except dataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj.study_maternal_identifier

    def caregiver_hiv_status(self, subject_identifier=None):

        status_helper = MaternalStatusHelper(
            subject_identifier=subject_identifier)

        return status_helper.hiv_status

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent = self.consent_obj(subject_identifier=subject_identifier)

        if consent:
            return consent.screening_identifier
        return None

    def consent_obj(self, subject_identifier: str):
        consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        consent = consent_cls.objects.filter(
            subject_identifier=subject_identifier)

        if consent.exists():
            return consent.last()
        return None

    def is_consent(self, obj):
        consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        return isinstance(obj, consent_cls)

    def is_visit(self, obj):
        visit_cls = django_apps.get_model('flourish_caregiver.maternalvisit')
        return isinstance(obj, visit_cls)

    def study_status(self, subject_identifier=None):
        if not subject_identifier:
            return ''
        caregiver_offstudy_cls = django_apps.get_model(
            'flourish_prn.caregiveroffstudy')
        is_offstudy = caregiver_offstudy_cls.objects.filter(
            subject_identifier=subject_identifier).exists()

        return 'off_study' if is_offstudy else 'on_study'

    @property
    def exclude_fields(self):
        return ['created', '_state', 'hostname_created', 'hostname_modified',
                'revision', 'device_created', 'device_modified', 'id', 'site_id',
                'created_time', 'modified_time', 'report_datetime_time',
                'registration_datetime_time', 'screening_datetime_time', 'modified',
                'form_as_json', 'consent_model', 'randomization_datetime',
                'registration_datetime', 'is_verified_datetime', 'first_name',
                'last_name', 'initials', 'guardian_name', 'identity', 'infant_visit_id',
                'maternal_visit_id', 'processed', 'processed_datetime', 'packed',
                'packed_datetime', 'shipped', 'shipped_datetime', 'received_datetime',
                'identifier_prefix', 'primary_aliquot_identifier', 'clinic_verified',
                'clinic_verified_datetime', 'drawn_datetime', 'slug', 'confirm_identity',
                'related_tracking_identifier', 'parent_tracking_identifier', 'site',
                'subject_consent_id', '_django_version', 'consent_identifier',
                'subject_identifier_as_pk']

    @property
    def maternal_delivery(self):
        return django_apps.get_model('flourish_caregiver.maternaldelivery')

    def maternal_delivery_obj(self, maternal_visit=None):
        """
        Takes subject identifier and return a maternal delivery objects
        """
        subject_identifier = getattr(
            maternal_visit, 'subject_identifier', None)
        child_subject_identifier = get_child_subject_identifier_by_visit(maternal_visit)
        try:
            maternal_delivery_obj = self.maternal_delivery.objects.get(
                subject_identifier=subject_identifier,
                child_subject_identifier=child_subject_identifier)
        except self.maternal_delivery.DoesNotExist:
            return None
        else:
            return maternal_delivery_obj
