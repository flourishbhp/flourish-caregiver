from edc_identifier.subject_identifier import SubjectIdentifier


class SubjectIdentifier(SubjectIdentifier):

    template = '{protocol_number}-0{site_id}{device_id}{sequence}'
    
    def __init__(self, caregiver_type=None, **kwargs):
        if caregiver_type:
            self.template = caregiver_type + self.template
        super().__init__(**kwargs)


class PreFlourishIdentifier(SubjectIdentifier):

    template = 'PF{protocol_number}-0{site_id}{device_id}{sequence}'
