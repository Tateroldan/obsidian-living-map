"""Hook de Claude Code: anota en events.jsonl cada vez que Claude toca la bóveda."""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import LOG, MARCA as BOVEDA, NOMBRE
VERBO = {"Read": "read", "Write": "write", "Edit": "write", "Grep": "search", "Glob": "search"}
QUOTED = re.compile(r"[\"']([^\"'\n]+)[\"']")
BARE = re.compile(r"(?<![\"'])([^\s\"']*" + re.escape(NOMBRE) + r"[^\s\"';|&)]*)", re.I)
ESCRIBE = re.compile(r"(^|[^2&])>\s*\S|sed -i|cat >|Set-Content|Out-File|open\([^)]*[\"']w[\"']|\.write\(")


def rutas(tool, inp):
    if tool not in ("Bash", "PowerShell"):
        return [inp.get(k) for k in ("file_path", "path") if inp.get(k)]
    cmd = inp.get("command", "")[:20000].replace("\\", "/")
    citadas = QUOTED.findall(cmd)
    dirs = [d for d in citadas + BARE.findall(cmd) if BOVEDA in d.lower()]
    if not dirs:
        return []
    out = [d for d in dirs if d.lower().endswith(".md")]
    base = next((d for d in dirs if not d.lower().endswith(".md")), dirs[0]).rstrip("/")
    # notas nombradas de forma relativa dentro del comando: 'Inicio.md', "Aprendizajes/X.md"
    # solo si la nota existe: evita eventos inventados como Boveda/~/.claude/CLAUDE.md
    out += [base + "/" + m for m in citadas if m.lower().endswith(".md") and BOVEDA not in m.lower()
            and os.path.exists(os.path.expandvars(os.path.expanduser(base + "/" + m)))]
    return out or [base]


def main():
    data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})
    verbo = VERBO.get(tool, "touch")
    if tool in ("Bash", "PowerShell"):
        verbo = "write" if ESCRIBE.search(inp.get("command", "")) else "read"
    ag = str(data.get("agent_id") or "")[:12]
    at = str(data.get("agent_type") or "")[:24]
    eventos = []
    for r in dict.fromkeys(rutas(tool, inp)):
        norm = r.replace("\\", "/")
        if BOVEDA in norm.lower():
            eventos.append({"t": time.time(), "verb": verbo, "tool": tool, "path": norm,
                            "session": str(data.get("session_id", ""))[:8]}
                           | ({"agente": ag} if ag else {}) | ({"agent_type": at} if at else {}))
    if eventos:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in eventos))  # una sola escritura


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
