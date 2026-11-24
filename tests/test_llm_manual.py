
import asyncio
from app.services.website_extractor import fetch_website_content
from app.services.llm_service import analyze_website_with_ai


async def main():
    website = await fetch_website_content(
        "https://example.com"
    )

    result = await analyze_website_with_ai(website)

    print("\nBRAND:")
    print(result["brand"])

    print("\nANALYSIS SECTIONS:")
    print(list(result["analysis"].keys()))

    print("\nTOKEN USAGE:")
    print(result["usage"])


if __name__ == "__main__":
    asyncio.run(main())
