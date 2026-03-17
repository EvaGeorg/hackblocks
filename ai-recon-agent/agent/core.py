from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
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

def build_agent(verbose: bool = True) -> AgentExecutor:
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, TOOLS, prompt)
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=verbose,
        max_iterations=int(os.getenv("MAX_ITERATIONS", 10)),
        return_intermediate_steps=True,
    )

def run_recon(target: str) -> dict:
    agent = build_agent(verbose=os.getenv("VERBOSE", "true").lower() == "true")
    result = agent.invoke({"input": f"Perform full reconnaissance on target: {target}"})
    return result
