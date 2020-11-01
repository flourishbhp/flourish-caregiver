from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Flourish Caregiver'
    site_header = 'Flourish Caregiver'
    index_title = 'Flourish Caregiver'
    site_url = '/administration/'
    enable_nav_sidebar = False


flourish_caregiver_admin = AdminSite(name='flourish_caregiver_admin')
