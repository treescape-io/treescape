import tempfile

from django.core.management import call_command
from django.test import TestCase

from unittest.mock import patch

from plant_species.models import Family, Genus, Species


class LoadSpeciesCommandTest(TestCase):
    @patch.object(Species, "enrich_related")
    def test_load_species(self, mock_enrich_related):
        family = Family.objects.create(latin_name="Fam", gbif_id=3)
        genus = Genus.objects.create(latin_name="Gen", family=family, gbif_id=2)

        # Use self to bring it into method context.
        self.call_counter = 0

        def enrich_side_effect(species_instance):
            species_instance.genus = genus
            species_instance.gbif_id = self.call_counter + 3
            self.call_counter += 1

        # Create a temporary file to act as our species list
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file.write("Species1\nSpecies2\nSpecies3\n")
            temp_file.seek(0)

            with patch.object(Species, "enrich", enrich_side_effect):
                call_command("load_species", filename=temp_file.name)

                self.assertEqual(self.call_counter, 3)
                self.assertTrue(mock_enrich_related.called)

        # Check that the species were added
        self.assertEqual(Species.objects.filter(latin_name="Species1").count(), 1)
        self.assertEqual(Species.objects.filter(latin_name="Species2").count(), 1)
        self.assertEqual(Species.objects.filter(latin_name="Species3").count(), 1)
