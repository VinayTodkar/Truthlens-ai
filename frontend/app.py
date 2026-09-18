import sys
from pathlib import Path

import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from backend.services.pipeline import verify_content


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
# HEADER
# =========================================================

st.title("🔎 TruthLens AI")

st.markdown(
    "### AI-Powered Misinformation & Fact Verification System"
)

st.write(
    "Analyze claims, search external evidence, rank sources, "
    "and evaluate whether claims are supported, contradicted, "
    "misleading, or unverified."
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

        It follows this pipeline:
        """
    )

    st.write("1. 📝 Claim Extraction")
    st.write("2. 🌐 Web Search")
    st.write("3. ⭐ Source Ranking")
    st.write("4. 🤖 AI Verification")
    st.write("5. 📊 Final Verdict")

    st.divider()

    st.subheader("📌 Verdicts")

    st.write("✅ SUPPORTS")
    st.write("❌ CONTRADICTS")
    st.write("⚠️ MISLEADING")
    st.write("❓ UNVERIFIED")

    st.divider()

    st.caption(
        "TruthLens AI is a prototype. Always review "
        "the cited sources before making high-stakes decisions."
    )


# =========================================================
# INPUT TABS
# =========================================================

text_tab, url_tab = st.tabs(
    [
        "📝 Verify Text",
        "🌐 Verify URL"
    ]
)


# =========================================================
# TEXT VERIFICATION
# =========================================================

with text_tab:

    st.subheader("Enter a claim or article")

    text_input = st.text_area(
        "Text",
        height=200,
        placeholder=(
            "Example:\n\n"
            "The Earth is flat."
        ),
        label_visibility="collapsed"
    )

    verify_text = st.button(
        "🔎 Verify Text",
        type="primary",
        use_container_width=True
    )

    if verify_text:

        if not text_input.strip():

            st.warning(
                "Please enter a claim or article."
            )

        else:

            with st.spinner(
                "🔍 Extracting claims, searching the web, "
                "and verifying evidence..."
            ):

                try:

                    result = verify_content(
                        text=text_input.strip()
                    )

                    st.session_state[
                        "verification_result"
                    ] = result

                except Exception as e:

                    error_message = str(e).lower()

                    if (
                      "429" in error_message
                      or "quota" in error_message
                      or "resource_exhausted" in error_message
                    ):

                      st.warning(
                        "⚠️ Gemini API quota is currently exhausted. "
                        "Please try again after the quota resets. "
                        "The application itself is working correctly."
                      )

                    else:
                      st.error(
                      f"Verification failed: {e}"
                    )


# =========================================================
# URL VERIFICATION
# =========================================================

with url_tab:

    st.subheader("Enter an article URL")

    url_input = st.text_input(
        "Article URL",
        placeholder="https://example.com/article"
    )

    verify_url = st.button(
        "🌐 Verify Article",
        type="primary",
        use_container_width=True
    )

    if verify_url:

        if not url_input.strip():

            st.warning(
                "Please enter an article URL."
            )

        else:

            with st.spinner(
                "🌐 Downloading article, extracting claims, "
                "and verifying evidence..."
            ):

                try:

                    result = verify_content(
                        url=url_input.strip()
                    )

                    st.session_state[
                        "verification_result"
                    ] = result

                except Exception as e:

                   error_message = str(e).lower()

                   if (
                      "429" in error_message
                      or "quota" in error_message
                      or "resource_exhausted" in error_message
                   ):

                      st.warning(
                        "⚠️ Gemini API quota is currently exhausted. "
                        "Please try again after the quota resets."
                      )

                   else:

                      st.error(
                      f"URL verification failed: {e}"
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


    # =====================================================
    # OVERALL RESULT
    # =====================================================

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


    # =====================================================
    # VERDICT CONFIGURATION
    # =====================================================

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


    verdict_info = verdict_config.get(
        overall_verdict,
        {
            "emoji": "❓",
            "label": overall_verdict
        }
    )


    # =====================================================
    # KPI CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Overall Verdict",
            f"{verdict_info['emoji']} "
            f"{verdict_info['label']}"
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


    # =====================================================
    # OVERALL CONFIDENCE
    # =====================================================

    st.subheader("🎯 Overall Confidence")

    st.progress(
        max(
            0.0,
            min(
                1.0,
                overall_confidence
            )
        )
    )

    st.caption(
        f"The system has {overall_confidence * 100:.1f}% "
        "confidence in the overall result."
    )


    # =====================================================
    # ANALYZED CONTENT
    # =====================================================

    with st.expander(
        "📄 View Analyzed Content"
    ):

        st.write(
            result.get(
                "input_text",
                ""
            )
        )


    # =====================================================
    # CLAIMS
    # =====================================================

    st.header("🔍 Claims Detected")


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
            # CLAIM RESULT
            # -------------------------------------------------

            claim = claim_result.claim

            verdict = claim_result.verdict

            confidence = float(
                claim_result.confidence
            )

            explanation = claim_result.explanation

            evidence = claim_result.evidence


            # -------------------------------------------------
            # CLAIM STATUS
            # -------------------------------------------------

            claim_config = {

                "SUPPORTS": {
                    "emoji": "✅",
                    "label": "SUPPORTS"
                },

                "CONTRADICTS": {
                    "emoji": "❌",
                    "label": "CONTRADICTS"
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


            claim_info = claim_config.get(
                verdict,
                {
                    "emoji": "❓",
                    "label": verdict
                }
            )


            # -------------------------------------------------
            # CLAIM HEADER
            # -------------------------------------------------

            st.subheader(
                f"Claim {index}"
            )

            st.markdown(
                f"### {claim_info['emoji']} {claim}"
            )


            # -------------------------------------------------
            # CLAIM METRICS
            # -------------------------------------------------

            claim_col1, claim_col2 = st.columns(2)


            with claim_col1:

                st.metric(
                    "Verdict",
                    claim_info["label"]
                )


            with claim_col2:

                st.metric(
                    "Confidence",
                    f"{confidence * 100:.1f}%"
                )


            # -------------------------------------------------
            # CLAIM CONFIDENCE
            # -------------------------------------------------

            st.progress(
                max(
                    0.0,
                    min(
                        1.0,
                        confidence
                    )
                )
            )


            # -------------------------------------------------
            # EXPLANATION
            # -------------------------------------------------

            st.markdown(
                "#### 🧠 Explanation"
            )

            st.write(
                explanation
            )


            # -------------------------------------------------
            # EVIDENCE
            # -------------------------------------------------

            st.markdown(
                "#### 📚 Evidence Sources"
            )


            if not evidence:

                st.info(
                    "No external evidence was available "
                    "for this claim."
                )


            else:

                for source_index, source in enumerate(
                    evidence,
                    start=1
                ):

                    title = source.title

                    url = source.url

                    snippet = source.snippet

                    domain = source.source_domain

                    source_score = float(
                        source.source_score
                    )


                    # -----------------------------------------
                    # SOURCE EXPANDER
                    # -----------------------------------------

                    with st.expander(
                        f"🌐 Source {source_index}: "
                        f"{domain}"
                    ):

                        st.markdown(
                            f"**{title}**"
                        )

                        st.write(
                            snippet
                        )

                        st.write(
                            f"**Source Credibility:** "
                            f"{source_score * 100:.0f}%"
                        )


                        if url:

                            st.link_button(
                                "🔗 View Source",
                                url,
                                use_container_width=True
                            )


            # -------------------------------------------------
            # CLAIM DIVIDER
            # -------------------------------------------------

            if index < len(claims):

                st.divider()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "TruthLens AI • AI-powered misinformation detection "
    "and evidence verification"
)

