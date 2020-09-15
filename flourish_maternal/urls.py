from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import flourish_maternal_admin

app_name = 'flourish_maternal'

urlpatterns = [
    path('admin/', flourish_maternal_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
]
