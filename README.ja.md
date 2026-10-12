# Obsidian Living Map

[English](README.md) · [Español](README.es.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · 日本語 · [中文](README.zh.md)

Claude Code が読む(シアン)・書く(琥珀)・検索する(紫)ノートの上をクモが歩く、Obsidian ボールトの 3D マップです。トークンは消費しません。`PostToolUse` フックがすべてのアクセスを `events.jsonl` に記録し、ページが 0.8 秒ごとに読み取ります。Python 標準ライブラリのみで、`pip install` は不要です。

## インストール

1. リポジトリをクローンし、`abrir.cmd` を開きます(または `python server.py --abrir`)。http://127.0.0.1:8765 が開きます。
2. ボールトが `~/Documents/Boveda` にない場合は、`MAPA_BOVEDA` にそのパスを設定します。ポートは `MAPA_PUERTO`、未完了チェックボックスのあるノートは `MAPA_DECISIONES` で変更できます。設定はすべて `config.py` にあります。
   `validar.py` を使うには、`reglas.ejemplo.json` を `reglas.json` にコピーし、種類・エリア・状態をボールトに合わせて調整します(`reglas.json` はコミットされません)。
3. Claude の動きを見るには、`~/.claude/settings.json` にフックを追加します:

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

任意: `validar.py`(PostToolUse `Write|Edit`。プロパティ欠落、壊れたリンク、貼り付けられた秘密情報を警告)と `diario.py`(SessionEnd。セッションをデイリーノートに要約)。

コンソールから初めて開くと、Windows 起動時に自動で開始するかどうかを一度だけ尋ねます。後から `python server.py --autoarranque on|off|estado` で変更できます。

## 構成

| ファイル | 役割 |
|---|---|
| `reglas.ejemplo.json` | `validar.py` のルール(許可するプロパティ、禁止する混在) |
| `config.py` | ボールトのパス、ポート、ログ(パスを持つ唯一の場所) |
| `server.py` | ローカルサーバー。ページと関連ファイルのみ配信し、`Host` を検証 |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | 孤立ノートと一度も触れられていないノート |
| `validar.py`, `vecinos.py`, `diario.py` | 書き込み時の検証、近傍/経路/テーマ、デイリーノートの自動生成 |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | カメラとグラフ、IK のクモ、6 つのパレット、8 言語、パネル |

URL パラメータ: `?tema=rgb&lang=ja`。ノートをクリックすると Obsidian で開き、ダブルクリックでフォーカスします。

## プライバシー

すべて `127.0.0.1` 上で動作します。`events.jsonl` にはノートのパスが保存されますが、`.gitignore` に入っています。

## サードパーティのライセンス

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## ライセンス

Apache-2.0。`LICENSE` を参照してください。
