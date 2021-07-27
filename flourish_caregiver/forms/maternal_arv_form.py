from ..models import MaternalArv
from .form_mixins import InlineSubjectModelFormMixin


class MaternalArvForm(InlineSubjectModelFormMixin):

    # form_validator_cls = MaternalArvFormValidator

    class Meta:
        model = MaternalArv
        fields = '__all__'
