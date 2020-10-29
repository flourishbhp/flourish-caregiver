from django.core.exceptions import ValidationError


def validate_bpd(value):
    if value < 5 or value > 300:
        raise ValidationError(
            f'BPD has to be between 5 and 300. You entered {value}')


def validate_hc(value):
    if value < 0 or value > 600:
        raise ValidationError(
            f'HC has to be between 0 and 600. You entered {value}')


def validate_ac(value):
    if value < 5 or value > 600:
        raise ValidationError(
            f'AC has to be between 5 and 600. You entered {value}')


def validate_fl(value):
    if value < 1 or value > 200:
        raise ValidationError(
            f'FL has to be between 1 and 200. You entered {value}')


def validate_hl(value):
    if value < 1 or value > 200:
        raise ValidationError(
            f'HL has to be between 1 and 200. You entered {value}')


def validate_ga_by_ultrasound(value):
    if value < 0 or value > 40:
        raise ValidationError(
            f'GA has to be between 1 and 39. You entered {value}')


def validate_fetal_weight(value):
    if value < 1 or value > 5000:
        raise ValidationError(
            f'fetal weight has to be between 1 and 5000. You entered {value}')
