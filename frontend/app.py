import os
import requests
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TruthLens AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BACKEND CONFIGURATION
# =========================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# =========================================================
# SESSION STATE
# =========================================================

if "verification_result" not in st.session_state:
    st.session_state.verification_result = None

if "verification_type" not in st.session_state:
    st.session_state.verification_type = None


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .truthlens-header {
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(128,128,128,0.25);
        }

        .verdict-box {
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.25);
            margin-bottom: 1rem;
        }

        .claim-box {
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.20);
            margin-bottom: 1rem;
        }

        .evidence-box {
            padding: 0.8rem;
            border-radius: 10px;
            border: 1px solid rgba(128,128,128,0.15);
            margin-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="truthlens-header">
        <h1>🔎 TruthLens AI</h1>
        <h3>AI-Powered Misinformation & Fact Verification System</h3>
        <p>
            Analyze claims, search external evidence, rank sources,
            and evaluate whether claims are supported, contradicted,
            misleading, or unverified.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🧠 About TruthLens")

    st.write(
        """
        TruthLens AI is an evidence-based misinformation
        verification prototype.
        """
    )

    st.markdown("### Verification Pipeline")

    st.write("1. 📝 Extract factual claims")
    st.write("2. 🌐 Search the web for evidence")
    st.write("3. 🏆 Rank source credibility")
    st.write("4. 🤖 Verify claims using Gemini")
    st.write("5. 📊 Generate an overall verdict")

    st.divider()

    st.caption("Backend")
    st.code(BACKEND_URL)

    if st.button("🔄 Clear Results", use_container_width=True):
        st.session_state.verification_result = None
        st.session_state.verification_type = None
        st.rerun()


# =========================================================
# BACKEND HEALTH CHECK
# =========================================================

with st.sidebar:

    try:
        health_response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=10
        )

        if health_response.status_code == 200:
            st.success("🟢 Backend Online")
        else:
            st.warning("🟡 Backend Responding")
    except requests.RequestException:
        st.error("🔴 Backend Offline")


# =========================================================
# VERIFICATION FUNCTIONS
# =========================================================

def verify_text(text: str):
    """Send text to the FastAPI backend."""

    response = requests.post(
        f"{BACKEND_URL}/api/v1/verify",
        json={
            "text": text
        },
        timeout=180
    )

    return response


def verify_url(url: str):
    """Send URL to the FastAPI backend."""

    response = requests.post(
        f"{BACKEND_URL}/api/v1/verify",
        json={
            "url": url
        },
        timeout=180
    )

    return response


# =========================================================
# INPUT TABS
# =========================================================

text_tab, url_tab = st.tabs(
    [
        "📝 Verify Text",
        "🌐 Verify Article URL"
    ]
)


# =========================================================
# TEXT VERIFICATION
# =========================================================

with text_tab:

    st.subheader("Verify Text")

    text_input = st.text_area(
        "Enter a claim or text to analyze",
        height=220,
        placeholder=(
            "Example:\n\n"
            "The Earth is flat and NASA has admitted that "
            "the planet is not spherical."
        )
    )

    verify_text_button = st.button(
        "🔍 Verify Text",
        type="primary",
        use_container_width=True
    )

    if verify_text_button:

        if not text_input.strip():

            st.warning(
                "Please enter some text before starting verification."
            )

        else:

            with st.spinner(
                "Analyzing claims, searching evidence, and verifying..."
            ):

                try:

                    response = verify_text(
                        text_input.strip()
                    )

                    if response.status_code == 200:

                        st.session_state.verification_result = (
                            response.json()
                        )

                        st.session_state.verification_type = "text"

                        st.success(
                            "Verification completed successfully."
                        )

                    elif response.status_code == 429:

                        st.warning(
                            "Gemini API quota is currently exhausted. "
                            "Please try again after the quota resets."
                        )

                    else:

                        try:
                            detail = response.json().get(
                                "detail",
                                response.text
                            )
                        except Exception:
                            detail = response.text

                        st.error(
                            f"Verification failed: {detail}"
                        )

                except requests.Timeout:

                    st.error(
                        "The verification request timed out. "
                        "The backend may still be processing the request. "
                        "Please try again."
                    )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to the backend: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Unexpected error: {e}"
                    )


