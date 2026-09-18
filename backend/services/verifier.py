import json
import time

from google import genai

from backend.config import GEMINI_API_KEY, GEMINI_MODEL
from backend.models.schemas import ClaimResult, Evidence


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def is_quota_or_rate_limit_error(error) -> bool:

    message = str(error).lower()

    return (
        "429" in message
        or "resource_exhausted" in message
        or "quota" in message
        or "rate limit" in message
    )


def is_temporary_service_error(error) -> bool:

    message = str(error).lower()

    return (
        "503" in message
        or "unavailable" in message
        or "high demand" in message
    )


def build_unverified_result(
    claim: str,
    evidence: list[Evidence],
    explanation: str
):

    return ClaimResult(
        claim=claim,
        verdict="UNVERIFIED",
        confidence=0.0,
        explanation=explanation,
        evidence=evidence
    )


def verify_claim(
    claim: str,
    sources: list
) -> ClaimResult:

    # ---------------------------------------------------------
    # NO SOURCES
    # ---------------------------------------------------------

    if not sources:

        return build_unverified_result(
            claim,
            [],
            (
                "No external evidence could be retrieved "
                "for this claim."
            )
        )

    # ---------------------------------------------------------
    # PREPARE EVIDENCE
    # ---------------------------------------------------------

    evidence = []

    for source in sources[:8]:

        evidence.append(
            Evidence(
                title=source.get(
                    "title",
                    ""
                ),
                url=source.get(
                    "url",
                    ""
                ),
                snippet=source.get(
                    "snippet",
                    ""
                ),
                source_domain=source.get(
                    "source_domain",
                    ""
                ),
                source_score=float(
                    source.get(
                        "source_score",
                        0.0
                    )
                )
            )
        )

    # ---------------------------------------------------------
    # CREATE EVIDENCE TEXT
    # ---------------------------------------------------------

    evidence_text = ""

    for index, item in enumerate(
        evidence,
        start=1
    ):

        evidence_text += f"""
SOURCE {index}

Title:
{item.title}

Domain:
{item.source_domain}

Source credibility score:
{item.source_score}

Evidence:
{item.snippet}

URL:
{item.url}

-----------------------------
"""

    # ---------------------------------------------------------
    # GEMINI PROMPT
    # ---------------------------------------------------------

    prompt = f"""
You are an expert fact-checking system.

Evaluate the following factual claim using ONLY
the provided evidence.

CLAIM:
{claim}

EVIDENCE:
{evidence_text}

Possible verdicts:

SUPPORTS
CONTRADICTS
MISLEADING
UNVERIFIED

Rules:

1. SUPPORTS means reliable evidence substantially
   supports the claim.

2. CONTRADICTS means reliable evidence substantially
   contradicts the claim.

3. MISLEADING means the claim contains some truth
   but omits, exaggerates, or distorts important context.

4. UNVERIFIED means there is insufficient reliable evidence.

5. Do not invent facts.

6. Do not treat a low-quality source as stronger
   than a high-quality source.

7. Prefer government organizations, universities,
   scientific organizations, major established news
   organizations, and recognized fact-checking
   organizations.

8. If evidence conflicts, explain the disagreement.

9. Base confidence on the strength and agreement
   of the available evidence.

Return ONLY valid JSON.

Do not use Markdown.

Required format:

{{
    "verdict": "SUPPORTS",
    "confidence": 0.0,
    "explanation": "Short explanation."
}}
"""

    # ---------------------------------------------------------
    # GEMINI REQUEST
    # ---------------------------------------------------------

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

    except Exception as error:

        # -----------------------------------------------------
        # 429 QUOTA
        # -----------------------------------------------------

        if is_quota_or_rate_limit_error(error):

            print(
                "Gemini quota/rate limit exhausted."
            )

            return build_unverified_result(
                claim,
                evidence,
                (
                    "The external evidence was retrieved, "
                    "but AI verification is temporarily "
                    "unavailable because the Gemini API "
                    "quota has been exhausted. "
                    "Please review the cited sources manually."
                )
            )

        # -----------------------------------------------------
        # 503 HIGH DEMAND
        # -----------------------------------------------------

        if is_temporary_service_error(error):

            print(
                "Gemini is temporarily unavailable."
            )

            return build_unverified_result(
                claim,
                evidence,
                (
                    "The external evidence was retrieved, "
                    "but the Gemini verification service "
                    "is temporarily unavailable due to "
                    "high demand. Please try again later "
                    "or review the cited sources manually."
                )
            )

        # -----------------------------------------------------
        # OTHER ERROR
        # -----------------------------------------------------

        raise

    # ---------------------------------------------------------
    # EMPTY RESPONSE
    # ---------------------------------------------------------

    if not response or not response.text:

        return build_unverified_result(
            claim,
            evidence,
            (
                "The verification service returned "
                "an empty response."
            )
        )

    content = response.text.strip()

    # ---------------------------------------------------------
    # REMOVE MARKDOWN CODE FENCES
    # ---------------------------------------------------------

    if content.startswith("```"):

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()

    # ---------------------------------------------------------
    # PARSE JSON
    # ---------------------------------------------------------

    try:

        result = json.loads(
            content
        )

        verdict = str(
            result.get(
                "verdict",
                "UNVERIFIED"
            )
        ).upper().strip()

        allowed_verdicts = {
            "SUPPORTS",
            "CONTRADICTS",
            "MISLEADING",
            "UNVERIFIED"
        }

        if verdict not in allowed_verdicts:

            verdict = "UNVERIFIED"

        confidence = float(
            result.get(
                "confidence",
                0.0
            )
        )

        confidence = max(
            0.0,
            min(
                1.0,
                confidence
            )
        )

        explanation = str(
            result.get(
                "explanation",
                "No explanation available."
            )
        )

    except (
        json.JSONDecodeError,
        TypeError,
        ValueError
    ):

        return build_unverified_result(
            claim,
            evidence,
            (
                "The verification model did not return "
                "a valid structured response."
            )
        )

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    return ClaimResult(
        claim=claim,
        verdict=verdict,
        confidence=confidence,
        explanation=explanation,
        evidence=evidence
    )