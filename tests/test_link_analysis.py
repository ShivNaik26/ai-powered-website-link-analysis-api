
import pytest

from app.utils.validators import validate_website_url


def test_valid_https_url(monkeypatch):
    def mock_getaddrinfo(*args, **kwargs):
        return [
            (2, 1, 6, "", ("93.184.216.34", 443))
        ]

    monkeypatch.setattr(
        "app.utils.validators.socket.getaddrinfo",
        mock_getaddrinfo
    )

    result = validate_website_url("https://example.com")

    assert result == "https://example.com"


def test_reject_empty_url():
    with pytest.raises(ValueError):
        validate_website_url("")


def test_reject_invalid_scheme():
    with pytest.raises(ValueError):
        validate_website_url("ftp://example.com")


def test_reject_localhost():
    with pytest.raises(ValueError):
        validate_website_url("http://localhost")


def test_reject_url_with_credentials():
    with pytest.raises(ValueError):
        validate_website_url("https://user:password@example.com")


def test_reject_unsupported_port():
    with pytest.raises(ValueError):
        validate_website_url("https://example.com:8080")


def test_reject_private_ip(monkeypatch):
    def mock_getaddrinfo(*args, **kwargs):
        return [
            (2, 1, 6, "", ("192.168.1.10", 443))
        ]

    monkeypatch.setattr(
        "app.utils.validators.socket.getaddrinfo",
        mock_getaddrinfo
    )

    with pytest.raises(ValueError):
        validate_website_url("https://example.com")
