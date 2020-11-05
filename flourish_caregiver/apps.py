from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from datetime import datetime
from dateutil.tz import gettz


class AppConfig(DjangoAppConfig):
    name = 'flourish_caregiver'
    verbose_name = 'Flourish Caregiver'
    admin_site_name = 'flourish_caregiver_admin'
    
    def ready(self):
        from .models import antenatal_enrollment_on_post_save
        from .models import pre_flourish_consent_on_post_save
        
if settings.APP_NAME == 'flourish_caregiver':
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
    from edc_visit_tracking.apps import (
        AppConfig as BaseEdcVisitTrackingAppConfig)

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'flourish_caregiver': (
                'maternal_visit', 'flourish_caregiver.maternalvisit')}

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = 'BHP132'
        protocol_number = '132'
        protocol_name = 'Flourish'
        protocol_title = ''
        study_open_datetime = datetime(
            2020, 4, 1, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2022, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        default_appt_type = 'clinic'
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='flourish_caregiver.maternalvisit')
        ]

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}


