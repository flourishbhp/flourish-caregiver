import datetime
import uuid

from django.apps import apps as django_apps
from django.db.models import ManyToManyField, ForeignKey, OneToOneField, ManyToOneRel
from django.db.models.fields.reverse_related import OneToOneRel
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import xlwt

from ..helper_classes import MaternalStatusHelper


class ExportActionMixin:

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (
            self.get_export_filename())

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws = wb.add_sheet('%s')

        row_num = 0
        obj_count = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = 'YYYY/MM/DD h:mm:ss'

        field_names = []
        for field in self.get_model_fields:
            if isinstance(field, ManyToManyField):
                choices_count = len(field.get_choices())
                for num in range(choices_count):
                    field_names.append(f'{field.name}_{num}')
                continue
            field_names.append(field.name)

        if queryset and self.is_consent(queryset[0]):
            field_names.insert(0, 'previous_study')
            field_names.insert(1, 'hiv_status')

        if queryset and getattr(queryset[0], 'maternal_visit', None):
            field_names.insert(0, 'subject_identifier')
            field_names.insert(1, 'study_maternal_identifier')
            field_names.insert(2, 'previous_study')
            field_names.insert(3, 'hiv_status')
            field_names.insert(4, 'visit_code')

        if ((queryset[0]._meta.label_lower.split('.')[1] == 'ultrasound') and
                queryset[0].get_current_ga):
            field_names.append('current_ga')

        for col_num in range(len(field_names)):
            ws.write(row_num, col_num, field_names[col_num], font_style)

        for obj in queryset:
            data = []
            inline_field_names = []

            # Add subject identifier and visit code
            if getattr(obj, 'maternal_visit', None):

                subject_identifier = obj.maternal_visit.subject_identifier
                screening_identifier = self.screening_identifier(
                    subject_identifier=subject_identifier)
                previous_study = self.previous_bhp_study(
                    screening_identifier=screening_identifier)
                study_maternal_identifier = self.study_maternal_identifier(
                    screening_identifier=screening_identifier)
                caregiver_hiv_status = self.caregiver_hiv_status(
                    subject_identifier=subject_identifier)

                data.append(subject_identifier)
                data.append(study_maternal_identifier)
                data.append(previous_study)
                data.append(caregiver_hiv_status)
                data.append(obj.maternal_visit.visit_code)

            elif self.is_consent(obj):

                subject_identifier = getattr(obj, 'subject_identifier')
                screening_identifier = self.screening_identifier(
                    subject_identifier=subject_identifier)
                previous_study = self.previous_bhp_study(
                    screening_identifier=screening_identifier)
                caregiver_hiv_status = self.caregiver_hiv_status(
                    subject_identifier=subject_identifier)

                data.append(previous_study)
                data.append(caregiver_hiv_status)

            inline_objs = []
            for field in self.get_model_fields:
                if isinstance(field, ManyToManyField):
                    choices_count = len(field.get_choices())
                    m2m_values = [None] * choices_count
                    key_manager = getattr(obj, field.name)
                    for _count, m2m_obj in enumerate(key_manager.all()):
                        m2m_values[_count] = m2m_obj.name
                    data.extend(m2m_values)
                    continue
                if isinstance(field, (ForeignKey, OneToOneField,)):
                    field_value = getattr(obj, field.name)
                    data.append(field_value.id)
                    continue
                if isinstance(field, OneToOneRel):
                    continue
                if isinstance(field, ManyToOneRel):
                    key_manager = getattr(obj, f'{field.name}_set')
                    inline_values = key_manager.all()
                    fields = field.related_model._meta.get_fields()
                    inline_field_names.extend(
                            [field.name for field in fields if not isinstance(
                                field, (ForeignKey, OneToOneField,))])
                    if inline_values:
                        inline_objs.append(inline_values)
                field_value = getattr(obj, field.name, '')
                data.append(field_value)

            if ((queryset[0]._meta.label_lower.split('.')[1] == 'ultrasound') and
                    queryset[0].get_current_ga):
                field_value = getattr(obj, 'get_current_ga', '')
                data.append(field_value)

            if inline_objs:
                # Update header
                inline_field_names = self.inline_exclude(field_names=inline_field_names)
                if obj_count == 0:
                    self.update_headers_inline(
                        inline_fields=inline_field_names, field_names=field_names,
                        ws=ws, row_num=0, font_style=font_style)

                for inline_qs in inline_objs:
                    for inline_obj in inline_qs:
                        inline_data = []
                        inline_data.extend(data)
                        for field in inline_field_names:
                            field_value = getattr(inline_obj, field, '')
                            inline_data.append(field_value)
                        row_num += 1
                        self.write_rows(data=inline_data, row_num=row_num, ws=ws)
                obj_count += 1
            else:
                row_num += 1
                self.write_rows(data=data, row_num=row_num, ws=ws)
        wb.save(response)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def write_rows(self, data=None, row_num=None, ws=None):
        for col_num in range(len(data)):
            if isinstance(data[col_num], uuid.UUID):
                ws.write(row_num, col_num, str(data[col_num]))
            elif isinstance(data[col_num], datetime.datetime):
                dt = data[col_num]
                if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
                    dt = timezone.make_naive(dt)
                dt = dt.strftime('%Y/%m/%d')
                ws.write(row_num, col_num, dt, xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            elif isinstance(data[col_num], datetime.date):
                ws.write(row_num, col_num, data[col_num], xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            else:
                ws.write(row_num, col_num, data[col_num])

    def update_headers_inline(self, inline_fields=None, field_names=None,
                              ws=None, row_num=None, font_style=None):
        top_num = len(field_names)
        for col_num in range(len(inline_fields)):
            ws.write(row_num, top_num, inline_fields[col_num], font_style)
            top_num += 1

    def get_export_filename(self):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s" % (self.model.__name__, date_str)
        return filename

    def previous_bhp_study(self, screening_identifier=None):
        dataset_cls = django_apps.get_model('flourish_caregiver.maternaldataset')
        if screening_identifier:
            try:
                dataset_obj = dataset_cls.objects.get(
                    screening_identifier=screening_identifier)
            except dataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj.protocol

    def study_maternal_identifier(self, screening_identifier=None):
        dataset_cls = django_apps.get_model('flourish_caregiver.maternaldataset')
        if screening_identifier:
            try:
                dataset_obj = dataset_cls.objects.get(
                    screening_identifier=screening_identifier)
            except dataset_cls.DoesNotExist:
                return None
            else:
                return dataset_obj.study_maternal_identifier

    def caregiver_hiv_status(self, subject_identifier=None):

        status_helper = MaternalStatusHelper(subject_identifier=subject_identifier)

        return status_helper.hiv_status

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent_cls = django_apps.get_model('flourish_caregiver.subjectconsent')
        consent = consent_cls.objects.filter(subject_identifier=subject_identifier)
        if consent:
            return consent.last().screening_identifier
        return None

    def is_consent(self, obj):
        consent_cls = django_apps.get_model('flourish_caregiver.subjectconsent')
        return isinstance(obj, consent_cls)

    def on_study(self, subject_identifier):
        caregiver_offstudy_cls = django_apps.get_model('flourish_prn.caregiveroffstudy')
        is_offstudy = caregiver_offstudy_cls.objects.filter(
            subject_identifier=subject_identifier).exists()

        return 'No' if is_offstudy else 'Yes'

    @property
    def get_model_fields(self):
        return [field for field in self.model._meta.get_fields()
                if field.name not in self.exclude_fields]

    def inline_exclude(self, field_names=[]):
        return [field_name for field_name in field_names
                if field_name not in self.exclude_fields]

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
                'clinic_verified_datetime', 'drawn_datetime', 'related_tracking_identifier',
                'parent_tracking_identifier']
