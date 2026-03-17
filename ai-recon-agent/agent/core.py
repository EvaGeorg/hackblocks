from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

from agent.tools.dns_tools import dns_lookup
from agent.tools.whois_tools import whois_lookup
from agent.tools.http_tools import http_headers_probe
from agent.tools.port_tools import port_scan
from agent.tools.subdomain_tools import subdomain_enum

load_dotenv()

TOOLS = [dns_lookup, whois_lookup, http_headers_probe, port_scan, subdomain_enum]

SYSTEM_PROMPT = """You are an autonomous reconnaissance agent. Your job is to thoroughly 
enumerate a given target using the available tools. 

For each target:
1. Start with WHOIS and DNS to understand ownership and infrastructure
2. Probe HTTP headers to identify technologies
3. Enumerate subdomains to map the attack surface
4. Scan common ports to identify exposed services
5. Synthesize all findings into a structured summary

Be methodical. Use each relevant tool. Report ALL findings clearly."""

def run_recon(target: str) -> dict:
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    agent = create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt=SYSTEM_PROMPT,
    )

    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Perform full reconnaissance on target: {target}"}]
    })

    # Extract the final text response
    final_message = result["messages"][-1]
    output = final_message.content if hasattr(final_message, "content") else str(final_message)

    return {
        "output": output,
        "intermediate_steps": result["messages"],
    }
