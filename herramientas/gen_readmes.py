"""Genera README.md (en) y README.<codigo>.md para los 8 idiomas del mapa.
Uso: python herramientas/gen_readmes.py  (edita los textos en el diccionario T y vuelve a correr)."""
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz del repo
NAMES = [("en", "English", "README.md"), ("es", "Español", "README.es.md"), ("pt", "Português", "README.pt.md"),
         ("fr", "Français", "README.fr.md"), ("de", "Deutsch", "README.de.md"), ("it", "Italiano", "README.it.md"),
         ("ja", "日本語", "README.ja.md"), ("zh", "中文", "README.zh.md")]

JSON = '''```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Read|Write|Edit|Grep|Glob|Bash|PowerShell",
        "hooks": [{ "type": "command", "command": "python \\"PATH/obsidian-living-map/hook.py\\"" }] }
    ]
  }
}
```'''

T = {
"en": dict(
 intro="3D map of your Obsidian vault where a spider walks the notes that Claude Code reads (cyan), writes (amber) or searches (violet). It costs no tokens: a `PostToolUse` hook logs every access to `events.jsonl` and the page polls it every 0.8 s. Python standard library only, no `pip install`.",
 h_install="Install",
 s1="Clone the repo and open `abrir.cmd` (or run `python server.py --abrir`). It opens http://127.0.0.1:8765.",
 s2="If your vault is not at `~/Documents/Boveda`, set `MAPA_BOVEDA` to its path. Change the port with `MAPA_PUERTO` and the note with open checkboxes with `MAPA_DECISIONES`. Everything lives in `config.py`.\n   For `validar.py`, copy `reglas.ejemplo.json` to `reglas.json` and adjust types, areas and states to your vault (`reglas.json` is not committed).",
 s3="To watch Claude move, add the hook to `~/.claude/settings.json`:",
 opt="Optional: `validar.py` (PostToolUse `Write|Edit`; warns about missing properties, broken links or pasted secrets) and `diario.py` (SessionEnd; summarizes the session in the daily note).",
 h_parts="Parts", c1="File", c2="Purpose",
 rows=["rules for `validar.py` (allowed properties, forbidden mixes)", "vault path, port and log (the only place with paths)",
       "local server; serves only the page and its pieces, checks `Host`", "PostToolUse → `events.jsonl`",
       "orphan notes and never-touched notes", "validate on write, neighbors/path/topic, automatic daily note",
       "camera and graph, spider with IK, 6 palettes, 8 languages, panels"],
 url="URL parameters: `?tema=rgb&lang=en`. Click a note to open it in Obsidian; double-click to focus it.",
 h_priv="Privacy", priv="Everything runs on `127.0.0.1`. `events.jsonl` stores your note paths; it is in `.gitignore`.",
 h_3p="Third-party licenses", h_lic="License", lic="Apache-2.0, see `LICENSE`."),
"es": dict(
 intro="Mapa 3D de tu bóveda de Obsidian donde una araña camina por las notas que Claude Code lee (cian), escribe (ámbar) o busca (violeta). No gasta tokens: un hook `PostToolUse` anota cada acceso en `events.jsonl` y la página lo consulta cada 0.8 s. Solo Python estándar, sin `pip install`.",
 h_install="Instalar",
 s1="Clona el repo y abre `abrir.cmd` (o `python server.py --abrir`). Se abre http://127.0.0.1:8765.",
 s2="Si tu bóveda no está en `~/Documents/Boveda`, define `MAPA_BOVEDA` con su ruta. El puerto se cambia con `MAPA_PUERTO` y la nota de casillas abiertas con `MAPA_DECISIONES`. Todo vive en `config.py`.\n   Para `validar.py`, copia `reglas.ejemplo.json` a `reglas.json` y ajusta tipos, áreas y estados a tu bóveda (`reglas.json` no se sube).",
 s3="Para ver a Claude moverse, agrega el hook a `~/.claude/settings.json`:",
 opt="Opcionales: `validar.py` (PostToolUse `Write|Edit`; avisa de propiedades faltantes, enlaces rotos o secretos pegados) y `diario.py` (SessionEnd; resume la sesión en la nota diaria).",
 h_parts="Piezas", c1="Archivo", c2="Para qué",
 rows=["reglas de `validar.py` (propiedades permitidas, mezclas prohibidas)", "ruta de la bóveda, puerto y log (único lugar con rutas)",
       "servidor local; solo sirve la página y sus piezas, revisa `Host`", "PostToolUse → `events.jsonl`",
       "huérfanas y notas nunca tocadas", "validar al escribir, vecinos/camino/tema, diario automático",
       "cámara y grafo, araña con IK, 6 paletas, 8 idiomas, paneles"],
 url="Parámetros de URL: `?tema=rgb&lang=en`. Clic en una nota la abre en Obsidian; doble clic la enfoca.",
 h_priv="Privacidad", priv="Todo corre en `127.0.0.1`. `events.jsonl` guarda rutas de tus notas; está en `.gitignore`.",
 h_3p="Licencias de terceros", h_lic="Licencia", lic="Apache-2.0, ver `LICENSE`."),
"pt": dict(
 intro="Mapa 3D do seu cofre do Obsidian em que uma aranha caminha pelas notas que o Claude Code lê (ciano), escreve (âmbar) ou busca (violeta). Não gasta tokens: um hook `PostToolUse` registra cada acesso em `events.jsonl` e a página o consulta a cada 0,8 s. Apenas biblioteca padrão do Python, sem `pip install`.",
 h_install="Instalação",
 s1="Clone o repositório e abra `abrir.cmd` (ou execute `python server.py --abrir`). Abre http://127.0.0.1:8765.",
 s2="Se o seu cofre não está em `~/Documents/Boveda`, defina `MAPA_BOVEDA` com o caminho dele. A porta muda com `MAPA_PUERTO` e a nota com caixas abertas com `MAPA_DECISIONES`. Tudo fica em `config.py`.\n   Para o `validar.py`, copie `reglas.ejemplo.json` para `reglas.json` e ajuste tipos, áreas e estados ao seu cofre (`reglas.json` não é enviado).",
 s3="Para ver o Claude se mover, adicione o hook em `~/.claude/settings.json`:",
 opt="Opcionais: `validar.py` (PostToolUse `Write|Edit`; avisa sobre propriedades ausentes, links quebrados ou segredos colados) e `diario.py` (SessionEnd; resume a sessão na nota diária).",
 h_parts="Peças", c1="Arquivo", c2="Para quê",
 rows=["regras do `validar.py` (propriedades permitidas, misturas proibidas)", "caminho do cofre, porta e log (único lugar com caminhos)",
       "servidor local; serve só a página e suas peças, confere o `Host`", "PostToolUse → `events.jsonl`",
       "notas órfãs e nunca tocadas", "validar ao escrever, vizinhos/caminho/tema, nota diária automática",
       "câmera e grafo, aranha com IK, 6 paletas, 8 idiomas, painéis"],
 url="Parâmetros de URL: `?tema=rgb&lang=pt`. Clique numa nota para abri-la no Obsidian; clique duplo para focar.",
 h_priv="Privacidade", priv="Tudo roda em `127.0.0.1`. `events.jsonl` guarda os caminhos das suas notas; está no `.gitignore`.",
 h_3p="Licenças de terceiros", h_lic="Licença", lic="Apache-2.0, veja `LICENSE`."),
"fr": dict(
 intro="Carte 3D de votre coffre Obsidian où une araignée parcourt les notes que Claude Code lit (cyan), écrit (ambre) ou recherche (violet). Elle ne consomme aucun token : un hook `PostToolUse` consigne chaque accès dans `events.jsonl` et la page l'interroge toutes les 0,8 s. Bibliothèque standard Python uniquement, sans `pip install`.",
 h_install="Installation",
 s1="Clonez le dépôt et ouvrez `abrir.cmd` (ou lancez `python server.py --abrir`). Cela ouvre http://127.0.0.1:8765.",
 s2="Si votre coffre n'est pas dans `~/Documents/Boveda`, définissez `MAPA_BOVEDA` avec son chemin. Le port se change avec `MAPA_PUERTO` et la note de cases ouvertes avec `MAPA_DECISIONES`. Tout se trouve dans `config.py`.\n   Pour `validar.py`, copiez `reglas.ejemplo.json` en `reglas.json` et adaptez types, zones et états à votre coffre (`reglas.json` n'est pas versionné).",
 s3="Pour voir Claude se déplacer, ajoutez le hook à `~/.claude/settings.json` :",
 opt="Optionnels : `validar.py` (PostToolUse `Write|Edit` ; signale propriétés manquantes, liens cassés ou secrets collés) et `diario.py` (SessionEnd ; résume la session dans la note du jour).",
 h_parts="Composants", c1="Fichier", c2="Rôle",
 rows=["règles de `validar.py` (propriétés autorisées, mélanges interdits)", "chemin du coffre, port et journal (seul endroit avec des chemins)",
       "serveur local ; ne sert que la page et ses pièces, vérifie `Host`", "PostToolUse → `events.jsonl`",
       "notes orphelines et jamais touchées", "valider à l'écriture, voisins/chemin/thème, note du jour automatique",
       "caméra et graphe, araignée à cinématique inverse, 6 palettes, 8 langues, panneaux"],
 url="Paramètres d'URL : `?tema=rgb&lang=fr`. Un clic sur une note l'ouvre dans Obsidian ; un double-clic la met au point.",
 h_priv="Confidentialité", priv="Tout tourne sur `127.0.0.1`. `events.jsonl` contient les chemins de vos notes ; il est dans `.gitignore`.",
 h_3p="Licences tierces", h_lic="Licence", lic="Apache-2.0, voir `LICENSE`."),
"de": dict(
 intro="3D-Karte deines Obsidian-Vaults, auf der eine Spinne über die Notizen läuft, die Claude Code liest (Cyan), schreibt (Bernstein) oder durchsucht (Violett). Sie kostet keine Tokens: Ein `PostToolUse`-Hook protokolliert jeden Zugriff in `events.jsonl`, und die Seite fragt ihn alle 0,8 s ab. Nur die Python-Standardbibliothek, kein `pip install`.",
 h_install="Installation",
 s1="Klone das Repo und öffne `abrir.cmd` (oder starte `python server.py --abrir`). Es öffnet http://127.0.0.1:8765.",
 s2="Liegt dein Vault nicht unter `~/Documents/Boveda`, setze `MAPA_BOVEDA` auf seinen Pfad. Den Port änderst du mit `MAPA_PUERTO`, die Notiz mit offenen Kästchen mit `MAPA_DECISIONES`. Alles steht in `config.py`.\n   Für `validar.py` kopiere `reglas.ejemplo.json` nach `reglas.json` und passe Typen, Bereiche und Status an deinen Vault an (`reglas.json` wird nicht eingecheckt).",
 s3="Damit du Claude beim Laufen siehst, füge den Hook in `~/.claude/settings.json` ein:",
 opt="Optional: `validar.py` (PostToolUse `Write|Edit`; warnt vor fehlenden Eigenschaften, kaputten Links oder eingefügten Geheimnissen) und `diario.py` (SessionEnd; fasst die Sitzung in der Tagesnotiz zusammen).",
 h_parts="Bestandteile", c1="Datei", c2="Zweck",
 rows=["Regeln für `validar.py` (erlaubte Eigenschaften, verbotene Mischungen)", "Vault-Pfad, Port und Log (einziger Ort mit Pfaden)",
       "lokaler Server; liefert nur die Seite und ihre Teile, prüft `Host`", "PostToolUse → `events.jsonl`",
       "verwaiste und nie berührte Notizen", "beim Schreiben validieren, Nachbarn/Pfad/Thema, automatische Tagesnotiz",
       "Kamera und Graph, Spinne mit IK, 6 Paletten, 8 Sprachen, Panels"],
 url="URL-Parameter: `?tema=rgb&lang=de`. Klick auf eine Notiz öffnet sie in Obsidian; Doppelklick fokussiert sie.",
 h_priv="Datenschutz", priv="Alles läuft auf `127.0.0.1`. `events.jsonl` speichert die Pfade deiner Notizen; sie steht in `.gitignore`.",
 h_3p="Lizenzen Dritter", h_lic="Lizenz", lic="Apache-2.0, siehe `LICENSE`."),
"it": dict(
 intro="Mappa 3D del tuo vault di Obsidian in cui un ragno cammina sulle note che Claude Code legge (ciano), scrive (ambra) o cerca (viola). Non consuma token: un hook `PostToolUse` registra ogni accesso in `events.jsonl` e la pagina lo interroga ogni 0,8 s. Solo libreria standard di Python, nessun `pip install`.",
 h_install="Installazione",
 s1="Clona il repository e apri `abrir.cmd` (oppure esegui `python server.py --abrir`). Si apre http://127.0.0.1:8765.",
 s2="Se il tuo vault non è in `~/Documents/Boveda`, imposta `MAPA_BOVEDA` con il suo percorso. La porta si cambia con `MAPA_PUERTO` e la nota con caselle aperte con `MAPA_DECISIONES`. Tutto sta in `config.py`.\n   Per `validar.py`, copia `reglas.ejemplo.json` in `reglas.json` e adatta tipi, aree e stati al tuo vault (`reglas.json` non viene committato).",
 s3="Per vedere Claude muoversi, aggiungi l'hook a `~/.claude/settings.json`:",
 opt="Opzionali: `validar.py` (PostToolUse `Write|Edit`; avvisa di proprietà mancanti, link rotti o segreti incollati) e `diario.py` (SessionEnd; riassume la sessione nella nota giornaliera).",
 h_parts="Componenti", c1="File", c2="A cosa serve",
 rows=["regole di `validar.py` (proprietà ammesse, mescolanze vietate)", "percorso del vault, porta e log (unico posto con percorsi)",
       "server locale; serve solo la pagina e i suoi pezzi, controlla `Host`", "PostToolUse → `events.jsonl`",
       "note orfane e mai toccate", "validare in scrittura, vicini/percorso/tema, nota giornaliera automatica",
       "camera e grafo, ragno con IK, 6 palette, 8 lingue, pannelli"],
 url="Parametri URL: `?tema=rgb&lang=it`. Un clic su una nota la apre in Obsidian; doppio clic la mette a fuoco.",
 h_priv="Privacy", priv="Tutto gira su `127.0.0.1`. `events.jsonl` contiene i percorsi delle tue note; è nel `.gitignore`.",
 h_3p="Licenze di terzi", h_lic="Licenza", lic="Apache-2.0, vedi `LICENSE`."),
"ja": dict(
 intro="Claude Code が読む(シアン)・書く(琥珀)・検索する(紫)ノートの上をクモが歩く、Obsidian ボールトの 3D マップです。トークンは消費しません。`PostToolUse` フックがすべてのアクセスを `events.jsonl` に記録し、ページが 0.8 秒ごとに読み取ります。Python 標準ライブラリのみで、`pip install` は不要です。",
 h_install="インストール",
 s1="リポジトリをクローンし、`abrir.cmd` を開きます(または `python server.py --abrir`)。http://127.0.0.1:8765 が開きます。",
 s2="ボールトが `~/Documents/Boveda` にない場合は、`MAPA_BOVEDA` にそのパスを設定します。ポートは `MAPA_PUERTO`、未完了チェックボックスのあるノートは `MAPA_DECISIONES` で変更できます。設定はすべて `config.py` にあります。\n   `validar.py` を使うには、`reglas.ejemplo.json` を `reglas.json` にコピーし、種類・エリア・状態をボールトに合わせて調整します(`reglas.json` はコミットされません)。",
 s3="Claude の動きを見るには、`~/.claude/settings.json` にフックを追加します:",
 opt="任意: `validar.py`(PostToolUse `Write|Edit`。プロパティ欠落、壊れたリンク、貼り付けられた秘密情報を警告)と `diario.py`(SessionEnd。セッションをデイリーノートに要約)。",
 h_parts="構成", c1="ファイル", c2="役割",
 rows=["`validar.py` のルール(許可するプロパティ、禁止する混在)", "ボールトのパス、ポート、ログ(パスを持つ唯一の場所)",
       "ローカルサーバー。ページと関連ファイルのみ配信し、`Host` を検証", "PostToolUse → `events.jsonl`",
       "孤立ノートと一度も触れられていないノート", "書き込み時の検証、近傍/経路/テーマ、デイリーノートの自動生成",
       "カメラとグラフ、IK のクモ、6 つのパレット、8 言語、パネル"],
 url="URL パラメータ: `?tema=rgb&lang=ja`。ノートをクリックすると Obsidian で開き、ダブルクリックでフォーカスします。",
 h_priv="プライバシー", priv="すべて `127.0.0.1` 上で動作します。`events.jsonl` にはノートのパスが保存されますが、`.gitignore` に入っています。",
 h_3p="サードパーティのライセンス", h_lic="ライセンス", lic="Apache-2.0。`LICENSE` を参照してください。"),
"zh": dict(
 intro="你的 Obsidian 知识库的 3D 地图:一只蜘蛛在 Claude Code 读取(青色)、写入(琥珀色)或搜索(紫色)的笔记上行走。不消耗 token:`PostToolUse` 钩子把每次访问记录到 `events.jsonl`,页面每 0.8 秒读取一次。仅使用 Python 标准库,无需 `pip install`。",
 h_install="安装",
 s1="克隆仓库并打开 `abrir.cmd`(或运行 `python server.py --abrir`),会打开 http://127.0.0.1:8765。",
 s2="如果你的知识库不在 `~/Documents/Boveda`,请把 `MAPA_BOVEDA` 设为其路径。端口用 `MAPA_PUERTO` 修改,含未完成复选框的笔记用 `MAPA_DECISIONES` 指定。所有设置都在 `config.py`。\n   使用 `validar.py` 时,把 `reglas.ejemplo.json` 复制为 `reglas.json`,并按你的知识库调整类型、领域和状态(`reglas.json` 不会提交)。",
 s3="想看到 Claude 的移动,请把钩子添加到 `~/.claude/settings.json`:",
 opt="可选:`validar.py`(PostToolUse `Write|Edit`;提示缺失属性、失效链接或粘贴的密钥)和 `diario.py`(SessionEnd;把会话摘要写入当日笔记)。",
 h_parts="组成", c1="文件", c2="用途",
 rows=["`validar.py` 的规则(允许的属性、禁止的混用)", "知识库路径、端口和日志(唯一包含路径的位置)",
       "本地服务器;只提供页面及其组件,并检查 `Host`", "PostToolUse → `events.jsonl`",
       "孤立笔记和从未被触及的笔记", "写入时校验、邻居/路径/主题、自动生成当日笔记",
       "相机与图谱、带 IK 的蜘蛛、6 种配色、8 种语言、面板"],
 url="URL 参数:`?tema=rgb&lang=zh`。单击笔记在 Obsidian 中打开,双击则聚焦。",
 h_priv="隐私", priv="一切都在 `127.0.0.1` 上运行。`events.jsonl` 保存你的笔记路径,已加入 `.gitignore`。",
 h_3p="第三方许可", h_lic="许可证", lic="Apache-2.0,见 `LICENSE`。"),
}

