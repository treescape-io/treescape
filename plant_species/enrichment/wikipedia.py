import wikipedia


def get_wikipedia_page(name: str) -> wikipedia.WikipediaPage | None:
    try:
        return wikipedia.page(title=name, redirect=True)
    except (wikipedia.PageError, wikipedia.DisambiguationError):
        return None
