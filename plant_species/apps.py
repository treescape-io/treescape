from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class PlantSpeciesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plant_species"
    verbose_name = _("Plant Species")
