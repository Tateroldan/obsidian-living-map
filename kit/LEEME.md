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
```

- La bóveda de ejemplo se crea en `MAPA_BOVEDA` (o `~/Documents/Boveda`). Si la carpeta ya tiene notas, solo se agregan los archivos que falten.
- El bloque de `CLAUDE.md` se muestra y **siempre** se pregunta; antes se guarda una copia `.bak`.
- Los hooks no se editan solos: el instalador imprime las líneas para `settings.json`.

## Cómo crece solo

1. Claude abre `Inicio.md` y busca neuronas del tema antes de opinar.
2. Al terminar, `cierre-de-tarea` actualiza el estado del proyecto y crea una neurona si hubo algo reutilizable.
3. `validar.py` revisa cada nota al escribirla (propiedades, enlaces, secretos).
4. El router y el bibliotecario procesan la bandeja; el mapa vivo te deja ver todo.

## Lo que NO trae

Skills de dominio (video, juegos, marketing…): cada quien crea las suyas con `find-skills` o a mano, y las apunta en `IA/Skills.md`. Las neuronas de ejemplo son solo guía: reemplázalas por las tuyas.

## Qué promete y qué no (medido)

- **No abarata una tarea aislada.** En pruebas A/B controladas el kit cuesta parecido o algo más por tarea, porque leer contexto y escribir el cierre añade turnos.
- **Sí evita errores de formato cuando hay una neurona aplicable.** Escenario: la convención de CSV de un cliente solo vivía en una neurona. En 15 corridas (5 por brazo), el archivo salió en formato equivocado 4 de 5 veces sin kit y 0 de 10 con kit (Fisher exacto p ≈ 0.004). El código quedó correcto en las 15 corridas, porque sin kit el usuario re-explicó la convención y pagó una segunda ronda.
- **El costo total salió igual** (≈ $0.147 por tarea en los tres brazos). El ahorro de acertar a la primera se compensó con 3 de 10 corridas con kit que no ejecutaron el script y necesitaron una segunda ronda.
- **Los hooks opcionales** (`kit/hooks/`: inyección de contexto y compuerta de cierre) no mostraron ganancia sobre el `CLAUDE.md` solo y no se recomiendan por defecto.
- **Límites:** muestras mínimas (n = 2 por brazo), un solo modelo, escenarios diseñados. Es evidencia del mecanismo, no prueba de ahorro.

El detalle y las cifras están en las notas del proyecto; falta documentación (ver abajo).

## Documentación pendiente
- Guía paso a paso con un ejemplo completo (tarea → neurona → reutilización).
- Cómo escribir neuronas que de verdad se reutilicen (qué incluir y qué no).
- Cómo correr tu propia medición A/B y leer la varianza.
