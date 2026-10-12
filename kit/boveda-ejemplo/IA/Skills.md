---
tipo: indice
area: ia
estado: activo
creado: {{HOY}}
---
# Skills

Índice de las skills y agentes de Claude y de las neuronas que los alimentan. **Solo es un índice**: cada skill vive en `~/.claude/skills/<nombre>/SKILL.md` y aquí no se copia su contenido.

> [!tip] Regla
> Cuando nace una neurona que toca el tema de una skill, se apunta aquí en su línea «Se alimenta de» y se revisa si la skill necesita actualizarse. Así el sistema mejora solo.

## Sistema
### Agente: bibliotecario
Ordena la bóveda: procesa la bandeja, pone propiedades, crea y enlaza neuronas, detecta enlaces rotos. Archivo: `~/.claude/agents/bibliotecario.md`.
- **Se alimenta de:** [[Cómo funciona esta bóveda]] · [[Aprendizajes]] · [[Lo rutinario a un modelo barato, lo difícil al caro]]

### cierre-de-tarea
Al terminar una tarea: actualiza el «Estado para Claude» del proyecto, lista los supuestos y propone la neurona si hubo algo reutilizable.
- **Se alimenta de:** [[Una neurona, una idea, y siempre enlaza]] · [[Pregunta lo que cambia el resultado, no adivines]]

## Desarrollo web
### verificar-web
Antes de decir «listo» en una página web local, toma una captura y lee la consola con Edge headless.
- **Se alimenta de:** (agrega aquí las neuronas de errores web que vayas aprendiendo)

**Conecta con:** [[Inicio]] · [[Aprendizajes]] · [[Busca neuronas antes de opinar]]
