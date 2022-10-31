from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import RelationshipFatherInvolvementFormValidator
from ..models import RelationshipFatherInvolvement


class RelationshipFatherInvolvementForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = RelationshipFatherInvolvementFormValidator
    class Meta:
        model = RelationshipFatherInvolvement
        fields = '__all__'
