import dns.resolver
from langchain.tools import tool

COMMON_SUBDOMAINS = ["www", "mail", "ftp", "admin", "api", "dev", "staging",
                     "test", "vpn", "remote", "portal", "blog", "shop", "cdn"]

@tool
def subdomain_enum(domain: str) -> str:
    """Enumerate common subdomains for a domain via DNS brute-force."""
    found = []
    for sub in COMMON_SUBDOMAINS:
        try:
            target = f"{sub}.{domain}"
            dns.resolver.resolve(target, "A")
            found.append(target)
        except Exception:
            pass
    return str({"discovered_subdomains": found, "checked": len(COMMON_SUBDOMAINS)})
