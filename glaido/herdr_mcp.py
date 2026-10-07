# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=1.12,<2"]  # mcp 2.x renomme FastMCP
# ///
"""Serveur MCP pour piloter Herdr à la voix depuis Glaido (Commands → Custom).

Déclaré dans ~/Glaido/mcp.json, lancé par `uv run --script`.
Variables d'env : HERDR_BIN (défaut /opt/homebrew/bin/herdr),
HERDR_SESSION (vide = session Herdr par défaut).
"""

import json
import os
import secrets
import subprocess
from typing import Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

HERDR = os.environ.get("HERDR_BIN", "/opt/homebrew/bin/herdr")
SESSION = os.environ.get("HERDR_SESSION")

mcp = FastMCP("herdr")


def run(*args: str) -> subprocess.CompletedProcess:
    cmd = [HERDR, *(["--session", SESSION] if SESSION else []), *args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=90)


def herdr(*args: str) -> dict:
    """Appelle une commande herdr qui répond en JSON et renvoie `.result`, ou lève son erreur."""
    proc = run(*args)
    out = proc.stdout.strip() or proc.stderr.strip()
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        raise RuntimeError(f"Réponse inattendue de herdr (le serveur tourne-t-il ? lance `herdr` dans Ghostty) : {out[:200]}")
    if "error" in data:
        raise RuntimeError(f"{data['error']['code']}: {data['error']['message']}")
    return data["result"]


def find_workspace(query: str) -> dict:
    """Trouve un espace par id (w1), par nom exact, ou par nom partiel unique."""
    workspaces = herdr("workspace", "list")["workspaces"]
    q = query.strip().lower()
    for match in (
        lambda w: w["workspace_id"] == query.strip(),
        lambda w: w["label"].lower() == q,
        lambda w: q in w["label"].lower(),
    ):
        found = [w for w in workspaces if match(w)]
        if len(found) == 1:
            return found[0]
    labels = ", ".join(w["label"] for w in workspaces) or "aucun"
    raise ValueError(f"Espace « {query} » introuvable ou ambigu. Espaces disponibles : {labels}")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_workspaces() -> list[dict]:
    """Liste les espaces de travail Herdr (un par projet) et l'état de leurs agents."""
    agents = herdr("agent", "list")["agents"]
    return [
        {
            "id": w["workspace_id"],
            "nom": w["label"],
            "agents": [
                {"nom": a.get("name"), "type": a["agent"], "état": a["agent_status"]}
                for a in agents
                if a["workspace_id"] == w["workspace_id"]
            ],
        }
        for w in herdr("workspace", "list")["workspaces"]
    ]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def start_agent(workspace: str, task: str, kind: Literal["claude", "codex"] = "claude") -> dict:
    """Lance un agent de code dans un nouvel onglet d'un espace Herdr, en arrière-plan,
    avec une tâche. `workspace` = nom de l'espace (ex. « dotfiles »), `task` = la consigne."""
    ws = find_workspace(workspace)
    name = f"{kind}-{secrets.token_hex(2)}"
    tab = herdr("tab", "create", "--workspace", ws["workspace_id"], "--label", name, "--no-focus")
    pane = tab["root_pane"]["pane_id"]
    # La tâche est passée au lancement : si l'agent demande d'abord une confirmation
    # (dossier non approuvé…), elle part dès que l'utilisateur a validé dans Herdr.
    try:
        herdr("agent", "start", name, "--kind", kind, "--pane", pane, "--", task)
        status, message = "en cours", f"Agent {name} lancé dans « {ws['label']} »."
    except RuntimeError as e:
        if not str(e).startswith("agent_not_ready"):
            raise
        status = "en attente"
        message = f"Agent {name} lancé dans « {ws['label']} », mais il attend une confirmation dans Herdr."
    return {"agent": name, "espace": ws["label"], "onglet": tab["tab"]["tab_id"], "état": status, "message": message}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def agent_status(agent: str, lines: int = 40) -> dict:
    """Donne l'état d'un agent Herdr (working, blocked, done, idle) et ses dernières lignes de sortie."""
    state = herdr("agent", "get", agent)["agent"]["agent_status"]
    # `agent read` répond en texte brut, pas en JSON
    output = run("agent", "read", agent, "--source", "recent-unwrapped", "--lines", str(lines)).stdout.strip()
    return {"agent": agent, "état": state, "sortie": output}


if __name__ == "__main__":
    mcp.run()