FILES = ["reglas.ejemplo.json", "config.py", "server.py", "hook.py", "salud.py", "validar.py`, `vecinos.py`, `diario.py",
         "mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js"]
AUTO = {'en': 'The first time you open it from a console it asks, once, whether to start automatically with Windows. Change it later with `python server.py --autoarranque on|off|estado`.', 'es': 'La primera vez que lo abres desde una consola pregunta, una sola vez, si quieres que arranque con Windows. Cámbialo después con `python server.py --autoarranque on|off|estado`.', 'pt': 'Na primeira vez que o abrir por um console, ele pergunta uma única vez se deve iniciar com o Windows. Mude depois com `python server.py --autoarranque on|off|estado`.', 'fr': "La première fois que vous l'ouvrez depuis une console, il demande une seule fois s'il doit démarrer avec Windows. Modifiez-le ensuite avec `python server.py --autoarranque on|off|estado`.", 'de': 'Beim ersten Start aus einer Konsole wird einmalig gefragt, ob der Server mit Windows starten soll. Später änderbar mit `python server.py --autoarranque on|off|estado`.', 'it': 'La prima volta che lo apri da una console chiede, una sola volta, se avviarsi con Windows. Cambialo dopo con `python server.py --autoarranque on|off|estado`.', 'ja': 'コンソールから初めて開くと、Windows 起動時に自動で開始するかどうかを一度だけ尋ねます。後から `python server.py --autoarranque on|off|estado` で変更できます。', 'zh': '首次从控制台打开时,会询问一次是否随 Windows 自动启动。之后可用 `python server.py --autoarranque on|off|estado` 更改。'}
SUP = {'en': ('Support', 'If it is useful to you, you can [buy me a coffee on Ko-fi](https://ko-fi.com/tateroldan) ☕'), 'es': ('Apoyo', 'Si te sirve, puedes [invitarme un café en Ko-fi](https://ko-fi.com/tateroldan) ☕'), 'pt': ('Apoio', 'Se for útil para você, pode [me pagar um café no Ko-fi](https://ko-fi.com/tateroldan) ☕'), 'fr': ('Soutien', "Si cela vous est utile, vous pouvez [m'offrir un café sur Ko-fi](https://ko-fi.com/tateroldan) ☕"), 'de': ('Unterstützung', 'Wenn es dir nützt, kannst du mir [auf Ko-fi einen Kaffee spendieren](https://ko-fi.com/tateroldan) ☕'), 'it': ('Supporto', 'Se ti è utile, puoi [offrirmi un caffè su Ko-fi](https://ko-fi.com/tateroldan) ☕'), 'ja': ('サポート', '役に立ったら、[Ko-fi でコーヒーをおごる](https://ko-fi.com/tateroldan)こともできます ☕'), 'zh': ('支持', '如果它对你有帮助,可以在 [Ko-fi 请我喝杯咖啡](https://ko-fi.com/tateroldan) ☕')}
KIT = {'en': ('Kit (the self-learning part)', 'The map shows what Claude touches; `kit/` gives Claude the working method that makes the vault grow on its own: rules for starting and finishing tasks, linked notes ("neurons"), a librarian agent, a zero-token inbox router, a closing skill and a sample vault. No one\'s personal notes are included. Preview with `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`). Details: [kit/LEEME.md](kit/LEEME.md).'), 'es': ('Kit (la parte autodidacta)', 'El mapa muestra qué toca Claude; `kit/` le da a Claude la forma de trabajar que hace crecer la bóveda sola: reglas para empezar y terminar tareas, notas enlazadas («neuronas»), un agente bibliotecario, un router de bandeja sin tokens, una skill de cierre y una bóveda de ejemplo. No incluye notas personales de nadie. Vista previa con `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`). Detalle: [kit/LEEME.md](kit/LEEME.md).'), 'pt': ('Kit (a parte autodidata)', 'O mapa mostra o que o Claude toca; `kit/` dá ao Claude o método de trabalho que faz o cofre crescer sozinho: regras para começar e terminar tarefas, notas ligadas («neurônios»), um agente bibliotecário, um roteador de caixa de entrada sem tokens, uma skill de encerramento e um cofre de exemplo. Não inclui notas pessoais de ninguém. Prévia com `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`). Detalhes: [kit/LEEME.md](kit/LEEME.md).'), 'fr': ('Kit (la partie autodidacte)', "La carte montre ce que Claude touche ; `kit/` lui donne la méthode de travail qui fait grandir le coffre tout seul : règles pour commencer et finir les tâches, notes liées (« neurones »), un agent bibliothécaire, un routeur de boîte de réception sans tokens, une skill de clôture et un coffre d'exemple. Aucune note personnelle n'est incluse. Aperçu avec `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`). Détails : [kit/LEEME.md](kit/LEEME.md)."), 'de': ('Kit (der selbstlernende Teil)', 'Die Karte zeigt, was Claude berührt; `kit/` gibt Claude die Arbeitsweise, mit der der Vault von selbst wächst: Regeln für Beginn und Abschluss von Aufgaben, verknüpfte Notizen („Neuronen“), ein Bibliothekar-Agent, ein Posteingangs-Router ohne Tokens, eine Abschluss-Skill und ein Beispiel-Vault. Keine persönlichen Notizen sind enthalten. Vorschau mit `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`). Details: [kit/LEEME.md](kit/LEEME.md).'), 'it': ('Kit (la parte autodidatta)', 'La mappa mostra cosa tocca Claude; `kit/` gli dà il metodo di lavoro che fa crescere il vault da solo: regole per iniziare e chiudere i compiti, note collegate («neuroni»), un agente bibliotecario, un router della casella senza token, una skill di chiusura e un vault di esempio. Nessuna nota personale inclusa. Anteprima con `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`). Dettagli: [kit/LEEME.md](kit/LEEME.md).'), 'ja': ('キット(自己学習の部分)', 'マップは Claude が何に触れるかを見せ、`kit/` はボールトが自然に育つ作業方法を Claude に与えます。タスク開始・終了のルール、リンクされたノート(「ニューロン」)、司書エージェント、トークン不要の受信箱ルーター、終了スキル、サンプルボールトが含まれます。個人のノートは一切含まれません。`python kit/instalar.py --simulacro` (`--lang en` / `--lang es`) でプレビューできます。詳細: [kit/LEEME.md](kit/LEEME.md)。'), 'zh': ('套件(自学习部分)', '地图展示 Claude 触及了什么;`kit/` 则赋予 Claude 让知识库自行生长的工作方法:任务开始与结束的规则、相互链接的笔记(“神经元”)、图书管理员代理、无需 token 的收件箱路由器、收尾技能和示例知识库。不包含任何人的个人笔记。可用 `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`) 预览。详情:[kit/LEEME.md](kit/LEEME.md)。')}
# Requisitos: van antes de instalar (Obsidian, Python y Claude Code)
REQ = {
'en': ('Requirements', [
  '**Obsidian** (free): download it from [obsidian.md](https://obsidian.md), then use *Open folder as vault* and pick your vault folder. If you use the kit, pick the folder it creates (`MAPA_BOVEDA`, default `~/Documents/Boveda`). Clicking a note in the map opens it in Obsidian.',
  '**Python 3.9+**: standard library only, no `pip install`.',
  '**[Claude Code](https://claude.com/claude-code)**: the hook records what it reads and writes; without it the map shows the vault but no spider moves.']),
'es': ('Requisitos', [
  '**Obsidian** (gratis): descárgalo de [obsidian.md](https://obsidian.md) y usa *Open folder as vault* («Abrir carpeta como bóveda») con la carpeta de tu bóveda. Si usas el kit, elige la carpeta que crea (`MAPA_BOVEDA`, por defecto `~/Documents/Boveda`). Al hacer clic en una nota del mapa, se abre en Obsidian.',
  '**Python 3.9+**: solo biblioteca estándar, sin `pip install`.',
  '**[Claude Code](https://claude.com/claude-code)**: el hook registra lo que lee y escribe; sin él, el mapa muestra la bóveda pero ninguna araña se mueve.']),
'pt': ('Requisitos', [
  '**Obsidian** (gratuito): baixe em [obsidian.md](https://obsidian.md) e use *Open folder as vault* com a pasta do seu cofre. Se usar o kit, escolha a pasta que ele cria (`MAPA_BOVEDA`, padrão `~/Documents/Boveda`). Clicar numa nota do mapa a abre no Obsidian.',
  '**Python 3.9+**: só a biblioteca padrão, sem `pip install`.',
  '**[Claude Code](https://claude.com/claude-code)**: o hook registra o que ele lê e escreve; sem ele, o mapa mostra o cofre mas nenhuma aranha se move.']),
'fr': ('Prérequis', [
  "**Obsidian** (gratuit) : téléchargez-le sur [obsidian.md](https://obsidian.md), puis *Open folder as vault* avec le dossier de votre coffre. Avec le kit, choisissez le dossier qu'il crée (`MAPA_BOVEDA`, par défaut `~/Documents/Boveda`). Un clic sur une note de la carte l'ouvre dans Obsidian.",
  '**Python 3.9+** : bibliothèque standard uniquement, sans `pip install`.',
  "**[Claude Code](https://claude.com/claude-code)** : le hook enregistre ce qu'il lit et écrit ; sans lui, la carte montre le coffre mais aucune araignée ne bouge."]),
'de': ('Voraussetzungen', [
  '**Obsidian** (kostenlos): von [obsidian.md](https://obsidian.md) herunterladen und mit *Open folder as vault* deinen Vault-Ordner öffnen. Mit dem Kit wählst du den Ordner, den es anlegt (`MAPA_BOVEDA`, Standard `~/Documents/Boveda`). Ein Klick auf eine Notiz in der Karte öffnet sie in Obsidian.',
  '**Python 3.9+**: nur Standardbibliothek, kein `pip install`.',
  '**[Claude Code](https://claude.com/claude-code)**: der Hook protokolliert, was es liest und schreibt; ohne ihn zeigt die Karte den Vault, aber keine Spinne bewegt sich.']),
'it': ('Requisiti', [
  '**Obsidian** (gratuito): scaricalo da [obsidian.md](https://obsidian.md) e usa *Open folder as vault* con la cartella del tuo vault. Con il kit, scegli la cartella che crea (`MAPA_BOVEDA`, predefinita `~/Documents/Boveda`). Un clic su una nota della mappa la apre in Obsidian.',
  '**Python 3.9+**: solo libreria standard, nessun `pip install`.',
  '**[Claude Code](https://claude.com/claude-code)**: il hook registra ciò che legge e scrive; senza, la mappa mostra il vault ma nessun ragno si muove.']),
'ja': ('必要なもの', [
  '**Obsidian**(無料): [obsidian.md](https://obsidian.md) からダウンロードし、*Open folder as vault* でボールトのフォルダーを開きます。キットを使う場合は、キットが作るフォルダー(`MAPA_BOVEDA`、既定は `~/Documents/Boveda`)を選びます。マップでノートをクリックすると Obsidian で開きます。',
  '**Python 3.9+**: 標準ライブラリのみ、`pip install` 不要。',
  '**[Claude Code](https://claude.com/claude-code)**: フックが読み書きを記録します。これがないとマップはボールトを表示しますが、クモは動きません。']),
'zh': ('环境要求', [
  '**Obsidian**(免费):从 [obsidian.md](https://obsidian.md) 下载,然后用 *Open folder as vault* 打开你的知识库文件夹。使用套件时,选择它创建的文件夹(`MAPA_BOVEDA`,默认 `~/Documents/Boveda`)。在地图中点击笔记会在 Obsidian 中打开。',
  '**Python 3.9+**:仅用标准库,无需 `pip install`。',
  '**[Claude Code](https://claude.com/claude-code)**:钩子记录它读写的内容;没有它,地图会显示知识库,但蜘蛛不会移动。']),
}
# Guía para principiantes: enlace arriba de todo
START = {'en': '**New to this?** Follow the [step-by-step beginner guide](BEGINNERS.md): no coding needed.',
 'es': '**¿Empiezas desde cero?** Sigue la [guía paso a paso para principiantes](PRINCIPIANTES.md): no hace falta programar.',
 'pt': '**Começando do zero?** Siga o [guia passo a passo para iniciantes](BEGINNERS.md) (em inglês; [em espanhol](PRINCIPIANTES.md)).',
 'fr': '**Vous débutez ?** Suivez le [guide pas à pas pour débutants](BEGINNERS.md) (en anglais ; [en espagnol](PRINCIPIANTES.md)).',
 'de': '**Neu dabei?** Folge der [Schritt-für-Schritt-Anleitung für Einsteiger](BEGINNERS.md) (auf Englisch; [auf Spanisch](PRINCIPIANTES.md)).',
 'it': '**Parti da zero?** Segui la [guida passo passo per principianti](BEGINNERS.md) (in inglese; [in spagnolo](PRINCIPIANTES.md)).',
 'ja': '**初めての方へ:** [初心者向けステップバイステップガイド](BEGINNERS.md)(英語。[スペイン語版](PRINCIPIANTES.md))をどうぞ。プログラミング不要です。',
 'zh': '**新手?** 请按照[分步新手指南](BEGINNERS.md)操作(英文;[西班牙文版](PRINCIPIANTES.md)),无需编程。'}
