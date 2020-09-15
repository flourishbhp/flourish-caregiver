from edc_identifier.subject_identifier import SubjectIdentifier


class SubjectIdentifier(SubjectIdentifier):

    template = '{protocol_number}-0{site_id}{device_id}{sequence}'
