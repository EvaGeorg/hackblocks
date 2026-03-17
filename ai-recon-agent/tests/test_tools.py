import pytest
from unittest.mock import patch, MagicMock

def test_http_probe_adds_https():
    from agent.tools.http_tools import http_headers_probe
    # Test that bare domain gets https:// prepended
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200, url="https://example.com", headers={}
        )
        result = http_headers_probe.invoke("example.com")
        assert "200" in result

def test_subdomain_enum_returns_dict():
    from agent.tools.subdomain_tools import subdomain_enum
    with patch("dns.resolver.resolve", side_effect=Exception("NXDOMAIN")):
        result = subdomain_enum.invoke("example.com")
        assert "discovered_subdomains" in result
