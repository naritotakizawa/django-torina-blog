from django.apps import AppConfig
from django.db.models.signals import post_save


def create_default_site(sender, instance, created, raw, using, update_fields, **kwargs):
    from .models import SiteDetail
    if created:
        SiteDetail.objects.create(site=instance)


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        # Siteが追加されたときに、SiteDetailも追加する
        post_save.connect(create_default_site, sender='sites.Site')