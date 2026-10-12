---
name: cierre-de-tarea
description: Cierra una tarea en la bóveda de Obsidian - actualiza el "Estado para Claude" del proyecto, lista los supuestos tomados y propone o crea la neurona si hubo algo reutilizable. Usar al terminar cualquier tarea que tocó un proyecto o produjo un aprendizaje, antes de dar la respuesta final.
---

# Cierre de tarea

Hazlo sin que te lo pidan, al final de cada tarea. Debe tomar un minuto, no una sesión.

## Pasos
Haz las escrituras de los pasos 1-4 en un solo mensaje, con llamadas a herramientas en paralelo: cada turno extra cuesta.
1. **Estado para Claude.** Abre la nota del proyecto (desde `Inicio.md`) y actualiza su sección «Estado para Claude» (≤10 líneas): fecha, dónde quedamos, siguiente paso, archivos clave. Si hubo alternativas descartadas, agrega «Descartado y por qué» con una línea cada una.
2. **Neurona.** Pregúntate: ¿hubo una técnica, una trampa o una decisión que aplicarías en otro proyecto? Ante la duda, sí: crea la neurona sin preguntar (una línea basta). Busca con Grep en `Aprendizajes/` si ya existe una parecida. Si existe, enlázala o crea una que la amplíe; si no, crea una nueva con la plantilla `Neurona` (una idea, 3-6 líneas, termina con **Conecta con:**). Nunca sobrescribas: nota nueva con «reemplaza a [[...]]».
3. **Índice de skills.** Si la neurona toca el tema de una skill, agrégala a su línea «Se alimenta de» en `IA/Skills.md` y avisa si conviene actualizar la skill.
4. **Índice de neuronas.** Agrega la neurona a `Aprendizajes.md` bajo su tema.
5. **Supuestos.** Termina la respuesta con una lista corta de lo que decidiste sin preguntar. Si no hubo, omítela.

## Reglas
- No inventes aprendizajes, pero «arreglé un bug puntual» sin ninguna regla detrás es lo único que no merece neurona.
- Una idea por neurona; enlaza en vez de repetir.
- Valida con el mapa vivo: la neurona nueva debe enlazar a otra (`validar.py` avisa si no).
