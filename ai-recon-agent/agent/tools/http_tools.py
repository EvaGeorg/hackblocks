import requests
from langchain.tools import tool

@tool
def http_headers_probe(target: str) -> str:
    """Probe HTTP/HTTPS headers of a target URL. Detects server, technologies, security headers."""
    if not target.startswith("http"):
        target = f"https://{target}"
    try:
        resp = requests.get(target, timeout=10, allow_redirects=True)
        headers = dict(resp.headers)
        security_headers = {
            k: v for k, v in headers.items()
            if k.lower() in ["server", "x-powered-by", "x-frame-options",
                              "content-security-policy", "strict-transport-security"]
        }
        return str({
            "status_code": resp.status_code,
            "final_url": resp.url,
            "security_headers": security_headers,
            "all_headers": headers,
        })
    except Exception as e:
        return f"HTTP probe failed: {e}"
