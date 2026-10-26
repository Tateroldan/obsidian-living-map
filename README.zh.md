# Obsidian Living Map

[English](README.md) · [Español](README.es.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · 中文

你的 Obsidian 知识库的 3D 地图:一只蜘蛛在 Claude Code 读取(青色)、写入(琥珀色)或搜索(紫色)的笔记上行走。不消耗 token:`PostToolUse` 钩子把每次访问记录到 `events.jsonl`,页面每 0.8 秒读取一次。仅使用 Python 标准库,无需 `pip install`。

**新手?** 请按照[分步新手指南](BEGINNERS.md)操作(英文;[西班牙文版](PRINCIPIANTES.md)),无需编程。

## 环境要求

- **Obsidian**(免费):从 [obsidian.md](https://obsidian.md) 下载,然后用 *Open folder as vault* 打开你的知识库文件夹。使用套件时,选择它创建的文件夹(`MAPA_BOVEDA`,默认 `~/Documents/Boveda`)。在地图中点击笔记会在 Obsidian 中打开。
- **Python 3.9+**:仅用标准库,无需 `pip install`。
- **[Claude Code](https://claude.com/claude-code)**:钩子记录它读写的内容;没有它,地图会显示知识库,但蜘蛛不会移动。

## 安装

1. 克隆仓库并打开 `abrir.cmd`(或运行 `python server.py --abrir`),会打开 http://127.0.0.1:8765。
2. 如果你的知识库不在 `~/Documents/Boveda`,请把 `MAPA_BOVEDA` 设为其路径。端口用 `MAPA_PUERTO` 修改,含未完成复选框的笔记用 `MAPA_DECISIONES` 指定。所有设置都在 `config.py`。
   使用 `validar.py` 时,把 `reglas.ejemplo.json` 复制为 `reglas.json`,并按你的知识库调整类型、领域和状态(`reglas.json` 不会提交)。
3. 想看到 Claude 的移动,请把钩子添加到 `~/.claude/settings.json`:

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

可选:`validar.py`(PostToolUse `Write|Edit`;提示缺失属性、失效链接或粘贴的密钥)和 `diario.py`(SessionEnd;把会话摘要写入当日笔记)。

首次从控制台打开时,会询问一次是否随 Windows 自动启动。之后可用 `python server.py --autoarranque on|off|estado` 更改。

## 组成

| 文件 | 用途 |
|---|---|
| `reglas.ejemplo.json` | `validar.py` 的规则(允许的属性、禁止的混用) |
| `config.py` | 知识库路径、端口和日志(唯一包含路径的位置) |
| `server.py` | 本地服务器;只提供页面及其组件,并检查 `Host` |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | 孤立笔记和从未被触及的笔记 |
| `validar.py`, `vecinos.py`, `diario.py` | 写入时校验、邻居/路径/主题、自动生成当日笔记 |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | 相机与图谱、带 IK 的蜘蛛、6 种配色、8 种语言、面板 |

URL 参数:`?tema=rgb&lang=zh`。单击笔记在 Obsidian 中打开,双击则聚焦。

## 隐私

一切都在 `127.0.0.1` 上运行。`events.jsonl` 保存你的笔记路径,已加入 `.gitignore`。

## 套件(自学习部分)

地图展示 Claude 触及了什么;`kit/` 则赋予 Claude 让知识库自行生长的工作方法:任务开始与结束的规则、相互链接的笔记(“神经元”)、图书管理员代理、无需 token 的收件箱路由器、收尾技能和示例知识库。不包含任何人的个人笔记。可用 `python kit/instalar.py --simulacro` (`--lang en` / `--lang es`) 预览。详情:[kit/README.md](kit/README.md)。

## 支持

如果它对你有帮助,可以在 [Ko-fi 请我喝杯咖啡](https://ko-fi.com/tateroldan) ☕

## 第三方许可

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## 许可证

Apache-2.0,见 `LICENSE`。
