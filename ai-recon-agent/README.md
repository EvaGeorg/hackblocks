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
git clone https://github.com/YOUR_USERNAME/ai-recon-agent
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
The agent uses LangChain's OpenAI Tools agent with 5 custom tools (will describe tools later)

## Legal Notice
Only use against targets you own or have explicit permission to test.
