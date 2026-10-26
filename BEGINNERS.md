# Getting started (no coding needed)

English · [Español](PRINCIPIANTES.md)

## What it is, in plain words

**Claude Code** is an AI assistant that works on your computer. The catch is that **it forgets everything when the session ends**: each time you have to explain your project, your preferences and what you already tried.

This repo gives it **memory and order**:

- **A notebook that grows on its own** (your Obsidian "vault"). After each task, Claude writes down where it left off, what it learned and what did not work.
- **A working method.** Before starting, Claude reads only the note it needs, not everything.
- **A 3D map** where you watch, live, a spider walking the notes Claude reads and writes.

**What you get:** "let's continue with my project" is enough, and Claude picks up without you repeating anything. Every later session costs less time, fewer explanations and less AI usage.

## What you need (about 20 minutes)

| What | Why | Cost |
|---|---|---|
| Obsidian | See and edit your notebook | Free |
| Python | Runs the map and the installer | Free |
| Claude Code | The assistant | Needs a paid Claude account (Pro or higher) or API credits |

## Step 1: install Obsidian

1. Go to [obsidian.md](https://obsidian.md), download it and install it like any other app.
2. Don't open a vault yet; you will in step 6.

## Step 2: install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version.
2. **On Windows:** on the installer's first screen, **tick "Add python.exe to PATH"** before clicking *Install Now*. Without it, nothing else will work.
3. To check, open a terminal (Windows: Start key, type `PowerShell` and open it; Mac: open the *Terminal* app) and type:
   ```
   python --version
   ```
   (on Mac: `python3 --version`). It must say `Python 3.9` or higher.

## Step 3: install Claude Code

1. Follow the instructions at [claude.com/claude-code](https://claude.com/claude-code) for your system.
2. In the terminal type `claude` and sign in. When you see the box where you type, you're done. Close it with `/exit`.

## Step 4: download this repo

1. At the top of this page on GitHub, click the green **Code → Download ZIP** button.
2. Unzip it into your Documents. You'll get a folder named `obsidian-living-map` (it may end in `-main`).

## Step 5: let Claude install it for you

1. Open a terminal **inside that folder**. Windows: open the folder, right-click an empty spot and choose **Open in Terminal**. Mac: right-click the folder → **Services → New Terminal at Folder**.
2. Type `claude` and paste this message as is:

```
I'm a beginner. Install this repo for me step by step, explaining in plain words:
1. Run `python kit/instalar.py --lang en --simulacro` (or python3 if python doesn't exist)
   and explain what it will create and which block it will add to my CLAUDE.md.
2. If I agree, run it with `--lang en --si --claude-md --hooks` to apply it
   (it keeps .bak copies of what it touches and never overwrites anything).
3. Open the map with `python server.py --abrir` and leave it running in the background.
4. Tell me the full path of my vault so I can open it in Obsidian.
Ask me before each step.
```

3. Answer its questions. Claude always shows you what it will change first.

## Step 6: open your vault in Obsidian

1. Open Obsidian → **Open folder as vault**.
2. Pick the folder Claude told you (usually `Documents/Boveda`).
3. You'll see example notes: `Home`, `Learnings`, etc. That's your notebook.

## Step 7: use it

- Work with Claude as usual. When each task ends, it takes notes on its own.
- Next time, just say **"let's continue with <your project>"**.
- To watch the spider: on Windows, double-click `abrir.cmd` in the repo folder; on Mac, run `python3 server.py --abrir` in the terminal.
- The example notes are only a guide: over time Claude fills the vault with yours.

## If something fails

| What happens | What to do |
|---|---|
| `python` is not recognized | Reinstall Python and tick "Add python.exe to PATH". On Mac use `python3` |
| `claude` is not recognized | Close and reopen the terminal; if it persists, repeat step 3 |
| The map opens but no spider moves | Close and reopen Claude Code (hooks load at startup) and ask it to read a note |
| My vault is in another folder | Run the installer with `--boveda "path"`: it remembers it for good |
| I'm not sure what I did | Run `claude` in the repo folder and say: "check whether the install went well" |

More technical detail: [README.md](README.md) and [kit/README.md](kit/README.md).
