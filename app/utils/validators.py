
import ipaddress
import socket
from urllib.parse import urlparse


def validate_website_url(url: str) -> str:
    """Validate a public HTTP/HTTPS website URL."""

    if not isinstance(url, str) or not url.strip():
        raise ValueError("Website URL is required.")

    url = url.strip()

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError("Only HTTP and HTTPS URLs are allowed.")

        if not parsed.hostname:
            raise ValueError("Invalid website URL.")

        if parsed.username or parsed.password:
            raise ValueError("URLs containing credentials are not allowed.")

        if parsed.port not in (None, 80, 443):
            raise ValueError("This URL port is not allowed.")

        hostname = parsed.hostname.lower().rstrip(".")

        if hostname == "localhost" or hostname.endswith(".localhost"):
            raise ValueError("Localhost URLs are not allowed.")

        # Resolve DNS and inspect every returned IP address.
        addresses = socket.getaddrinfo(
            hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
            type=socket.SOCK_STREAM,
        )

        if not addresses:
            raise ValueError("Website hostname could not be resolved.")

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if not ip.is_global:
                raise ValueError(
                    "Private, local and reserved IP addresses are not allowed."
                )

        return url

    except ValueError:
        raise
    except (socket.gaierror, OSError):
        raise ValueError("Website hostname could not be resolved.")
