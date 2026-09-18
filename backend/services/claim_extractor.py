import json
import time

from google import genai

from backend.config import GEMINI_API_KEY, GEMINI_MODEL
from backend.models.schemas import Claim


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def extract_claims(text: str) -> list[Claim]:

    # ---------------------------------------------------------
    # STEP 1: Validate input
    # ---------------------------------------------------------

    if not text or not text.strip():

        return []

    # ---------------------------------------------------------
    # STEP 2: Gemini prompt
    # ---------------------------------------------------------

    prompt = f"""
You are an expert fact-checking assistant.

Analyze the following content.

Extract ONLY factual claims that can potentially be verified
using reliable external evidence.

Do not extract:

- opinions
- emotions
- questions
- greetings
- personal preferences
- vague statements
- predictions unless presented as factual claims

A factual claim should be a statement that can potentially
be checked against external evidence.

Return ONLY valid JSON.

Do not use Markdown.
Do not use ```json.
Do not add any text outside the JSON.

Required format:

{{
    "claims": [
        {{
            "claim": "factual claim",
            "importance": 0.9
        }}
    ]
}}

The importance value must be between 0.0 and 1.0.

CONTENT:

{text}
"""

    # ---------------------------------------------------------
    # STEP 3: Call Gemini with retry handling
    # ---------------------------------------------------------

    response = None

    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            break

        except Exception as e:

            error_message = str(e)

            # Handle temporary Gemini availability problems
            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "high demand" in error_message.lower()
            ):

                print(
                    f"Gemini temporarily unavailable "
                    f"during claim extraction. "
                    f"Retry {attempt + 1}/{max_attempts}..."
                )

                if attempt < max_attempts - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Waiting {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                continue

            # Other errors should be visible
            raise

    # ---------------------------------------------------------
    # STEP 4: Gemini still unavailable
    # ---------------------------------------------------------

    if response is None:

        print(
            "Gemini claim extraction unavailable."
        )

        return []

    # ---------------------------------------------------------
    # STEP 5: Extract Gemini response
    # ---------------------------------------------------------

    content = response.text.strip()

    # Remove Markdown code fences if Gemini adds them
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
    # STEP 6: Parse JSON
    # ---------------------------------------------------------

    try:

        data = json.loads(content)

    except json.JSONDecodeError:

        print(
            "Gemini returned invalid JSON "
            "during claim extraction."
        )

        return []

    # ---------------------------------------------------------
    # STEP 7: Convert JSON into Claim objects
    # ---------------------------------------------------------

    claims = []

    for item in data.get("claims", []):

        try:

            claim_text = str(
                item.get("claim", "")
            ).strip()

            if not claim_text:

                continue

            importance = float(
                item.get(
                    "importance",
                    1.0
                )
            )

            # Keep importance between 0 and 1
            importance = max(
                0.0,
                min(1.0, importance)
            )

            claims.append(
                Claim(
                    claim=claim_text,
                    importance=importance
                )
            )

        except (
            TypeError,
            ValueError,
            AttributeError
        ):

            continue

    return claims[:5]