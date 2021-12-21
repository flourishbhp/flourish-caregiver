import datetime
import uuid

from django.apps import apps as django_apps
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import xlwt


class ExportActionMixin:

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (
            self.get_export_filename())

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws = wb.add_sheet('%s')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.num_format_str = 'YYYY/MM/DD h:mm:ss'

        field_names = queryset[0].__dict__
        field_names = [a for a in field_names.keys()]
        field_names.append('on_study')
        field_names.remove('_state')

        if queryset and self.is_consent(queryset[0]):
            field_names.append('previous_study')

        if queryset and getattr(queryset[0], 'maternal_visit', None):
            field_names.insert(0, 'subject_identifier')
            field_names.insert(1, 'study_maternal_identifier')
            field_names.insert(2, 'previous_study')
            field_names.insert(3, 'visit_code')


        for col_num in range(len(field_names)):
            ws.write(row_num, col_num, field_names[col_num], font_style)

        for obj in queryset:
            obj_data = obj.__dict__

            # Add subject identifier and visit code
            if getattr(obj, 'maternal_visit', None):
                obj_data['visit_code'] = obj.maternal_visit.visit_code
                obj_data['subject_identifier'] = obj.maternal_visit.subject_identifier
                # obj_data['on_study'] = "ONSTUDY/OFFSTUDY"

            subject_identifier = obj_data.get('subject_identifier', None)
            screening_identifier = self.screening_identifier(subject_identifier=subject_identifier)
            previous_study = self.previous_bhp_study(screening_identifier=screening_identifier)
            study_maternal_identifier = self.study_maternal_identifier(screening_identifier=screening_identifier)
            obj_data['previous_study'] = previous_study
            obj_data['study_maternal_identifier'] = study_maternal_identifier
            obj_data['on_study'] = self.on_study(subject_identifier=subject_identifier)


            data = [obj_data[field] for field in field_names]

            row_num += 1
            for col_num in range(len(data)):
                if isinstance(data[col_num], uuid.UUID):
                    ws.write(row_num, col_num, str(data[col_num]))
                elif isinstance(data[col_num], datetime.datetime):
                    data[col_num] = timezone.make_naive(data[col_num])
                    ws.write(row_num, col_num, data[col_num], xlwt.easyxf(num_format_str='YYYY/MM/DD h:mm:ss'))
                else:
                    ws.write(row_num, col_num, data[col_num])
        wb.save(response)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

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
        is_offstudy = caregiver_offstudy_cls.objects.filter(subject_identifier=subject_identifier).exists()

        return 'No' if is_offstudy else 'Yes'
