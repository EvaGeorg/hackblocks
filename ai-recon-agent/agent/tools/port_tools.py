import nmap
from langchain.tools import tool

@tool
def port_scan(target: str) -> str:
    """Scan common ports on a target host. Returns open ports and services."""
    try:
        nm = nmap.PortScanner()
        nm.scan(target, arguments="-F --open -T4")  # Fast scan, open ports only
        results = {}
        for host in nm.all_hosts():
            results[host] = {}
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                results[host][proto] = {
                    port: nm[host][proto][port] for port in ports
                }
        return str(results)
    except Exception as e:
        return f"Port scan failed: {e}"
