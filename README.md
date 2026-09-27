# TruthLens AI



### AI-Powered Misinformation Detection & Fact Verification



TruthLens AI is an AI-powered fact-verification system designed to analyze textual claims and online articles, retrieve supporting evidence from the web, evaluate source credibility, and generate evidence-based verification results.



The system combines \*\*Google Gemini, web search, source credibility ranking, NLP-based claim extraction, FastAPI, and Streamlit\*\* into a single verification pipeline.



> \*\*Project status:\*\* Functional prototype

> \*\*Backend:\*\* FastAPI

> \*\*Frontend:\*\* Streamlit

> \*\*AI Model:\*\* Google Gemini

> \*\*Language:\*\* Python 3.12+



\---



## 📌 Overview



Misinformation can spread rapidly through social media, websites, blogs, and online articles.



TruthLens AI attempts to simplify the initial fact-checking process by automatically:



1\. Accepting text or an article URL.

2\. Extracting the readable article content.

3\. Identifying factual claims.

4\. Searching the web for relevant evidence.

5\. Ranking sources according to predefined credibility scores.

6\. Comparing claims against the retrieved evidence.

7\. Generating a verification verdict.

8\. Displaying evidence and explanations to the user.



The system does \*\*not\*\* claim to provide absolute truth. Its results depend on the quality, availability, and agreement of the external evidence retrieved during verification.



\---



## ✨ Features



### 🔍 Claim Extraction



Google Gemini analyzes the submitted content and extracts factual claims that can potentially be verified using external evidence.



The system attempts to exclude:



\* Opinions

\* Emotions

\* Questions

\* Greetings

\* Personal preferences

\* Vague statements

\* Unsupported predictions



\---



### 🌐 Web Evidence Search



For every extracted claim, TruthLens AI searches the web for relevant supporting or contradicting information.



The application uses the `ddgs` search library to retrieve:



\* Article titles

\* URLs

\* Search snippets

\* Source domains



\---



### 🏆 Source Credibility Ranking



Retrieved sources are assigned a predefined credibility score.



Examples include:



| Source Category             | Examples                               |

| --------------------------- | -------------------------------------- |

| Government                  | `gov.in`, `india.gov.in`, `pib.gov.in` |

| Scientific agencies         | NASA, NOAA, USGS                       |

| International organizations | WHO, UN                                |

| Major news organizations    | Reuters, AP, BBC                       |

| Indian news                 | The Hindu, Indian Express              |

| Medical                     | Mayo Clinic, Harvard Health            |

| Research                    | Nature, Science, PubMed                |

| Fact checking               | Snopes, PolitiFact, FactCheck.org      |



Unknown domains receive a lower default score.



The ranking is used as an input to the verification process and should not be interpreted as a guarantee that a source is always correct.



\---



## 🤖 AI Verification



Each claim is evaluated against the retrieved evidence.



Possible claim-level verdicts:



| Verdict       | Meaning                                                               |

| ------------- | --------------------------------------------------------------------- |

| `SUPPORTS`    | Evidence substantially supports the claim                             |

| `CONTRADICTS` | Evidence substantially contradicts the claim                          |

| `MISLEADING`  | Claim contains some truth but lacks important context or is distorted |

| `UNVERIFIED`  | Available evidence is insufficient                                    |



The application also produces:



\* Confidence score

\* Explanation

\* Evidence sources

\* Source domain

\* Source credibility score



\---



## 📊 Overall Result



After individual claims are evaluated, TruthLens AI calculates an overall result.



Possible overall results include:



\* `LIKELY TRUE`

\* `LIKELY FALSE`

\* `MISLEADING`

\* `UNVERIFIED`



Unverified claims are not treated as positive evidence in the final aggregation.



\---



# 🖥️ Application Screenshots



Screenshots can be stored inside:



```text

assets/screenshots/

```



Recommended screenshots:



### 1. TruthLens AI Home Screen



```text

!\[TruthLens AI Home](assets/screenshots/home.png)

```



### 2. URL Verification



```text

!\[URL Verification](assets/screenshots/url-verification.png)

```



### 3. Verification Results



```text

!\[Verification Results](assets/screenshots/results.png)

```



### 4. Evidence Sources



```text

!\[Evidence Sources](assets/screenshots/evidence.png)

```



### 5. API Documentation



```text

!\[API Documentation](assets/screenshots/api-docs.png)

```



\---



# 🏗️ System Architecture



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │       User           │

&#x20;                   │ Text / Article URL   │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Streamlit Frontend   │

&#x20;                   │    frontend/app.py   │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   Verification      │

&#x20;                   │      Pipeline        │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                ┌─────────────┴─────────────┐

&#x20;                │                           │

&#x20;                ▼                           ▼

