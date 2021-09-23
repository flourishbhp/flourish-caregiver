import datetime
import uuid
import xlwt

from django.apps import apps as django_apps
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
        field_names.remove('_state')

        if queryset and self.is_consent(queryset[0]):
            field_names.append('previous study name')

        for col_num in range(len(field_names)):
            ws.write(row_num, col_num, field_names[col_num], font_style)

        for obj in queryset:
            obj_data = obj.__dict__
            screening_identifier = getattr(obj, 'screening_identifier', None)
            previous_study = self.previous_bhp_study(screening_identifier=screening_identifier)
            data = [obj_data[field] if field != 'previous study name' else previous_study for field in field_names]
        
            # Add subject identifier
            try:
                data.get('subject_identifier')
            except ValueError:
                try:
                    obj.subject_identifier
                except AttributeError:
                    pass
                else:
                    data.update(subject_identifier=obj.subject_identifier)
            
            try:
                data.get('visit_code')
            except ValueError:
                try:
                    obj.visit_code
                except AttributeError:
                    pass
                else:
                    data.update(visit_code=obj.visit_code)

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

    def is_consent(self, obj):
        consent_cls = django_apps.get_model('flourish_caregiver.subjectconsent')
        return isinstance(obj, consent_cls)

