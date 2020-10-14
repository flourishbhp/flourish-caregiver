from ..models import ReferredTo
from .form_mixins import SubjectModelFormMixin


class ReferredToForm(SubjectModelFormMixin):

    class Meta:
        model = ReferredTo
        fields = '__all__'
