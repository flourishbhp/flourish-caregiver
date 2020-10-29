from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Flourish Maternal'
    site_header = 'Flourish Maternal'
    index_title = 'Flourish Maternal'
    site_url = '/administration/'
    enable_nav_sidebar = False


flourish_maternal_admin = AdminSite(name='flourish_maternal_admin')