# =========================================================
# URL VERIFICATION
# =========================================================

with url_tab:

    st.subheader("Verify an Article URL")

    url_input = st.text_input(
        "Article URL",
        placeholder="https://example.com/article"
    )

    verify_url_button = st.button(
        "🌐 Verify Article",
        type="primary",
        use_container_width=True
    )

    if verify_url_button:

        if not url_input.strip():

            st.warning(
                "Please enter an article URL."
            )

        else:

            with st.spinner(
                "Extracting article, searching evidence, and verifying..."
            ):

                try:

                    response = verify_url(
                        url_input.strip()
                    )

                    if response.status_code == 200:

                        st.session_state.verification_result = (
                            response.json()
                        )

                        st.session_state.verification_type = "url"

                        st.success(
                            "Article verification completed successfully."
                        )

                    elif response.status_code == 429:

                        st.warning(
                            "Gemini API quota is currently exhausted. "
                            "Please try again after the quota resets."
                        )

                    else:

                        try:
                            detail = response.json().get(
                                "detail",
                                response.text
                            )
                        except Exception:
                            detail = response.text

                        st.error(
                            f"URL verification failed: {detail}"
                        )

                except requests.Timeout:

                    st.error(
                        "The verification request timed out. "
                        "Please try again."
                    )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to the backend: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Unexpected error: {e}"
                    )


# =========================================================
# GET RESULT
# =========================================================

result = st.session_state.get(
    "verification_result"
)


# =========================================================
# DISPLAY RESULT
# =========================================================

