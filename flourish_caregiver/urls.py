from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import flourish_caregiver_admin

app_name = 'flourish_caregiver'

urlpatterns = [
    path('admin/', flourish_caregiver_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
]
