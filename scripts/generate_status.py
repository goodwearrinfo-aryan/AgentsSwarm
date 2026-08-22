#!/usr/bin/env python3
"""
Generate hive status JSON for GitHub Pages.
Reads local hive state and outputs structured JSON.
"""

import json
import os
import glob
import subprocess
from datetime import datetime
from pathlib import Path

HIVE_ROOT = Path("/Users/aryanagarwal/AgentsSwarm/hive")


def read_board():
    """Parse board.md for current status."""
    board_path = HIVE_ROOT / "board.md"
    if not board_path.exists():
        return {}
    content = board_path.read_text()
    return {"raw": content[:5000]}


def read_fleet():
    """Read fleet.json for agent registry."""
    fleet_path = HIVE_ROOT / "fleet.json"
    if not fleet_path.exists():
        return {}
    return json.loads(fleet_path.read_text())


def read_tasks():
    """Read tasks.json for task definitions."""
    tasks_path = HIVE_ROOT / "tasks.json"
    if not tasks_path.exists():
        return {}
    return json.loads(tasks_path.read_text())


def scan_outputs():
    """Scan all agent outputs directories."""
    outputs = []
    for agent_dir in HIVE_ROOT.glob("agents/*/outputs/"):
        if agent_dir.is_dir():
            agent_name = agent_dir.parent.name
            for file_path in agent_dir.rglob("*"):
                if file_path.is_file():
                    stat = file_path.stat()
                    try:
                        content = file_path.read_text()[:500]
                    except Exception:
                        content = "[binary or unreadable]"
                    outputs.append({
                        "agent": agent_name,
                        "file": str(file_path.relative_to(HIVE_ROOT)),
                        "preview": content,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
    return sorted(outputs, key=lambda x: x["modified"], reverse=True)[:20]


def get_ci_status():
    """Get latest CI workflow status."""
    try:
        result = subprocess.run(
            ["gh", "run", "list", "--workflow", "ci.yml", "--limit", "1", "--json", "conclusion,status,createdAt,headBranch"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            runs = json.loads(result.stdout)
            if runs:
                return runs[0]
    except Exception:
        pass
    return {"conclusion": "unknown", "status": "unknown"}


def get_agent_statuses(fleet_data):
    """Extract agent statuses from fleet data."""
    agents = []
    for agent in fleet_data.get("agents", []):
        agents.append({
            "id": agent.get("id"),
            "name": agent.get("name"),
            "role": agent.get("role"),
            "status": agent.get("status", "unknown"),
            "circuit_breaker": agent.get("circuit_breaker", "unknown"),
            "current_task": agent.get("current_task"),
            "inbox_count": agent.get("inbox_count", 0),
            "output_count": agent.get("output_count", 0)
        })
    return agents


def main():
    fleet = read_fleet()
    tasks = read_tasks()
    board = read_board()
    outputs = scan_outputs()
    ci = get_ci_status()
    agents = get_agent_statuses(fleet)

    status = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ci": ci,
        "agents": agents,
        "tasks": tasks.get("tasks", []) if isinstance(tasks, dict) else tasks,
        "recent_outputs": outputs,
        "blocked": [
            {"task": "task-2", "reason": "GitHub Secrets for staging deploy", "owner": "human"},
            {"task": "task-3", "reason": "GPU runner decision (self-hosted vs optional)", "owner": "human"}
        ],
        "circuit_breakers": {
            "all_healthy": all(a.get("circuit_breaker") == "HEALTHY" for a in agents),
            "details": {a["name"]: a["circuit_breaker"] for a in agents}
        },
        "urls": {
            "status_json": "https://goodwearrinfo-aryan.github.io/AgentsSwarm/status.json",
            "html_viewer": "https://goodwearrinfo-aryan.github.io/AgentsSwarm/",
            "repo": "https://github.com/goodwearrinfo-aryan/AgentsSwarm",
            "actions": "https://github.com/goodwearrinfo-aryan/AgentsSwarm/actions"
        }
    }

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()