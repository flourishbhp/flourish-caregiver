from ..models import SocioDemographicData
from .form_mixins import SubjectModelFormMixin


class SocioDemographicDataForm(SubjectModelFormMixin):

    class Meta:
        model = SocioDemographicData
        fields = '__all__'