&#x20;      ┌──────────────────┐        ┌──────────────────┐

&#x20;      │ Article Extractor│        │ Claim Extractor  │

&#x20;      │   Trafilatura    │        │  Google Gemini   │

&#x20;      └────────┬─────────┘        └────────┬─────────┘

&#x20;               │                           │

&#x20;               └─────────────┬─────────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │   Web Search     │

&#x20;                   │      DDGS        │

&#x20;                   └────────┬─────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │ Source Ranking   │

&#x20;                   │ Credibility Score│

&#x20;                   └────────┬─────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │ Evidence-Based   │

&#x20;                   │    Verifier      │

&#x20;                   │   Gemini AI      │

&#x20;                   └────────┬─────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │ Claim Results +  │

&#x20;                   │ Overall Verdict  │

&#x20;                   └────────┬─────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                   ┌──────────────────┐

&#x20;                   │ Streamlit Result │

&#x20;                   │    Dashboard     │

&#x20;                   └──────────────────┘

```



\---



# 🔄 Verification Workflow



```text

User Input

&#x20;   │

&#x20;   ├── Text

&#x20;   │

&#x20;   └── Article URL

&#x20;          │

&#x20;          ▼

&#x20;  Article Extraction

&#x20;          │

&#x20;          ▼

&#x20;   Claim Extraction

&#x20;          │

&#x20;          ▼

&#x20;   Web Search per Claim

&#x20;          │

&#x20;          ▼

&#x20;   Source Credibility

&#x20;      Ranking

&#x20;          │

&#x20;          ▼

&#x20;  Evidence Collection

&#x20;          │

&#x20;          ▼

&#x20;    AI Verification

&#x20;          │

&#x20;          ▼

&#x20; Claim-Level Verdict

&#x20;          │

&#x20;          ▼

&#x20;   Overall Evaluation

&#x20;          │

&#x20;          ▼

&#x20;  Results + Evidence

```



\---



# 🧩 Technology Stack



## Frontend



\* Streamlit

\* Python



## Backend



\* FastAPI

\* Uvicorn

\* Pydantic



## Artificial Intelligence



\* Google Gemini API

\* `google-genai`



## Natural Language Processing



\* Google Gemini

\* Claim extraction

\* Evidence-based classification



## Web Search



\* DDGS



## Article Extraction



\* Trafilatura



## Configuration



\* python-dotenv



## Testing



\* Pytest

\* FastAPI TestClient



\---



# 📁 Project Structure



```text

truthlens-ai/

│

├── backend/

│   ├── \_\_init\_\_.py

│   │

│   ├── api/

│   │   ├── \_\_init\_\_.py

│   │   └── routes.py

│   │

│   ├── models/

│   │   ├── \_\_init\_\_.py

│   │   └── schemas.py

│   │

│   ├── services/

│   │   ├── \_\_init\_\_.py

│   │   ├── claim\_extractor.py

│   │   ├── pipeline.py

│   │   ├── source\_ranker.py

│   │   ├── verifier.py

│   │   └── web\_search.py

│   │

│   ├── config.py

│   └── main.py

│

├── frontend/

│   └── app.py

│

├── tests/

│   ├── conftest.py

│   └── test\_api.py

│

├── assets/

│   └── screenshots/

│

├── .env.example

├── .gitignore

├── README.md

└── requirements.txt

```



\---



# 🚀 Installation



## 1. Clone the repository



```bash

git clone https://github.com/VinayTodkar/Truthlens-ai.git

cd Truthlens-ai

```



\---



## 2. Create a virtual environment



### Windows



```powershell

python -m venv venv

```



Activate it:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\---



## 3. Install dependencies



```powershell

pip install -r requirements.txt

```



\---



# 🔐 Configuration



Create a `.env` file in the project root.



```env

GEMINI\_API\_KEY=your\_gemini\_api\_key\_here

GEMINI\_MODEL=gemini-3.6-flash

```



The `.env` file must remain private.



It is included in `.gitignore` and should \*\*never be committed to GitHub\*\*.



The repository provides `.env.example` as a safe configuration template.



\---



# ▶️ Running the Application



## Start the Streamlit frontend



From the project root:



```powershell

streamlit run frontend/app.py

```



Streamlit will provide a local address similar to:



```text

http://localhost:8501

```



Open that address in your browser.



\---



# ⚙️ Running the FastAPI Backend



Start the API server with:



```powershell

uvicorn backend.main:app --reload

```



The API will normally be available at:



```text

http://127.0.0.1:8000

```



FastAPI interactive documentation:



```text

http://127.0.0.1:8000/docs

```



\---



# 🔌 API Documentation



## GET `/`



Checks whether the application is running.



### Response



```json

{

&#x20; "application": "TruthLens AI",

&#x20; "status": "running"

}

