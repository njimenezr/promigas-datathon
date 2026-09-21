# Guía del participante — Datathon Promigas

¡Bienvenido/a! Este es un datathon técnico de datos sobre Databricks, aterrizado al negocio de **transporte y distribución de gas natural**. El objetivo es **aprender haciendo**: construyes soluciones reales de datos y las validas tú mismo/a.

> Es una actividad de **formación y práctica**. No necesitas experiencia previa con Databricks: la plataforma trae un asistente de IA (Databricks Assistant / Genie) que te ayuda a escribir el código.

---

## 1. Cómo funciona

- **Participas de forma individual.** Cada quien resuelve su propio reto en su propio workspace.
- **Eliges UN track** (puedes intentar el otro como bonus si terminas):
  - 🛠️ **Data Engineer** — construyes el pipeline de datos completo (Bronce → Plata → Oro) desde archivos crudos. Guía: [`track_data_engineer.md`](track_data_engineer.md)
  - 📊 **Analytics Engineer** — partes de datos ya limpios y te enfocas en análisis, visualización y pronóstico. Guía: [`track_analytics_engineer.md`](track_analytics_engineer.md)
- Cada track tiene **4 niveles** — 🟢 Básico → 🟡 Medio → 🔴 Avanzado → 🟣 Experto — **en cascada**: completa uno para pasar al siguiente. El nivel Experto lleva lo avanzado de la plataforma (orquestación con Jobs, funciones de IA, gobierno, capa semántica con Metric Views, ML/AutoML).
- **Los tracks son independientes:** trabajan en **catálogos distintos** (`hackathon_data_eng` vs. `hackathon_analytics_eng`) y ninguno bloquea al otro.

---

## 2. Qué necesitas antes de empezar

1. **Una cuenta de Databricks Free Edition** (tu propio workspace).
   Regístrate en: [Databricks Free Edition](https://www.databricks.com/learn/free-edition)
2. **Acceso al repo Git del datathon** (te lo comparte la organización). Contiene:
   - Las guías de cada track.
   - La carpeta `datasets/` con los datos (CSV versionados).
3. **Acceso a la App de scoring** (te comparten el enlace). Ahí registras tus respuestas.

---

## 3. Preparar tu workspace

1. **Clona el repo** como Git folder en tu workspace de Free Edition.
   Docs: [Git folders](https://docs.databricks.com/aws/en/repos/)
2. **Sigue el "Paso 0"** de la guía de tu track para crear el catálogo/esquema/volumen y subir los CSV.
3. ¡Listo para el Nivel Básico!

---

## 4. Cómo se evalúa — la App de scoring

Cada nivel tiene **preguntas de reto**. Para cada pregunta, en la App registras:

1. **El valor calculado** (un número, un texto — p. ej. `10980` o `Gases del Caribe`).
2. **El prompt de IA** que usaste, si te apoyaste en el Assistant/Genie para llegar al resultado.

Reglas:

- **La App valida tu respuesta** contra el resultado esperado sobre el dataset congelado.
- **Los niveles se desbloquean en orden:** Básico → Medio → Avanzado → Experto.
- **Puntaje:** Básico 10 pts/pregunta · Medio 20 · Avanzado 30 · **Experto 40**.
- Algunas preguntas del nivel **Experto** se validan por **evidencia** (pegas el prompt y adjuntas/describes una captura): el organizador las revisa. Son las de funciones de IA, gobierno y ML.
- **Leaderboard compartido**, con desempate **por velocidad** (quien llega primero al mismo puntaje, arriba).

> No es trampa usar IA — ¡al contrario! Se te pide el prompt justamente para que compartas cómo lo resolviste. Lo que importa es que **entiendas** y llegues al **valor correcto**.

---

## 5. Consejos

- **Lee el diccionario de columnas** en [`datasets/README.md`](datasets/README.md) — está todo en español.
- **Apóyate en el Databricks Assistant / Genie** para escribir SQL y explorar.
- **Ve nivel por nivel.** No te saltes pasos: cada tabla/artefacto que construyes alimenta las preguntas siguientes.
- **Verifica tus conteos** antes de pegarlos en la App (un `SELECT count(*)` de más nunca sobra).
- Si te bloqueas, **pregúntale a un mentor** — están para desatascarte rápido.

---

## 6. Preguntas frecuentes

**¿Puedo hacer los dos tracks?** Sí, si terminas el tuyo. Cada track vive en su propio catálogo, así que no se pisan.

**¿Necesito saber Python?** Ayuda, pero con SQL + el Assistant puedes resolver casi todo. El track Analytics Engineer es más ligero en código.

**¿Qué pasa si mi respuesta no coincide?** Revisa filtros, nulos y duplicados. Casi siempre la diferencia está en una regla de calidad o un `JOIN` mal cruzado.

**¿Los datos son reales?** Son **sintéticos** y están **congelados** para que las respuestas sean deterministas. Reflejan la operación de transporte de gas (desbalances en KPCD, nodos del Caribe, remitentes, clima).

¡Éxitos! 🚀
