# Kit del conjunto neuronal

El mapa vivo muestra qué toca Claude; este kit le da a Claude **la forma de trabajar** que hace que la bóveda crezca sola: reglas para empezar y terminar cada tarea, neuronas enlazadas, un agente que ordena y un router que clasifica sin gastar tokens. Sin ninguna nota de nadie: todo es genérico y se adapta con `reglas.json`.

## Qué incluye

| Pieza | Dónde | Para qué |
|---|---|---|
| Reglas para Claude | `claude/CLAUDE.plantilla.md` | Al empezar (abrir `Inicio`, buscar neuronas), al terminar (estado, supuestos, neurona) y forma de trabajar |
| Bóveda de ejemplo | `boveda-ejemplo/` | Carpetas, guía, plantillas, 4 neuronas de muestra, índice de skills |
| Agente | `claude/agentes/bibliotecario.md` | Ordena la bandeja, pone propiedades, crea y enlaza neuronas (modelo barato) |
| Skill `cierre-de-tarea` | `claude/skills/cierre-de-tarea/` | Automatiza el «al terminar»: estado, supuestos, neurona |
| Skill `verificar-web` | `claude/skills/verificar-web/` | Captura y consola con Edge headless antes de decir «listo» |
| Router de la bandeja | `router_bandeja.py` | Clasifica por palabras, sin tokens; mueve solo lo seguro |
| Instalador | `instalar.py` | Copia todo sin sobrescribir y pregunta antes de tocar tu `CLAUDE.md` |

## Instalar

```
python kit/instalar.py --simulacro     # ver qué haría, sin escribir nada
python kit/instalar.py                 # paso a paso, pregunta antes de cada grupo
python kit/instalar.py --lang en       # kit en inglés (carpetas, propiedades y mensajes en inglés)
python kit/instalar.py --si --claude-md --hooks   # todo sin preguntas (después de revisar --simulacro)
```

- La bóveda de ejemplo se crea en `MAPA_BOVEDA` (o `~/Documents/Boveda`). Si la carpeta ya tiene notas, solo se agregan los archivos que falten.
- El bloque de `CLAUDE.md` se muestra y **siempre** se pregunta; antes se guarda una copia `.bak`.
- Los hooks se agregan a `settings.json` solo con `--hooks` (copia `.bak`, sin duplicar y con el mismo Python del instalador); si no, el instalador imprime las líneas.
- La carpeta de la bóveda (`--boveda`) queda guardada en `preferencias.json`: el hook, el servidor y `contexto.py` la encuentran sin variables de entorno.

## Cómo crece solo

1. Claude abre `Inicio.md` y busca neuronas del tema antes de opinar.
2. Al terminar, `cierre-de-tarea` actualiza el estado del proyecto y crea una neurona si hubo algo reutilizable.
3. `validar.py` revisa cada nota al escribirla (propiedades, enlaces, secretos).
4. El router y el bibliotecario procesan la bandeja; el mapa vivo te deja ver todo.

## Lo que NO trae

Skills de dominio (video, juegos, marketing…): cada quien crea las suyas con `find-skills` o a mano, y las apunta en `IA/Skills.md`. Las neuronas de ejemplo son solo guía: reemplázalas por las tuyas.

## De dónde sale el ahorro

El kit ahorra recursos **entre sesiones**, no dentro de una tarea aislada:

- **Dejas de repetir instrucciones.** Cada proyecto guarda un «Estado para Claude» corto (dónde quedamos, siguiente paso, qué se descartó y por qué). Basta con «sigamos con el proyecto X»: Claude no necesita que le vuelvas a contar la historia ni explorar todo el código otra vez.
- **Lectura modular.** Archivos chicos de una sola responsabilidad y un mapa en el `CLAUDE.md` del proyecto permiten abrir solo la pieza que hace falta, en vez de cargar todo al contexto.
- **Las neuronas se reutilizan.** Una convención o un arreglo guardado se aplica a la primera, sin re-explicarlo ni pagar una segunda ronda.
- **No se repiten errores.** Lo descartado y las trampas conocidas quedan escritos.
- **Tu tiempo también cuenta.** Menos correcciones y explicaciones es un ahorro que ningún contador de tokens muestra.

El precio es un costo de entrada pequeño: leer el índice y escribir el cierre añade unos turnos. En una tarea nueva y suelta que no reutiliza nada, el kit cuesta parecido o un poco más. El retorno crece con cada tarea que se apoya en las anteriores.

## Qué se midió

- **Neurona aplicable (15 corridas, 5 por brazo):** la convención de CSV de un cliente solo vivía en una neurona. Sin kit el archivo salió en formato equivocado 4 de 5 veces; con kit, 0 de 10 (Fisher exacto p ≈ 0.004). Sin kit el usuario tuvo que re-explicar la convención.
- **El costo por tarea en ese escenario salió igual** (≈ $0.147 en los tres brazos): lo ganado al acertar a la primera se compensó con 3 de 10 corridas con kit que no ejecutaron el script y necesitaron otra ronda.
- **Los hooks opcionales** (`kit/hooks/`: inyección de contexto y compuerta de cierre) no mostraron ganancia sobre el `CLAUDE.md` solo y no se recomiendan por defecto.
- **Falta medir:** una serie larga de tareas relacionadas en varias sesiones, que es donde se acumula el ahorro de arriba. Las muestras hasta ahora son chicas, con un solo modelo y escenarios diseñados.

## Documentación pendiente
- Guía paso a paso con un ejemplo completo (tarea → neurona → reutilización).
- Cómo escribir neuronas que de verdad se reutilicen (qué incluir y qué no).
- Cómo correr tu propia medición A/B y leer la varianza.
