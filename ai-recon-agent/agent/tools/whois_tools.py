import whois
from langchain.tools import tool

@tool
def whois_lookup(target: str) -> str:
    """Perform WHOIS lookup on a domain or IP. Returns registrar, dates, nameservers."""
    try:
        w = whois.whois(target)
        return str({
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "org": w.org,
        })
    except Exception as e:
        return f"WHOIS failed: {e}"
