# 🤖 AI Recon Agent

An autonomous reconnaissance agent powered by LangChain that enumerates targets, 
selects tools dynamically, and outputs structured findings.

## Features
- 🔍 Autonomous tool selection — the agent decides what to run
- 🌐 DNS enumeration, WHOIS, HTTP probing, port scanning, subdomain discovery
- 📄 Structured JSON output with full audit trail
- 🖥️ Rich CLI interface

## Prerequisites
- Python 3.11+
- nmap installed: `brew install nmap` / `apt install nmap`
- OpenAI API key (or Anthropic)

## Installation
\`\`\`bash
git clone https://github.com/EvaGeorg/hackblocks/ai-recon-agent
cd ai-recon-agent
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env   # Add your API key
\`\`\`

## Usage

### Basic scan
\`\`\`bash
python main.py example.com
\`\`\`

### Save findings to file
\`\`\`bash
python main.py example.com --save
\`\`\`

### Markdown output
\`\`\`bash
python main.py 192.168.1.1 --output markdown --save
\`\`\`

## Example Output
\`\`\`json
{
  "target": "example.com",
  "output": "Recon complete. Found 3 subdomains, ports 80/443 open, 
             running nginx/1.24. MX records point to Google Workspace.",
  "steps": 5
}
\`\`\`

## Architecture
The agent uses LangChain's OpenAI Tools agent with 5 custom tools:

dns_tools.py - Performs DNS enumeration (A, MX, NS, TXT, CNAME records) to map infrastructure and identify hosting, email providers, and metadata.

whois_tools.py - Retrieves domain ownership information such as registrar, creation/expiration dates, and organization details for OSINT insights.

subdomain_tools.py - Discovers common subdomains (e.g. admin, api, dev) to expand the attack surface and uncover hidden entry points.

http_tools.py - Probes HTTP/HTTPS endpoints to extract headers, detect technologies, and analyze security configurations.

port_tools.py - Uses Nmap to scan for open ports and running services, helping identify exposed systems and potential vulnerabilities.


## Legal Notice
Only use against targets you own or have explicit permission to test.
