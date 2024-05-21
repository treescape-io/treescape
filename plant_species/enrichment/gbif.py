import typing
import pycountry

from pygbif import occurrences, species

_valid_licenses = (
    # CC-BY
    "http://creativecommons.org/licenses/by/4.0/legalcode",
    "http://creativecommons.org/licenses/by/4.0/",
    "https://creativecommons.org/licenses/by/4.0/deed.en",
    # CC0
    "http://creativecommons.org/publicdomain/zero/1.0/legalcode",
    "http://creativecommons.org/publicdomain/zero/1.0/",
    # CC-BY-SA
    "http://creativecommons.org/licenses/by-sa/4.0/",
)


def _get_image_url(occurrence: dict) -> str | None:
    for media in occurrence.get("media", []):
        if (
            media.get("type") == "StillImage"
            and media.get("license") in _valid_licenses
        ):
            return media.get("identifier")

    return None


def get_image_urls(taxonKey: int) -> typing.List[str]:
    """Get URL of CC licensed images."""
    occurrence_data = occurrences.search(
        taxonKey, mediatype="StillImage", basisOfRecord="HUMAN_OBSERVATION"
    )
    """ Returns something like this:
    {
      "offset":0,
      "limit":2,
      "endOfRecords":false,
      "count":238684,
      "results":[
        {
          "key":4509146329,
          "datasetKey":"963a6b96-4d22-4428-86e4-afee52cf4a8e",
          "publishingOrgKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
          "installationKey":"f9c0c41b-6da4-4be4-b917-a6f7710f3dbc",
          "hostingOrganizationKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
          "publishingCountry":"DK",
          "protocol":"DWC_ARCHIVE",
          "lastCrawled":"2024-04-06T10:26:45.524+00:00",
          "lastParsed":"2024-04-06T10:31:30.950+00:00",
          "crawlId":204,
          "extensions":{
            "http://rs.gbif.org/terms/1.0/Multimedia":[
              {
                "http://purl.org/dc/terms/identifier":"https://arter.dk/media/9bf952d1-e004-4a52-bd0f-b0f000e00f61.jpg",
                "http://purl.org/dc/terms/type":"Image",
                "http://purl.org/dc/terms/license":"https://creativecommons.org/licenses/by/4.0/"
              }
            ]
          },
          "basisOfRecord":"HUMAN_OBSERVATION",
          "occurrenceStatus":"PRESENT",
          "taxonKey":5231190,
          "kingdomKey":1,
          "phylumKey":44,
          "classKey":212,
          "orderKey":729,
          "familyKey":5264,
          "genusKey":2492321,
          "speciesKey":5231190,
          "acceptedTaxonKey":5231190,
          "scientificName":"Passer domesticus (Linnaeus, 1758)",
          "acceptedScientificName":"Passer domesticus (Linnaeus, 1758)",
          "kingdom":"Animalia",
          "phylum":"Chordata",
          "order":"Passeriformes",
          "family":"Passeridae",
          "genus":"Passer",
          "species":"Passer domesticus",
          "genericName":"Passer",
          "specificEpithet":"domesticus",
          "taxonRank":"SPECIES",
          "taxonomicStatus":"ACCEPTED",
          "iucnRedListCategory":"LC",
          "decimalLatitude":55.149119,
          "decimalLongitude":12.009073,
          "coordinateUncertaintyInMeters":10.21,
          "continent":"EUROPE",
          "gadm":{
            "level0":{
              "gid":"DNK",
              "name":"Denmark"
            },
            "level1":{
              "gid":"DNK.4_1",
              "name":"Sjælland"
            },
            "level2":{
              "gid":"DNK.4.9_1",
              "name":"Næstved"
            }
          },
          "year":2024,
          "month":1,
          "day":7,
          "eventDate":"2024-01-07",
          "startDayOfYear":7,
          "endDayOfYear":7,
          "issues":[
            "COORDINATE_ROUNDED",
            "CONTINENT_DERIVED_FROM_COORDINATES",
            "TAXON_MATCH_TAXON_ID_IGNORED"
          ],
          "modified":"2024-01-07T17:31:30.725+00:00",
          "lastInterpreted":"2024-04-06T10:31:30.950+00:00",
          "license":"http://creativecommons.org/licenses/by/4.0/legalcode",
          "isSequenced":false,
          "identifiers":[
            {
              "identifier":"0e098265-8adb-4189-b7e0-b0f000e0100d"
            }
          ],
          "media":[
            {
              "type":"StillImage",
              "license":"http://creativecommons.org/licenses/by/4.0/",
              "identifier":"https://arter.dk/media/9bf952d1-e004-4a52-bd0f-b0f000e00f61.jpg"
            }
          ],
          "facts":[

          ],
          "relations":[

          ],
          "isInCluster":false,
          "recordedBy":"Eddie Bach",
          "identifiedBy":"Eddie Bach",
          "geodeticDatum":"WGS84",
          "class":"Aves",
          "countryCode":"DK",
          "recordedByIDs":[

          ],
          "identifiedByIDs":[

          ],
          "gbifRegion":"EUROPE",
          "country":"Denmark",
          "publishedByGbifRegion":"EUROPE",
          "identifier":"0e098265-8adb-4189-b7e0-b0f000e0100d",
          "catalogNumber":"Arter_0e098265-8adb-4189-b7e0-b0f000e0100d",
          "vernacularName":"Gråspurv",
          "institutionCode":"MST-and-NHMD",
          "dynamicProperties":"{\"Substrate\":\"\"}",
          "eventTime":"14:34:53.268+01:00",
          "gbifID":"4509146329",
          "language":"da",
          "occurrenceID":"https://arter.dk/observation/record-details/0e098265-8adb-4189-b7e0-b0f000e0100d",
          "bibliographicCitation":"Arter.dk Miljøstyrelsen",
          "taxonID":"MSTSNM:Arter:5ebbe02c-52b5-4560-afe2-abc800da0560"
        },
        {
          "key":4509144335,
          "datasetKey":"963a6b96-4d22-4428-86e4-afee52cf4a8e",
          "publishingOrgKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
          "installationKey":"f9c0c41b-6da4-4be4-b917-a6f7710f3dbc",
          "hostingOrganizationKey":"1a4e6112-b3af-402e-b29f-c2ade2167f72",
          "publishingCountry":"DK",
          "protocol":"DWC_ARCHIVE",
          "lastCrawled":"2024-04-06T10:26:45.524+00:00",
          "lastParsed":"2024-04-06T10:31:33.086+00:00",
          "crawlId":204,
          "extensions":{
            "http://rs.gbif.org/terms/1.0/Multimedia":[
              {
                "http://purl.org/dc/terms/identifier":"https://arter.dk/media/5af3c382-9771-4f86-b2bb-b0f300eea47f.jpg",
                "http://purl.org/dc/terms/type":"Image",
                "http://purl.org/dc/terms/license":"https://creativecommons.org/licenses/by/4.0/"
              }
            ]
          },
          "basisOfRecord":"HUMAN_OBSERVATION",
          "occurrenceStatus":"PRESENT",
          "taxonKey":5231190,
          "kingdomKey":1,
          "phylumKey":44,
          "classKey":212,
          "orderKey":729,
          "familyKey":5264,
          "genusKey":2492321,
          "speciesKey":5231190,
          "acceptedTaxonKey":5231190,
          "scientificName":"Passer domesticus (Linnaeus, 1758)",
          "acceptedScientificName":"Passer domesticus (Linnaeus, 1758)",
          "kingdom":"Animalia",
          "phylum":"Chordata",
          "order":"Passeriformes",
          "family":"Passeridae",
          "genus":"Passer",
          "species":"Passer domesticus",
          "genericName":"Passer",
          "specificEpithet":"domesticus",
          "taxonRank":"SPECIES",
          "taxonomicStatus":"ACCEPTED",
          "iucnRedListCategory":"LC",
          "decimalLatitude":54.764569,
          "decimalLongitude":11.867456,
          "coordinateUncertaintyInMeters":18.5,
          "continent":"EUROPE",
          "gadm":{
            "level0":{
              "gid":"DNK",
              "name":"Denmark"
            },
            "level1":{
              "gid":"DNK.4_1",
              "name":"Sjælland"
            },
            "level2":{
              "gid":"DNK.4.3_1",
              "name":"Guldborgsund"
            }
          },
          "year":2024,
          "month":1,
          "day":10,
          "eventDate":"2024-01-10",
          "startDayOfYear":10,
          "endDayOfYear":10,
          "issues":[
            "COORDINATE_ROUNDED",
            "CONTINENT_DERIVED_FROM_COORDINATES",
            "TAXON_MATCH_TAXON_ID_IGNORED"
          ],
          "modified":"2024-01-11T14:27:37.300+00:00",
          "lastInterpreted":"2024-04-06T10:31:33.086+00:00",
          "license":"http://creativecommons.org/licenses/by/4.0/legalcode",
          "isSequenced":false,
          "identifiers":[
            {
              "identifier":"15ef9233-6298-44cc-9884-b0f300eea4f1"
            }
          ],
          "media":[
            {
              "type":"StillImage",
              "license":"http://creativecommons.org/licenses/by/4.0/",
              "identifier":"https://arter.dk/media/5af3c382-9771-4f86-b2bb-b0f300eea47f.jpg"
            }
          ],
          "facts":[

          ],
          "relations":[

          ],
          "isInCluster":false,
          "recordedBy":"Aske Keiser-Nielsen",
          "identifiedBy":"Aske Keiser-Nielsen",
          "geodeticDatum":"WGS84",
          "class":"Aves",
          "countryCode":"DK",
          "recordedByIDs":[

          ],
          "identifiedByIDs":[

          ],
          "gbifRegion":"EUROPE",
          "country":"Denmark",
          "publishedByGbifRegion":"EUROPE",
          "identifier":"15ef9233-6298-44cc-9884-b0f300eea4f1",
          "catalogNumber":"Arter_15ef9233-6298-44cc-9884-b0f300eea4f1",
          "vernacularName":"Gråspurv",
          "institutionCode":"MST-and-NHMD",
          "dynamicProperties":"{\"Substrate\":\"\"}",
          "eventTime":"15:28:07.796+01:00",
          "gbifID":"4509144335",
          "language":"da",
          "occurrenceID":"https://arter.dk/observation/record-details/15ef9233-6298-44cc-9884-b0f300eea4f1",
          "bibliographicCitation":"Arter.dk Miljøstyrelsen",
          "taxonID":"MSTSNM:Arter:5ebbe02c-52b5-4560-afe2-abc800da0560"
        }
      ],
      "facets":[

      ]
    }
    """
    results = occurrence_data["results"]
    assert isinstance(results, list)

    return [url for url in map(_get_image_url, results) if url is not None]


def _convert_language_code(alpha_3):
    """Convert ISO 639-2 code to ISO 639-1 using pycountry."""

    assert alpha_3
    country = pycountry.languages.get(alpha_3=alpha_3)
    assert country

    return country.alpha_2


def get_common_names(
    gbif_id: int, enabled_languages: typing.List[str]
) -> typing.List[typing.Dict[str, str]]:
    """Fetch common names from GBIF for the given gbif_id and return them as a list of dictionaries."""
    names_data = species.name_usage(gbif_id, data="vernacularNames")
    assert isinstance(names_data, dict)
    results = names_data["results"]
    assert isinstance(results, list)

    common_names = []
    for name_data in results:
        assert isinstance(name_data, dict)
        assert "language" in name_data
        assert "vernacularName" in name_data and name_data["vernacularName"]

        if not name_data["language"]:
            continue

        alpha2_lang = _convert_language_code(name_data["language"])
        assert alpha2_lang

        if alpha2_lang in enabled_languages:
            common_names.append(
                {"language": alpha2_lang, "name": name_data["vernacularName"]}
            )

    return common_names
