from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class ForestDesignsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "forest_designs"
    verbose_name = _("Forest Designs")
