from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.core.files.base import ContentFile

from plant_species.enrichment import gbif, wikipedia


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
        self.assertEqual(gbif._get_image_urls(12345), expected_urls)

    @patch("plant_species.enrichment.gbif._get_image_urls")
    @patch("requests.get")
    def test_get_image(self, mock_get, mock_get_image_urls):
        # Mock the _get_image_urls to return a list of image URLs
        mock_get_image_urls.return_value = ["http://example.com/image.jpg"]

        # Mock the requests.get to return a response with image content
        mock_response = MagicMock()
        mock_response.__enter__.return_value.headers = {"Content-Type": "image/jpeg"}
        mock_response.__enter__.return_value.content = b"image content"
        mock_get.return_value = mock_response

        # Call the get_image function
        result = gbif.get_image(12345)

        # Assert that the result is a ContentFile with the expected content
        assert isinstance(result, ContentFile)
        self.assertEqual(result.read(), b"image content")

    @patch("plant_species.enrichment.gbif._get_image_urls")
    @patch("requests.get")
    def test_get_image_no_valid_images(self, mock_get, mock_get_image_urls):
        # Mock the _get_image_urls to return a list of image URLs
        mock_get_image_urls.return_value = ["http://example.com/image.png"]

        # Mock the requests.get to return a response with non-JPEG content
        mock_response = MagicMock()
        mock_response.headers = {"Content-Type": "image/png"}
        mock_response.content = b"image content"
        mock_get.return_value = mock_response

        # Call the get_image function
        result = gbif.get_image(12345)

        # Assert that the result is None since no valid JPEG images were found
        self.assertIsNone(result)
        self.assertEqual(gbif._convert_language_code("eng"), "en")
        self.assertEqual(gbif._convert_language_code("fra"), "fr")
        self.assertEqual(gbif._convert_language_code("deu"), "de")

    @patch("plant_species.enrichment.gbif.species.name_usage")
    def test_get_common_names(self, mock_name_usage):
        mock_name_usage.return_value = {
            "results": [
                {"language": "eng", "vernacularName": "House Sparrow"},
                {"language": "fra", "vernacularName": "Moineau domestique"},
                {"language": "deu", "vernacularName": "Haussperling"},
                {"language": "spa", "vernacularName": "Gorrión común"},
            ]
        }

        enabled_languages = ["en", "fr", "de"]
        expected_common_names = [
            {"language": "en", "name": "House Sparrow"},
            {"language": "fr", "name": "Moineau domestique"},
            {"language": "de", "name": "Haussperling"},
        ]

        self.assertEqual(
            gbif.get_common_names(12345, enabled_languages), expected_common_names
        )


class WikipediaTestCase(TestCase):
    @patch("plant_species.enrichment.wikipedia.wikipedia.page")
    def test_get_wikipedia_page_success(self, mock_page):
        mock_page.return_value = MagicMock(title="Test Page")
        page = wikipedia.get_wikipedia_page("Test Page")
        assert page
        self.assertEqual(page.title, "Test Page")

    @patch("plant_species.enrichment.wikipedia.wikipedia.page")
    def test_get_wikipedia_page_failure(self, mock_page):
        mock_page.side_effect = wikipedia.wikipedia.PageError(pageid=18630637)
        page = wikipedia.get_wikipedia_page("Test Page")
        self.assertIsNone(page)
