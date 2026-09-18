import trafilatura

from backend.services.claim_extractor import extract_claims
from backend.services.web_search import search_web
from backend.services.source_ranker import rank_sources
from backend.services.verifier import verify_claim


def extract_article(url: str) -> str:

    downloaded = trafilatura.fetch_url(url)

    if not downloaded:
        raise ValueError(
            "Could not download the article."
        )

    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False
    )

    if not text:
        raise ValueError(
            "Could not extract readable article text."
        )

    return text


def calculate_overall_result(results):

    if not results:
        return "UNVERIFIED", 0.0

    scores = []

    for result in results:

        verdict = result.verdict

        confidence = max(
            0.0,
            min(
                1.0,
                float(result.confidence)
            )
        )

        # -------------------------------------------------
        # Only verified claims influence the final verdict.
        # UNVERIFIED claims are ignored.
        # -------------------------------------------------

        if verdict == "SUPPORTS":

            scores.append(
                confidence
            )

        elif verdict == "CONTRADICTS":

            scores.append(
                -confidence
            )

        elif verdict == "MISLEADING":

            scores.append(
                -0.25 * confidence
            )

        # UNVERIFIED:
        # Do not add anything.

    # -----------------------------------------------------
    # No verified claims
    # -----------------------------------------------------

    if not scores:

        return "UNVERIFIED", 0.0

    # -----------------------------------------------------
    # Average verified evidence
    # -----------------------------------------------------

    final_score = (
        sum(scores)
        / len(scores)
    )

    confidence = min(
        1.0,
        abs(final_score)
    )

    # -----------------------------------------------------
    # FINAL VERDICT
    # -----------------------------------------------------

    if final_score >= 0.50:

        verdict = "LIKELY TRUE"

    elif final_score <= -0.50:

        verdict = "LIKELY FALSE"

    elif final_score <= -0.15:

        verdict = "MISLEADING"

    elif final_score >= 0.15:

        verdict = "LIKELY TRUE"

    else:

        verdict = "UNVERIFIED"

    return verdict, confidence

def verify_content(
    text: str = None,
    url: str = None
):

    if url:

        text = extract_article(url)

    if not text:

        raise ValueError(
            "Either text or URL is required."
        )

    claims = extract_claims(text)

    if not claims:

        return {
            "input_text": text,
            "overall_verdict": "UNVERIFIED",
            "overall_confidence": 0.0,
            "claims": []
        }

    claim_results = []

    for claim in claims:

        search_results = search_web(
            claim.claim,
            max_results=10
        )

        ranked_sources = rank_sources(
            search_results
        )

        result = verify_claim(
            claim.claim,
            ranked_sources
        )

        claim_results.append(result)

    overall_verdict, overall_confidence = (
        calculate_overall_result(
            claim_results
        )
    )

    return {
        "input_text": text,
        "overall_verdict": overall_verdict,
        "overall_confidence": overall_confidence,
        "claims": claim_results
    }