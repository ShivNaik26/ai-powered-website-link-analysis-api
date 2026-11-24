
# AI-Powered Website Link Analysis API

A Python-based website analysis API built using FastAPI, HTTPX, BeautifulSoup and Google Gemini.

## 1. Project Overview

This project was developed as part of the Python Practical Test assigned by Dxora Technologies.

The objective is to analyze a website URL, extract its publicly available content and use an AI model to generate structured business and SEO insights.

The API accepts a website URL and returns brand information, competitor suggestions, target search queries, SEO recommendations, services and target audience insights.

## 2. Project Objectives

- Extract website content from a submitted URL.
- Identify the website's brand and business category.
- Generate competitor analysis.
- Suggest target search queries for social and search platforms.
- Recommend SEO improvements.
- Identify key products and services.
- Analyze potential target audiences.
- Return structured JSON through a REST API.

## 3. Features

### Brand Analysis
- Brand name
- Business category
- Brand overview

### Competitor Analysis
- Brand overview
- Business category
- Main products and services
- Competitor suggestions
- Strengths and weaknesses
- Competitive advantages
- Business opportunities

AI-generated competitor suggestions are not independently verified.

### Target Search Queries
Generates five suggested search queries for platforms such as:
- Google
- Facebook
- Instagram
- LinkedIn
- X

### SEO Improvements
- Primary keyword
- Secondary keywords
- Long-tail keywords
- Business keywords
- Recommended page title
- Meta description
- Supporting content suggestions

### Top Services
Generates service descriptions and related business insights based on available website content and AI inference.

### Target Audience
- Primary and secondary audiences
- Industries and business types
- Customer profiles
- Geographical focus
- Customer needs and interests
- Marketing segments

AI-generated insights should be reviewed before making business decisions.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| HTTPX | Website requests |
| BeautifulSoup | HTML parsing |
| Google Gemini | AI-powered analysis |
| Pydantic | Request and response validation |
| python-dotenv | Environment configuration |
| Uvicorn | ASGI server |
| Pytest | Testing framework |

## 5. Project Structure

```text
Ai-link-Analysis/
│
├── app/
│   ├── services/
│   │   ├── competitor_service.py
│   │   ├── llm_service.py
│   │   └── website_extractor.py
│   │
│   ├── utils/
│   │   └── validators.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── schemas.py
│
├── tests/
│   ├── test_link_analysis.py
│   └── test_llm_manual.py
│
├── screenshots/
│
├── .env.example
├── .gitignore
├── LLM_COMPARISON.md
├── requirements.txt
└── README.md
```

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Google Gemini API key

### Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Ai-link-Analysis
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 7. Environment Configuration

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder with your own API key.

Never upload `.env` or expose API keys in public repositories.

## 8. Run the Application

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

Local API:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 9. API Usage

### Endpoint

```http
POST /link-analysis
```

### Request Body

```json
{
  "url": "https://www.microsoft.com"
}
```

### Successful Response

The API returns a structured JSON response containing:

```json
{
  "success": true,
  "website": {},
  "brand": {},
  "analysis": {
    "competitor_analysis": {},
    "target_search_queries": [],
    "seo_improvements": {},
    "top_services": [],
    "target_audience": {}
  },
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0
  }
}
```

Token counts and analysis values depend on the actual API response.

## 10. URL Validation and Security

The application includes URL validation and website-fetching safeguards.

- Allows HTTP and HTTPS URLs.
- Rejects invalid URL formats.
- Blocks localhost URLs.
- Rejects non-global IP addresses.
- Restricts URL ports.
- Validates redirect destinations.
- Limits downloaded HTML size.
- Uses request timeouts.
- Does not follow redirects automatically without validation.

Security limitations remain. DNS rebinding protection through connection-level IP pinning has not been implemented or verified. Further security testing is required before production use.

## 11. LLM Provider Comparison

The project includes a separate comparison document:

[LLM Provider Comparison](LLM_COMPARISON.md)

It discusses Google Gemini, OpenAI and Anthropic, including documented capabilities, pricing and cost optimization.

No direct three-provider performance benchmark has been conducted.

## 12. Screenshots

Screenshots of project development and local API testing are available in the `screenshots/` directory.

| Screenshot | Description |
|---|---|
| 01_project_setup.png | Project structure |
| 02_dependencies_installed.png | Installed dependencies |
| 03_configuration.png | Environment configuration |
| 04_url_validation.png | URL validation |
| 05_website_extraction.png | Website content extraction |
| 06_llm_integration.png | Gemini integration |
| 07_pydantic_schemas.png | Pydantic schemas |
| 08_analysis_service.png | Analysis service |
| 09_fastapi_application.png | FastAPI application |
| 10_api_running.png | Running API server |
| 11_swagger_ui.png | Swagger documentation |
| 12_health_check.png | Health endpoint |
| 13_successful_api_response.png | Successful API response |
| 13_successful_response_bottom.png | Response details |
| 14_error_handling.png | Invalid URL response |

Additional real website testing was performed with Microsoft. Its output is not independently verified market research.

## 13. Cost Optimization

Potential cost optimization methods include:

- Limiting website content before sending it to the LLM.
- Removing unnecessary HTML elements.
- Restricting output token limits.
- Using cost-efficient models.
- Reusing previously extracted content where appropriate.
- Handling API failures and rate limits.

Actual API costs depend on provider pricing and usage.

## 14. Current Limitations

- Competitor suggestions are AI-generated and may require external verification.
- Search query volumes and rankings are not measured.
- No direct performance benchmark across three providers has been performed.
- Live deployment has not yet been completed.
- Production-grade DNS rebinding protection requires further work.

## 15. Future Improvements

- Add independent competitor research.
- Improve validation of AI-generated output.
- Add caching and retry handling.
- Perform comparative LLM benchmarks.
- Deploy the API to a public hosting platform.
- Add automated test coverage.

## 16. License

License to be selected before public release.
```

### Step 1 – Save and verify