THIRD = ["d3 7.9.0 (ISC), `vendor/`", "Departure Mono v1.500 (SIL OFL), `fuentes/`"]

for code, nombre, fname in NAMES:
    t = T[code]
    nav = " · ".join(n if c == code else "[%s](%s)" % (n, f) for c, n, f in NAMES)
    rows = "\n".join("| `%s` | %s |" % (f, r) for f, r in zip(FILES, t["rows"]))
    doc = f"""# Obsidian Living Map

[![pruebas](https://github.com/Tateroldan/obsidian-living-map/actions/workflows/pruebas.yml/badge.svg)](https://github.com/Tateroldan/obsidian-living-map/actions/workflows/pruebas.yml)

{nav}

{t['intro']}

{START[code]}

## {REQ[code][0]}

{chr(10).join("- " + x for x in REQ[code][1])}

## {t['h_install']}

1. {t['s1']}
2. {t['s2']}
3. {t['s3']}

{JSON}

{t['opt']}

{AUTO[code]}

## {t['h_parts']}

| {t['c1']} | {t['c2']} |
|---|---|
{rows}

{t['url']}

## {t['h_priv']}

{t['priv']}

## {KIT[code][0]}

{KIT[code][1] if code == 'es' else KIT[code][1].replace('kit/LEEME.md', 'kit/README.md')}

## {SUP[code][0]}

{SUP[code][1]}

## {t['h_3p']}

- {THIRD[0]}
- {THIRD[1]}

## {t['h_lic']}

{t['lic']}
"""
    with open(os.path.join(OUT, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
print("ok", len(NAMES))
