# Guía para empezar (sin saber programar)

[English](BEGINNERS.md) · Español

## Qué es, en palabras simples

**Claude Code** es un asistente de IA que trabaja en tu computadora. El problema es que **olvida todo al cerrar la sesión**: cada vez tienes que volver a explicarle tu proyecto, tus gustos y lo que ya intentaste.

Este repo le da **memoria y orden**:

- **Una libreta que crece sola** (tu «bóveda» de Obsidian). Al terminar cada tarea, Claude anota dónde se quedó, qué aprendió y qué no funcionó.
- **Un método de trabajo.** Antes de empezar, Claude lee solo la nota que le sirve, no todo.
- **Un mapa en 3D** donde ves en vivo, como una araña, qué notas lee y escribe Claude.

**Lo que ganas:** basta con decir «sigamos con mi proyecto» y Claude retoma sin que le repitas nada. Gastas menos tiempo, menos explicaciones y menos uso de la IA en cada sesión siguiente.

## Lo que necesitas (unos 20 minutos)

| Qué | Para qué | Costo |
|---|---|---|
| Obsidian | Ver y editar tu libreta de notas | Gratis |
| Python | Hace funcionar el mapa y el instalador | Gratis |
| Claude Code | El asistente | Necesita una cuenta de Claude de pago (Pro o superior) o créditos de API |

## Paso 1: instala Obsidian

1. Entra a [obsidian.md](https://obsidian.md), descárgalo e instálalo como cualquier programa.
2. Por ahora no abras ninguna bóveda; lo harás en el paso 6.

## Paso 2: instala Python

1. Entra a [python.org/downloads](https://www.python.org/downloads/) y descarga la versión más nueva.
2. **En Windows:** en la primera pantalla del instalador, **marca la casilla «Add python.exe to PATH»** antes de dar clic en *Install Now*. Si no la marcas, nada de lo demás funcionará.
3. Para comprobarlo, abre una terminal (Windows: tecla Inicio, escribe `PowerShell` y ábrelo; Mac: abre la app *Terminal*) y escribe:
   ```
   python --version
   ```
   (en Mac: `python3 --version`). Debe salir `Python 3.9` o mayor.

## Paso 3: instala Claude Code

1. Sigue las instrucciones de [claude.com/claude-code](https://claude.com/claude-code) para tu sistema.
2. En la terminal escribe `claude` y entra con tu cuenta. Cuando veas el cuadro donde se escribe, ya está. Ciérralo con `/exit`.

## Paso 4: descarga este repo

1. Arriba de esta página, en GitHub, da clic en el botón verde **Code → Download ZIP**.
2. Descomprime el ZIP en tus Documentos. Quedará una carpeta llamada `obsidian-living-map` (puede terminar en `-main`).

## Paso 5: deja que Claude lo instale por ti

1. Abre una terminal **dentro de esa carpeta**. En Windows: abre la carpeta, da clic derecho en un espacio vacío y elige **Abrir en Terminal**. En Mac: clic derecho en la carpeta → **Servicios → Nuevo terminal en la carpeta**.
2. Escribe `claude` y pega este mensaje tal cual:

```
Soy principiante. Instálame este repo paso a paso, explicándome en palabras simples:
1. Corre `python kit/instalar.py --lang es --simulacro` y explícame qué va a crear.
2. Si estoy de acuerdo, córrelo con `--si` para aplicarlo.
3. Agrega a mi settings.json de Claude Code los hooks que imprime el instalador
   (hook.py, validar.py y diario.py; NO los opcionales). Antes, haz una copia de seguridad.
   Usa el comando de Python que funcione en esta computadora (python o python3).
4. Abre el mapa con `python server.py --abrir`.
5. Dime en qué carpeta quedó mi bóveda para abrirla en Obsidian.
Pregúntame antes de cada paso.
```

3. Responde a lo que te pregunte. Claude siempre te mostrará antes lo que va a cambiar.

## Paso 6: abre tu bóveda en Obsidian

1. Abre Obsidian → **Open folder as vault** («Abrir carpeta como bóveda»).
2. Elige la carpeta que te dijo Claude (normalmente `Documentos/Boveda`).
3. Verás notas de ejemplo: `Inicio`, `Aprendizajes`, etc. Esa es tu libreta.

## Paso 7: úsalo

- Trabaja con Claude como siempre. Al terminar cada tarea, él anota por su cuenta.
- La próxima vez, di solo **«sigamos con <tu proyecto>»**.
- Para ver la araña: en Windows, doble clic a `abrir.cmd` en la carpeta del repo; en Mac, `python3 server.py --abrir` en la terminal.
- Las notas de ejemplo son solo guía: con el tiempo, Claude las irá llenando con las tuyas.

## Si algo falla

| Lo que pasa | Qué hacer |
|---|---|
| `python` no se reconoce | Reinstala Python y marca «Add python.exe to PATH». En Mac usa `python3` |
| `claude` no se reconoce | Cierra y vuelve a abrir la terminal; si sigue, repite el paso 3 |
| El mapa abre pero no se ve la araña | Reinicia Claude Code (los hooks se cargan al iniciar) y pídele que lea una nota |
| No sé qué hice | Abre `claude` en la carpeta del repo y dile: «revisa si la instalación quedó bien» |

Más detalle técnico: [README.es.md](README.es.md) y [kit/LEEME.md](kit/LEEME.md).
