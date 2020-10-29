from django.urls.conf import path
from django.views.generic.base import RedirectView

from flourish_caregiver import flourish_maternal_admin

app_name = 'flourish_caregiver'

urlpatterns = [
    path('admin/', flourish_maternal_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
]
