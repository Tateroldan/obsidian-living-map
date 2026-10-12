---
tipo: guia
area: sistema
estado: activo
creado: {{HOY}}
---
# Cómo funciona esta bóveda

Guía para ti y para Claude. Si algo nuevo no encaja aquí, se ajusta esta nota.

> [!info] Conjunto neuronal
> Así se llama el sistema completo: las neuronas de `Aprendizajes` enlazadas entre sí con **Conecta con:**, más las skills y agentes de Claude que se alimentan de ellas (índice en [[Skills]]). Cada tarea le agrega neuronas y la siguiente las aprovecha.

## Las 3 capas
1. **Carpetas = tipo de lugar** (pocas, nunca más de 2 niveles): `00 Bandeja` (capturas rápidas) · `00 Diario` · áreas (`Trabajo`, `Personal`, `Proyectos`, `Ideas`, `IA`) · `Aprendizajes` (neuronas) · `99 Archivo` (lo terminado; no se borra) · `Adjuntos` (imágenes) · `_Sistema` (esta guía).
2. **Propiedades = qué es la nota** (todas las llevan):
   - `tipo`: aprendizaje · prompt · proyecto · plan · guia · script · indice · diario
   - `area`: trabajo · personal · proyectos · ideas · ia · sistema
   - `estado`: activo · idea · listo · reemplazada · archivado
   - `creado`: AAAA-MM-DD
3. **Enlaces = de qué trata** (`[[...]]`): cada nota enlaza al menos a otra; las neuronas terminan en **Conecta con:**.

Los valores permitidos viven en `reglas.json` (copia de `reglas.ejemplo.json`). Si cambias las listas de arriba, cámbialas también ahí.

## Flujo
- **Capturar:** todo lo rápido va a `00 Bandeja` o a la nota diaria.
- **Procesar (1 vez por semana):** `python kit/router_bandeja.py` (sin tokens, en simulacro) y lo ambiguo, al agente **bibliotecario**.
- **Encontrar:** el buscador, la vista gráfica y el mapa vivo.
- **Cerrar:** lo terminado cambia a `estado: listo`; lo viejo pasa a `99 Archivo`. Nunca se borra.
- **Salud:** `python salud.py` escribe un informe de huérfanas y notas nunca tocadas.

## Reglas
- Neuronas: nunca sobrescribir; si algo cambia, nota nueva con «reemplaza a [[...]]» y la vieja con `estado: reemplazada`.
- Plantillas (Ctrl+P → «Insertar plantilla»): `Neurona`, `Prompt`, `Proyecto`, `Diaria`, `Estado para Claude`.
- Ayudantes: agente **bibliotecario** (dile a Claude «pásaselo al bibliotecario») y las skills de [[Skills]].
- **Confianza (opcional):** en neuronas de una fuente sin probar, agrega `confianza: verificada | inferida | sin-verificar`.

## Para Claude (leer antes de escribir aquí)
- Crear notas con las 4 propiedades; elegir `tipo`/`area` de las listas de arriba.
- Antes de responder sobre un tema, buscar neuronas existentes (Grep en `Aprendizajes/` o por `area:`).
- Notas cortas y de una idea; enlazar en vez de repetir.

**Conecta con:** [[Inicio]] · [[Aprendizajes]] · [[Skills]]
