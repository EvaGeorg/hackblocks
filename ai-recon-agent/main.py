import argparse
import json
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from agent.core import run_recon
from agent.output.formatter import save_findings

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="🔍 AI Recon Agent — Autonomous target enumeration"
    )
    parser.add_argument("target", help="Target domain, IP, or URL")
    parser.add_argument("--output", "-o", default="json",
                        choices=["json", "markdown"], help="Output format")
    parser.add_argument("--save", "-s", action="store_true",
                        help="Save findings to findings/ directory")
    args = parser.parse_args()

    console.print(Panel(f"[bold green]🤖 AI Recon Agent[/bold green]\nTarget: [cyan]{args.target}[/cyan]"))

    result = run_recon(args.target)

    output_data = {
        "target": args.target,
        "output": result["output"],
        "steps": len([m for m in result.get("intermediate_steps", []) if hasattr(m, "tool_calls")]),
    }

    if args.save:
        path = save_findings(
            target=args.target,
            findings=output_data,
            reasoning=str(result.get("intermediate_steps", [])),
            summary=result["output"],
        )
        console.print(f"[green]✅ Findings saved to: {path}[/green]")

    if args.output == "markdown":
        console.print(Markdown(result["output"]))
    else:
        syntax = Syntax(json.dumps(output_data, indent=2), "json", theme="monokai")
        console.print(Panel(syntax, title="Findings"))

if __name__ == "__main__":
    main()
