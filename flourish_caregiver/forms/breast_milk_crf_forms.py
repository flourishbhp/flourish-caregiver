from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from edc_constants.constants import NO

from flourish_form_validations.form_validators import BreastMilkCRFFormValidator
from flourish_form_validations.form_validators.breast_milk_crf_form_validator import \
    CrackedNipplesInlineFormValidator, MastitisInlineFormValidator
from .form_mixins import InlineSubjectModelFormMixin, SubjectModelFormMixin
from ..choices import EXP_COUNT_CHOICES_NONE, YES_NO_NONE, YES_RESOLVED_NO
from ..models.breast_milk_crfs import BreastMilk6Months, BreastMilkBirth, \
    CrackedNipplesInline, MastitisInline


class BreastMilkBirthFormsMixin(forms.ModelForm):

    def clean(self):
        super().clean()
        mastitis_inline_count = int(self.data.get('mastitisinline_set-TOTAL_FORMS'))
        cracked_nipples_inline_count = int(
            self.data.get('crackednipplesinline_set-TOTAL_FORMS'))
        exp_mastitis_count = self.cleaned_data.get('exp_mastitis_count', '')
        exp_cracked_nipples_count = self.cleaned_data.get('exp_cracked_nipples_count', '')

        self._validate_count(mastitis_inline_count, exp_mastitis_count, 'Mastitis')
        self._validate_count(cracked_nipples_inline_count, exp_cracked_nipples_count,
                             'Cracked Nipples')

        self._validate_mastitis_actions(mastitis_inline_count)
        self._validate_cracked_nipples_actions(cracked_nipples_inline_count)

        exp_mastitis = self.cleaned_data.get('exp_mastitis')
        exp_cracked_nipples = self.cleaned_data.get('exp_cracked_nipples')
        milk_collected = self.cleaned_data.get('milk_collected')

        if not exp_cracked_nipples and exp_mastitis == NO:
            raise ValidationError(
                {'exp_cracked_nipples': 'This field is required'}
            )

        if not milk_collected and exp_cracked_nipples == NO:
            raise ValidationError(
                {'milk_collected': 'This field is required'}
            )

    def _validate_count(self, inline_count, exp_count, field_name):
        if exp_count:
            exp_count = exp_count.split('_')[0]
            if inline_count != int(exp_count):
                raise ValidationError(
                    {f'exp_{field_name.lower()}_count': f'Ensure that you have the same '
                                                        f'number of {field_name} inlines'}
                )
        elif inline_count > 0:
            raise ValidationError(f'{field_name} inlines are not required')

    def _validate_mastitis_actions(self, mastitis_inline_count):
        exp_cracked_nipples = self.cleaned_data.get('exp_cracked_nipples')
        for x in range(0, mastitis_inline_count):
            if x < (mastitis_inline_count - 1):
                mastitis_actions = self.data.get(
                    f'mastitisinline_set-{x}-mastitis_action')
                if str(self._get_mastitis_action.id) in mastitis_actions:
                    raise ValidationError(
                        'If there are multiple Instances of Mastitis Inlines ensure '
                        'that only on the last Inline the option \'Stopped '
                        'breastfeeding\' is selected')
            if x == (mastitis_inline_count - 1):
                mastitis_actions = self.data.get(
                    f'mastitisinline_set-{x}-mastitis_action')
                if (self.cleaned_data.get('exp_cracked_nipples') and str(
                        self._get_mastitis_action.id) in mastitis_actions):
                    raise ValidationError(
                        {'exp_cracked_nipples': 'This field is not required'})
                elif not exp_cracked_nipples:
                    raise ValidationError(
                        {'exp_cracked_nipples': 'This field is required'}
                    )
                if (self.cleaned_data.get('milk_collected') and str(
                        self._get_mastitis_action.id) in mastitis_actions):
                    raise ValidationError(
                        {'milk_collected': 'This field is not required'})

    def _validate_cracked_nipples_actions(self, cracked_nipples_inline_count):
        milk_collected = self.cleaned_data.get('milk_collected')
        for x in range(0, cracked_nipples_inline_count):
            if x < (cracked_nipples_inline_count - 1):
                cracked_nipples_actions = self.data.get(
                    f'crackednipplesinline_set-{x}-cracked_nipples_action')
                if str(self._get_cracked_nipples_action.id) in cracked_nipples_actions:
                    raise ValidationError(
                        'If there are multiple Instances of Cracked Nipples ensure that '
                        'only on the last Inline the option \'Stopped breastfeeding\' '
                        'is selected')
            if x == (cracked_nipples_inline_count - 1):
                cracked_nipples_actions = self.data.get(
                    f'crackednipplesinline_set-{x}-cracked_nipples_action')
                if (self.cleaned_data.get('milk_collected') and str(
                        self._get_cracked_nipples_action.id) in
                        cracked_nipples_actions):
                    raise ValidationError(
                        {'milk_collected': 'This field is not required'})
                elif not milk_collected:
                    raise ValidationError(
                        {'milk_collected': 'This field is required'}
                    )

    @property
    def _get_cracked_nipples_action(self):
        return self._get_action(
            django_apps.get_model('flourish_caregiver.crackednipplesactions'),
        )

    @property
    def _get_mastitis_action(self):
        return self._get_action(
            django_apps.get_model('flourish_caregiver.mastitisactions'),
        )

    def _get_action(self, model_cls):
        short_name = 'stopped_breastfeeding'
        try:
            return model_cls.objects.get(short_name=short_name)
        except ObjectDoesNotExist:
            return None


class BreastMilkBirthForms(BreastMilkBirthFormsMixin, SubjectModelFormMixin,
                           forms.ModelForm):
    form_validator_cls = BreastMilkCRFFormValidator
    exp_mastitis = forms.ChoiceField(
        label='Since the mother started breastfeeding, has she experienced mastitis?',
        choices=YES_RESOLVED_NO,
        widget=forms.RadioSelect,
    )
    exp_mastitis_count = forms.ChoiceField(
        label='How many times has the participant experienced mastitis?',
        choices=EXP_COUNT_CHOICES_NONE,
        widget=forms.RadioSelect,
        required=False
    )
    exp_cracked_nipples = forms.ChoiceField(
        label='Has the participant experienced cracked nipples?',
        choices=YES_NO_NONE,
        widget=forms.RadioSelect,
        required=False,
    )

    class Meta:
        model = BreastMilkBirth
        fields = '__all__'


class BreastMilk6MonthsForms(BreastMilkBirthFormsMixin, SubjectModelFormMixin,
                             forms.ModelForm):
    form_validator_cls = BreastMilkCRFFormValidator

    class Meta:
        model = BreastMilk6Months
        fields = '__all__'


class MastitisInlineForm(InlineSubjectModelFormMixin):
    form_validator_cls = MastitisInlineFormValidator

    def has_changed(self):
        return True

    def clean(self):
        breast_milk_crf = self.cleaned_data.get('breast_milk_crf')
        maternal_visit = breast_milk_crf.maternal_visit
        self.cleaned_data['maternal_visit'] = maternal_visit
        super().clean()

    class Meta:
        model = MastitisInline
        fields = '__all__'


class CrackedNipplesInlineForm(InlineSubjectModelFormMixin):
    form_validator_cls = CrackedNipplesInlineFormValidator

    def has_changed(self):
        return True

    def clean(self):
        breast_milk_crf = self.cleaned_data.get('breast_milk_crf')
        maternal_visit = breast_milk_crf.maternal_visit
        self.cleaned_data['maternal_visit'] = maternal_visit
        super().clean()

    class Meta:
        model = CrackedNipplesInline
        fields = '__all__'
