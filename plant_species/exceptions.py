class EnrichmentException(Exception):
    pass


class SpeciesNotFound(EnrichmentException):
    pass


class SpeciesAlreadyExists(EnrichmentException):
    pass
