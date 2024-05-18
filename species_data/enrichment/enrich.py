import pprint

from plant_species.models import Species
from .chains import get_enrichment_chain


def enrich_species_data(species: Species):
    """Retrieves and stores additional data about a plant species using a language model."""
    chain = get_enrichment_chain()
    assert species.wikipedia_page
    plant_data = chain.invoke(
        {
            "source_content": species.wikipedia_page.content,
            "latin_name": species.latin_name,
        }
    )
    pprint.pprint(plant_data)

    # TODO:
    # 1. Auto-generated slugs for all multi-select models.
    # 2. Idempotently save generated data to models.
    # 3. Fixture/data migration for Source Type.
    # 4. Citations for source.
    # 5. Set source for created data.
    # 6. Dynamic prompting without source.
    # 7. Source type confidence.
    # 8. Add additional sources, confidence-based trumping:
    #     - a) USDA
    #     - b) GBIF description
    #     - c) Trefle
    #