```



\---



## GET `/health`



Health-check endpoint.



### Response



```json

{

&#x20; "status": "healthy"

}

```



\---



## POST `/api/v1/verify`



Verifies submitted text or an article URL.



### Request with text



```json

{

&#x20; "text": "The Earth is approximately 4.5 billion years old."

}

```



### Request with URL



```json

{

&#x20; "url": "https://example.com/article"

}

```



### Response structure



```json

{

&#x20; "input\_text": "...",

&#x20; "overall\_verdict": "LIKELY TRUE",

&#x20; "overall\_confidence": 0.92,

&#x20; "claims": \[

&#x20;   {

&#x20;     "claim": "...",

&#x20;     "verdict": "SUPPORTS",

&#x20;     "confidence": 0.95,

&#x20;     "explanation": "...",

&#x20;     "evidence": \[

&#x20;       {

&#x20;         "title": "...",

&#x20;         "url": "...",

&#x20;         "snippet": "...",

&#x20;         "source\_domain": "...",

&#x20;         "source\_score": 0.98

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ]

}

```



\---



# 🧪 Testing



Run the automated tests:



```powershell

pytest -q

```



Current API test coverage includes:



\* Root endpoint

\* Health endpoint

\* Invalid verification request handling



Example:



```text

3 passed

```



The tests do not require a successful Gemini generation request, so normal API validation can be tested independently of Gemini availability.



\---



# ⚠️ Gemini API Quota & Availability



TruthLens AI depends on the Google Gemini API for:



\* Claim extraction

\* Claim verification



The Gemini API may enforce project/model-specific rate limits and free-tier quotas.



If the quota is exhausted, the application handles the condition and can return an `UNVERIFIED` result rather than treating the claim as verified.



Possible temporary conditions include:



\* HTTP `429` — quota/rate limit exhausted

\* HTTP `503` — service temporarily unavailable/high demand



When Gemini verification is unavailable:



```text

UNVERIFIED

```



does \*\*not\*\* mean the claim is false.



It means that the application could not obtain sufficient AI verification at that time.



Users should review the displayed evidence sources manually when AI verification is unavailable.



For reliable production usage, configure an appropriate Gemini API plan and monitor its usage limits.



\---



# 🔒 Security



Never commit:



```text

.env

```



or any file containing an actual API key.



The repository uses:



```text

.env.example

```



for configuration documentation.



The actual API key should exist only in the local `.env` file or an appropriately secured deployment environment.



\---



# ⚠️ Limitations



TruthLens AI is an automated fact-verification prototype and has several limitations.



### Search dependency



Verification quality depends on the availability and quality of search results.



### Source ranking



Source credibility scores are based on predefined domain rules. A high score does not guarantee that every individual article or claim from that domain is correct.



### AI limitations



Gemini can produce incorrect or incomplete interpretations. AI-generated verdicts should therefore be treated as an assistance mechanism rather than absolute proof.



### Conflicting evidence



Different sources may disagree. The application attempts to identify conflicts but cannot guarantee perfect resolution.



### API quotas



Gemini API quotas can temporarily prevent claim extraction or verification.



### Dynamic websites



Some websites may block automated extraction or contain content that cannot be retrieved successfully.



\---



# 🎯 Project Objectives



The main objectives of TruthLens AI are to:



\* Automate initial claim verification.

\* Reduce the time required to locate relevant evidence.

\* Provide source-aware fact verification.

\* Present evidence alongside AI-generated explanations.

\* Demonstrate an end-to-end AI + web-search pipeline.

\* Provide an accessible interface for non-technical users.



\---



# 🔮 Future Improvements



Potential future improvements include:



\* Multi-model verification

\* More advanced source credibility scoring

\* Claim importance weighting

\* Cross-source consensus analysis

\* Citation quality analysis

\* Multilingual misinformation detection

\* Social-media claim verification

\* Browser extension

\* Batch article verification

\* Verification history

\* Database-backed results

\* User authentication

\* Improved evidence summarization

\* Automated source freshness detection



\---



# 📌 Example Use Cases



TruthLens AI can be used as an experimental tool for:



\* Fact-checking online claims

\* Educational demonstrations

\* Research prototypes

\* Media-literacy applications

\* AI/NLP projects

\* Evidence retrieval experiments

\* Demonstrating LLM-powered verification pipelines



\---



# 👨‍💻 Author



\*\*Vinay Todkar\*\*



B.Tech — Artificial Intelligence & Data Science



GitHub:



https://github.com/VinayTodkar



Project:



https://github.com/VinayTodkar/Truthlens-ai



Deployed Project:



https://truthlens-ai-1-e7ic.onrender.com/



\---



# 📄 License



This project is intended for educational and research purposes.



Add an appropriate open-source license before distributing the project for broader reuse.




