
from app.services.website_extractor import fetch_website_content
from app.services.llm_service import analyze_website_with_ai


async def analyze_link(url: str) -> dict:
    # Step 1: Fetch website content
    website_data = await fetch_website_content(url)

    # Step 2: Analyze website using Gemini
    ai_result = await analyze_website_with_ai(website_data)

    # Step 3: Prepare structured API response
    return {
        "success": True,
        "website": {
            "url": website_data.get("url", url),
            "title": website_data.get("title", ""),
            "meta_description": website_data.get(
                "meta_description", ""
            ),
            "content_length": website_data.get(
                "content_length", 0
            ),
        },
        "brand": ai_result.get("brand", {}),
        "analysis": ai_result.get("analysis", {}),
        "usage": ai_result.get("usage", {}),
    }
