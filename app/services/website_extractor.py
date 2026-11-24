
import httpx
import ipaddress
import socket

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.utils.validators import validate_website_url
from app.config import REQUEST_TIMEOUT, MAX_HTML_SIZE, MAX_CONTENT_LENGTH


USER_AGENT = (
    "Mozilla/5.0 (compatible; WebsiteAnalysisBot/1.0)"
)

MAX_REDIRECTS = 3


async def fetch_website_content(url: str) -> dict:
    """
    Fetch and extract useful information from a public website.
    """

    current_url = validate_website_url(url)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
    }

    timeout = httpx.Timeout(REQUEST_TIMEOUT)

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=False,
        trust_env=False,
    ) as client:

        response = None

        for redirect_count in range(MAX_REDIRECTS + 1):

            # Validate every redirect destination.
            current_url = validate_website_url(current_url)

            try:
                async with client.stream(
                    "GET",
                    current_url,
                    headers=headers,
                ) as result:

                    if result.status_code in (301, 302, 303, 307, 308):
                        location = result.headers.get("location")

                        if not location:
                            raise ValueError(
                                "Website returned an invalid redirect."
                            )

                        if redirect_count >= MAX_REDIRECTS:
                            raise ValueError(
                                "Too many website redirects."
                            )

                        current_url = urljoin(current_url, location)
                        continue

                    if result.status_code >= 400:
                        raise ValueError(
                            f"Website returned HTTP {result.status_code}."
                        )

                    content_type = result.headers.get(
                        "content-type", ""
                    ).lower()

                    if not (
                        "text/html" in content_type
                        or "application/xhtml+xml" in content_type
                    ):
                        raise ValueError(
                            "The URL does not return an HTML page."
                        )

                    content_length = result.headers.get("content-length")

                    if content_length:
                        if int(content_length) > MAX_HTML_SIZE:
                            raise ValueError(
                                "Website HTML exceeds the allowed size."
                            )

                    html_chunks = []
                    total_size = 0

                    async for chunk in result.aiter_bytes():
                        total_size += len(chunk)

                        if total_size > MAX_HTML_SIZE:
                            raise ValueError(
                                "Website HTML exceeds the allowed size."
                            )

                        html_chunks.append(chunk)

                    html_content = b"".join(html_chunks)
                    response = html_content
                    break

            except httpx.TimeoutException as exc:
                raise ValueError(
                    "Website request timed out."
                ) from exc

            except httpx.HTTPError as exc:
                raise ValueError(
                    "Unable to connect to the website."
                ) from exc

        if response is None:
            raise ValueError("Unable to retrieve website content.")

    # Parse HTML
    soup = BeautifulSoup(response, "html.parser")

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else ""
    )

    meta_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    meta_description = (
        meta_tag.get("content", "")
        if meta_tag
        else ""
    )

    # Extract headings
    headings = {}

    for tag in ["h1", "h2", "h3"]:
        headings[tag] = [
            heading.get_text(" ", strip=True)
            for heading in soup.find_all(tag)
            if heading.get_text(strip=True)
        ]

    # Remove unnecessary HTML elements
    for element in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "form",
    ]):
        element.decompose()

    # Extract readable text
    website_text = soup.get_text(
        separator=" ",
        strip=True
    )

    website_text = " ".join(website_text.split())

    if not website_text:
        raise ValueError(
            "No readable website content was found."
        )

    website_text = website_text[:MAX_CONTENT_LENGTH]

    return {
        "url": current_url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "content": website_text,
        "content_length": len(website_text),
    }
