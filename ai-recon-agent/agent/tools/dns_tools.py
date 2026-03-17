import dns.resolver
from langchain.tools import tool

@tool
def dns_lookup(target: str) -> str:
    """Perform DNS enumeration on a domain. Returns A, MX, NS, TXT records."""
    results = {}
    for record_type in ["A", "MX", "NS", "TXT", "CNAME"]:
        try:
            answers = dns.resolver.resolve(target, record_type)
            results[record_type] = [str(r) for r in answers]
        except Exception:
            results[record_type] = []
    return str(results)
