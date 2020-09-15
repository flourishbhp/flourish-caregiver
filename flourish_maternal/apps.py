from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'flourish_maternal'
    verbose_name = 'Flourish Maternal'
    admin_site_name = 'flourish_maternal'
