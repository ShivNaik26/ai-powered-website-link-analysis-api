
import json

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL


SYSTEM_PROMPT = """
You are a business analyst and SEO specialist.

Analyze the supplied website content and return valid JSON.

Use this structure:

{
  "brand": {
    "name": "",
    "category": "",
    "summary": ""
  },
  "analysis": {
    "competitor_analysis": {
      "brand_overview": "",
      "business_category": "",
      "main_products_services": [],
      "competitors": [],
      "strengths": [],
      "weaknesses": [],
      "competitive_advantages": [],
      "opportunities": []
    },
    "target_search_queries": [],
    "seo_improvements": {
      "primary_keyword": "",
      "secondary_keywords": [],
      "long_tail_keywords": [],
      "business_keywords": [],
      "recommended_title": "",
      "meta_description": "",
      "supporting_content": []
    },
    "top_services": [],
    "target_audience": {
      "primary_audience": [],
      "secondary_audience": [],
      "industries": [],
      "business_types": [],
      "customer_profiles": [],
      "geographical_focus": [],
      "customer_needs": [],
      "customer_interests": [],
      "marketing_segments": []
    }
  }
}

Rules:
- Use actual supplied website content.
- Do not invent business facts or search volumes.
- Clearly label unverified competitor suggestions.
- Generate five search queries where possible.
- Generate five service objects where possible.
- Label actual services as website_content.
- Label inferred services as AI_inference.
- Return empty arrays when information is unavailable.
- Return JSON only.
"""


async def analyze_website_with_ai(website_data: dict) -> dict:

    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is not configured.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    user_prompt = f"""
Analyze this website:

URL: {website_data.get('url', '')}

Title: {website_data.get('title', '')}

Meta description:
{website_data.get('meta_description', '')}

Headings:
{json.dumps(website_data.get('headings', {}), ensure_ascii=False)}

Website content:
{website_data.get('content', '')}
"""

    try:
        async with client.aio as ai_client:

            response = await ai_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    SYSTEM_PROMPT,
                    user_prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                    max_output_tokens=4000
                )
            )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        result = json.loads(response.text)

        if not isinstance(result, dict):
            raise ValueError("Invalid AI response.")

        if not isinstance(result.get("brand"), dict):
            raise ValueError("Brand information is missing.")

        if not isinstance(result.get("analysis"), dict):
            raise ValueError("Analysis information is missing.")

        required_sections = [
            "competitor_analysis",
            "target_search_queries",
            "seo_improvements",
            "top_services",
            "target_audience"
        ]

        for section in required_sections:
            if section not in result["analysis"]:
                raise ValueError(
                    f"Missing analysis section: {section}"
                )

        usage = response.usage_metadata

        result["usage"] = {
            "input_tokens": usage.prompt_token_count if usage else 0,
            "output_tokens": usage.candidates_token_count if usage else 0,
            "total_tokens": usage.total_token_count if usage else 0
        }

        return result

    except json.JSONDecodeError as exc:
        raise ValueError("Gemini returned invalid JSON.") from exc

    except ValueError:
        raise

    except Exception as exc:
        raise RuntimeError(
            f"Gemini API request failed: {exc}"
        ) from exc

    finally:
        client.close()
