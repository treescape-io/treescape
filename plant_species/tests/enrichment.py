from django.test import TestCase
from unittest.mock import patch

from plant_species.enrichment import gbif


class GBIFTestCase(TestCase):
    def test_get_image_url(self):
        occurrence_with_valid_license = {
            "media": [
                {
                    "type": "StillImage",
                    "license": "http://creativecommons.org/licenses/by/4.0/",
                    "identifier": "https://example.com/image1.jpg",
                }
            ]
        }
        occurrence_with_invalid_license = {
            "media": [
                {
                    "type": "StillImage",
                    "license": "http://invalid.license/",
                    "identifier": "https://example.com/image2.jpg",
                }
            ]
        }
        occurrence_without_media = {}

        self.assertEqual(
            gbif._get_image_url(occurrence_with_valid_license),
            "https://example.com/image1.jpg",
        )
        self.assertIsNone(gbif._get_image_url(occurrence_with_invalid_license))
        self.assertIsNone(gbif._get_image_url(occurrence_without_media))

    @patch("plant_species.enrichment.gbif.occurrences.search")
    def test_get_image_urls(self, mock_search):
        mock_search.return_value = {
            "results": [
                {
                    "media": [
                        {
                            "type": "StillImage",
                            "license": "http://creativecommons.org/licenses/by/4.0/",
                            "identifier": "https://example.com/image1.jpg",
                        }
                    ]
                },
                {
                    "media": [
                        {
                            "type": "StillImage",
                            "license": "http://invalid.license/",
                            "identifier": "https://example.com/image2.jpg",
                        }
                    ]
                },
                {"media": []},
            ]
        }

        expected_urls = ["https://example.com/image1.jpg"]
        self.assertEqual(gbif.get_image_urls(12345), expected_urls)
