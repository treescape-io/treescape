from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class SpeciesDataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "species_data"
    verbose_name = _("Species Data")
