import json
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel
from typing import Any

class ReconFindings(BaseModel):
    target: str
    timestamp: str
    agent_reasoning: str
    findings: dict[str, Any]
    summary: str

def save_findings(target: str, findings: dict, reasoning: str, summary: str) -> Path:
    report = ReconFindings(
        target=target,
        timestamp=datetime.utcnow().isoformat(),
        agent_reasoning=reasoning,
        findings=findings,
        summary=summary,
    )
    out_dir = Path("findings")
    out_dir.mkdir(exist_ok=True)
    safe_name = target.replace(".", "_").replace("/", "_")
    out_path = out_dir / f"{safe_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(report.model_dump_json(indent=2))
    return out_path