if result:

    st.divider()

    st.header("📊 Verification Result")

    # -----------------------------------------------------
    # OVERALL RESULT
    # -----------------------------------------------------

    overall_verdict = result.get(
        "overall_verdict",
        "UNVERIFIED"
    )

    overall_confidence = float(
        result.get(
            "overall_confidence",
            0.0
        )
    )

    claims = result.get(
        "claims",
        []
    )

    # -----------------------------------------------------
    # OVERALL VERDICT CONFIGURATION
    # -----------------------------------------------------

    verdict_config = {

        "LIKELY TRUE": {
            "emoji": "✅",
            "label": "LIKELY TRUE"
        },

        "LIKELY FALSE": {
            "emoji": "❌",
            "label": "LIKELY FALSE"
        },

        "MISLEADING": {
            "emoji": "⚠️",
            "label": "MISLEADING"
        },

        "UNVERIFIED": {
            "emoji": "❓",
            "label": "UNVERIFIED"
        }
    }

    config = verdict_config.get(
        overall_verdict,
        {
            "emoji": "❓",
            "label": overall_verdict
        }
    )

    # -----------------------------------------------------
    # OVERALL RESULT CARD
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Overall Verdict",
            f"{config['emoji']} {config['label']}"
        )

    with col2:

        st.metric(
            "Confidence",
            f"{overall_confidence * 100:.1f}%"
        )

    with col3:

        st.metric(
            "Claims Detected",
            len(claims)
        )

    st.progress(
        min(max(overall_confidence, 0.0), 1.0)
    )

    # -----------------------------------------------------
    # CLAIMS
    # -----------------------------------------------------

    st.subheader("📝 Claims Detected")

    if not claims:

        st.info(
            "No verifiable factual claims were detected."
        )

    else:

        for index, claim_result in enumerate(
            claims,
            start=1
        ):

            # -------------------------------------------------
            # SUPPORT BOTH DICT AND OBJECT RESPONSES
            # -------------------------------------------------

            if isinstance(claim_result, dict):

                claim = claim_result.get(
                    "claim",
                    "Unknown claim"
                )

                verdict = claim_result.get(
                    "verdict",
                    "UNVERIFIED"
                )

                confidence = float(
                    claim_result.get(
                        "confidence",
                        0.0
                    )
                )

                explanation = claim_result.get(
                    "explanation",
                    ""
                )

                evidence = claim_result.get(
                    "evidence",
                    []
                )

            else:

                claim = getattr(
                    claim_result,
                    "claim",
                    "Unknown claim"
                )

                verdict = getattr(
                    claim_result,
                    "verdict",
                    "UNVERIFIED"
                )

                confidence = float(
                    getattr(
                        claim_result,
                        "confidence",
                        0.0
                    )
                )

                explanation = getattr(
                    claim_result,
                    "explanation",
                    ""
                )

                evidence = getattr(
                    claim_result,
                    "evidence",
                    []
                )

            # -------------------------------------------------
            # CLAIM VERDICT CONFIG
            # -------------------------------------------------

            claim_config = {

                "SUPPORTS": {
                    "emoji": "✅",
                    "label": "SUPPORTED"
                },

                "CONTRADICTS": {
                    "emoji": "❌",
                    "label": "CONTRADICTED"
                },

                "MISLEADING": {
                    "emoji": "⚠️",
                    "label": "MISLEADING"
                },

                "UNVERIFIED": {
                    "emoji": "❓",
                    "label": "UNVERIFIED"
                }
            }

            claim_status = claim_config.get(
                verdict,
                {
                    "emoji": "❓",
                    "label": verdict
                }
            )

            # -------------------------------------------------
            # CLAIM DISPLAY
            # -------------------------------------------------

            with st.expander(
                f"Claim {index}: {claim_status['emoji']} "
                f"{claim_status['label']}",
                expanded=(index == 1)
            ):

                st.markdown(
                    f"**Claim:** {claim}"
                )

                st.markdown(
                    f"**Verdict:** "
                    f"{claim_status['emoji']} "
                    f"{claim_status['label']}"
                )

                st.markdown(
                    f"**Confidence:** {confidence * 100:.1f}%"
                )

                st.progress(
                    min(max(confidence, 0.0), 1.0)
                )

                if explanation:

                    st.markdown(
                        f"**Explanation:** {explanation}"
                    )

                # -------------------------------------------------
                # EVIDENCE
                # -------------------------------------------------

                st.markdown("### 🔎 Evidence")

                if not evidence:

                    st.info(
                        "No external evidence was returned."
                    )

                else:

                    for evidence_index, item in enumerate(
                        evidence,
                        start=1
                    ):

                        if isinstance(item, dict):

                            title = item.get(
                                "title",
                                "Untitled source"
                            )

                            url = item.get(
                                "url",
                                ""
                            )

                            source = item.get(
                                "source",
                                item.get(
                                    "domain",
                                    "Unknown source"
                                )
                            )

                            snippet = item.get(
                                "snippet",
                                item.get(
                                    "text",
                                    ""
                                )
                            )

                            credibility = item.get(
                                "credibility",
                                item.get(
                                    "score",
                                    None
                                )
                            )

                        else:

                            title = getattr(
                                item,
                                "title",
                                "Untitled source"
                            )

                            url = getattr(
                                item,
                                "url",
                                ""
                            )

                            source = getattr(
                                item,
                                "source",
                                getattr(
                                    item,
                                    "domain",
                                    "Unknown source"
                                )
                            )

                            snippet = getattr(
                                item,
                                "snippet",
                                getattr(
                                    item,
                                    "text",
                                    ""
                                )
                            )

                            credibility = getattr(
                                item,
                                "credibility",
                                getattr(
                                    item,
                                    "score",
                                    None
                                )
                            )

                        with st.container():

                            st.markdown(
                                f"**{evidence_index}. {title}**"
                            )

                            st.write(
                                f"Source: {source}"
                            )

                            if credibility is not None:

                                try:

                                    credibility_value = float(
                                        credibility
                                    )

                                    st.write(
                                        "Credibility: "
                                        f"{credibility_value * 100:.1f}%"
                                    )

                                except Exception:

                                    st.write(
                                        f"Credibility: {credibility}"
                                    )

                            if snippet:

                                st.write(
                                    snippet
                                )

                            if url:

                                st.markdown(
                                    f"[🔗 Open Source]({url})"
                                )

                            st.divider()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "TruthLens AI • Evidence-based misinformation verification "
    "using web search, source credibility ranking, and Google Gemini."
)