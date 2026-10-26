# Obsidian Living Map

[![pruebas](https://github.com/Tateroldan/obsidian-living-map/actions/workflows/pruebas.yml/badge.svg)](https://github.com/Tateroldan/obsidian-living-map/actions/workflows/pruebas.yml)

[English](README.md) · [Español](README.es.md) · Português · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [中文](README.zh.md)

Mapa 3D do seu cofre do Obsidian em que uma aranha caminha pelas notas que o Claude Code lê (ciano), escreve (âmbar) ou busca (violeta). Não gasta tokens: um hook `PostToolUse` registra cada acesso em `events.jsonl` e a página o consulta a cada 0,8 s. Apenas biblioteca padrão do Python, sem `pip install`.

**Começando do zero?** Siga o [guia passo a passo para iniciantes](BEGINNERS.md) (em inglês; [em espanhol](PRINCIPIANTES.md)).

## Requisitos

- **Obsidian** (gratuito): baixe em [obsidian.md](https://obsidian.md) e use *Open folder as vault* com a pasta do seu cofre. Se usar o kit, escolha a pasta que ele cria (`MAPA_BOVEDA`, padrão `~/Documents/Boveda`). Clicar numa nota do mapa a abre no Obsidian.
- **Python 3.9+**: só a biblioteca padrão, sem `pip install`.
- **[Claude Code](https://claude.com/claude-code)**: o hook registra o que ele lê e escreve; sem ele, o mapa mostra o cofre mas nenhuma aranha se move.

## Instalação

1. Clone o repositório e abra `abrir.cmd` (ou execute `python server.py --abrir`). Abre http://127.0.0.1:8765.
2. Se o seu cofre não está em `~/Documents/Boveda`, defina `MAPA_BOVEDA` com o caminho dele. A porta muda com `MAPA_PUERTO` e a nota com caixas abertas com `MAPA_DECISIONES`. Tudo fica em `config.py`.
   Para o `validar.py`, copie `reglas.ejemplo.json` para `reglas.json` e ajuste tipos, áreas e estados ao seu cofre (`reglas.json` não é enviado).
3. Para ver o Claude se mover, adicione o hook em `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Read|Write|Edit|Grep|Glob|Bash|PowerShell",
        "hooks": [{ "type": "command", "command": "python \"PATH/obsidian-living-map/hook.py\"" }] }
    ]
  }
}
```

Opcionais: `validar.py` (PostToolUse `Write|Edit`; avisa sobre propriedades ausentes, links quebrados ou segredos colados) e `diario.py` (SessionEnd; resume a sessão na nota diária).

Na primeira vez que o abrir por um console, ele pergunta uma única vez se deve iniciar com o Windows. Mude depois com `python server.py --autoarranque on|off|estado`.

## Peças

| Arquivo | Para quê |
|---|---|
| `reglas.ejemplo.json` | regras do `validar.py` (propriedades permitidas, misturas proibidas) |
| `config.py` | caminho do cofre, porta e log (único lugar com caminhos) |
| `server.py` | servidor local; serve só a página e suas peças, confere o `Host` |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | notas órfãs e nunca tocadas |
| `validar.py`, `vecinos.py`, `diario.py` | validar ao escrever, vizinhos/caminho/tema, nota diária automática |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | câmera e grafo, aranha com IK, 6 paletas, 8 idiomas, painéis |

Parâmetros de URL: `?tema=rgb&lang=pt`. Clique numa nota para abri-la no Obsidian; clique duplo para focar.

## Privacidade

Tudo roda em `127.0.0.1`. `events.jsonl` guarda os caminhos das suas notas; está no `.gitignore`.

## Kit (a parte autodidata)

O mapa mostra o que o Claude toca; `kit/` dá ao Claude o método de trabalho que faz o cofre crescer sozinho: regras para começar e terminar tarefas, notas ligadas («neurônios»), um agente bibliotecário, um roteador de caixa de entrada sem tokens, uma skill de encerramento e um cofre de exemplo. Não inclui notas pessoais de ninguém. Prévia com `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`). Detalhes: [kit/README.md](kit/README.md).

## Apoio

Se for útil para você, pode [me pagar um café no Ko-fi](https://ko-fi.com/tateroldan) ☕

## Licenças de terceiros

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## Licença

Apache-2.0, veja `LICENSE`.
