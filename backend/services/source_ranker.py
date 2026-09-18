from urllib.parse import urlparse


TRUSTED_DOMAINS = {

    # ---------------------------------------------
    # Indian Government
    # ---------------------------------------------

    "gov.in": 0.98,
    "india.gov.in": 0.98,
    "pib.gov.in": 0.98,

    # ---------------------------------------------
    # US Government / Scientific Agencies
    # ---------------------------------------------

    "nasa.gov": 0.98,
    "noaa.gov": 0.98,
    "usgs.gov": 0.98,
    "cdc.gov": 0.98,
    "nih.gov": 0.97,

    # ---------------------------------------------
    # International Organizations
    # ---------------------------------------------

    "who.int": 0.98,
    "un.org": 0.97,

    # ---------------------------------------------
    # Major News Organizations
    # ---------------------------------------------

    "reuters.com": 0.94,
    "apnews.com": 0.94,

    "bbc.com": 0.92,
    "bbc.co.uk": 0.92,
    "bbcearth.com": 0.92,

    # ---------------------------------------------
    # Indian News
    # ---------------------------------------------

    "thehindu.com": 0.90,
    "indianexpress.com": 0.90,

    # ---------------------------------------------
    # Scientific / Educational
    # ---------------------------------------------

    "scientificamerican.com": 0.90,
    "britannica.com": 0.90,

    # ---------------------------------------------
    # Medical
    # ---------------------------------------------

    "mayoclinic.org": 0.94,
    "health.harvard.edu": 0.94,
    "harvard.edu": 0.94,

    "clevelandclinic.org": 0.94,
    "tuftsmedicine.org": 0.93,
    "urmc.rochester.edu": 0.93,

    # ---------------------------------------------
    # Fact Checking
    # ---------------------------------------------

    "snopes.com": 0.92,
    "politifact.com": 0.92,
    "factcheck.org": 0.92,

    # ---------------------------------------------
    # Academic / Research
    # ---------------------------------------------

    "nature.com": 0.94,
    "science.org": 0.94,

    "ncbi.nlm.nih.gov": 0.97,
    "pubmed.ncbi.nlm.nih.gov": 0.97,
}


def normalize_domain(url: str) -> str:

    try:

        domain = urlparse(
            url
        ).netloc.lower()

        if domain.startswith("www."):

            domain = domain[4:]

        return domain

    except Exception:

        return ""


def get_source_score(url: str) -> float:

    domain = normalize_domain(
        url
    )

    if not domain:

        return 0.0

    if domain in TRUSTED_DOMAINS:

        return TRUSTED_DOMAINS[
            domain
        ]

    for trusted_domain, score in (
        TRUSTED_DOMAINS.items()
    ):

        if domain.endswith(
            "." + trusted_domain
        ):

            return score

    # Unknown websites receive
    # a neutral/low credibility score.

    return 0.35


def rank_sources(results):

    ranked = []

    for result in results:

        url = result.get(
            "url",
            ""
        )

        source_domain = normalize_domain(
            url
        )

        source_score = get_source_score(
            url
        )

        updated_result = {
            **result,
            "source_domain": source_domain,
            "source_score": source_score
        }

        ranked.append(
            updated_result
        )

    ranked.sort(
        key=lambda x: x["source_score"],
        reverse=True
    )

    return ranked