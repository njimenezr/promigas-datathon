# Track Data Engineer — Guía del participante

Construye una plataforma de datos de punta a punta sobre la **arquitectura Medallion** (Bronce → Plata → Oro) con datos de operaciones de transporte de gas, y llévala hasta **orquestación, gobierno e IA**. Trabajas **individual**, en **tu propio workspace de Databricks Free Edition**, en el catálogo **`hackathon_data_eng`**.

Avanzas por **4 niveles en cascada** (cada uno desbloquea el siguiente):

| Nivel | Foco | Pts/pregunta |
|-------|------|:---:|
| 🟢 Básico | Capa Bronce + exploración del crudo | 10 |
| 🟡 Medio | Capa Plata + Control de Calidad | 20 |
| 🔴 Avanzado | Capa Oro (lógica de negocio) | 30 |
| 🟣 Experto | Orquestación (Jobs) + Gobierno + IA + Capa semántica | 40 |

En cada nivel respondes **preguntas de reto** en la App de scoring pegando el **valor calculado** y, si usaste IA, el **prompt** que usaste. Algunas preguntas del nivel Experto se validan por **evidencia** (captura + prompt), no por un número.

> 💡 Puedes apoyarte en el **Databricks Assistant / Genie** para escribir el código. **Aquí lo difícil no es escribir el SQL — es entender el negocio y definir bien la transformación.** Varias preguntas tienen trampas (el texto `'null'`, duplicados, umbrales, "promedio" vs "frecuencia", "filas" vs "grupos", "tasa" vs "volumen"): si no razonas la definición, el número te saldrá mal-pero-plausible. Ve nivel por nivel: cada tabla que construyes alimenta las siguientes.

---

## Paso 0 — Preparación (una sola vez)

1. **Clona el repo** del datathon como Git folder en tu workspace.
   Docs: [Git folders](https://docs.databricks.com/aws/en/repos/)
2. **Crea el catálogo, el esquema y el volumen:**
   ```sql
   CREATE CATALOG IF NOT EXISTS hackathon_data_eng;
   CREATE SCHEMA  IF NOT EXISTS hackathon_data_eng.medallion;
   CREATE VOLUME  IF NOT EXISTS hackathon_data_eng.medallion.crudos;
   ```
   Docs: [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/) · [Volumes](https://docs.databricks.com/aws/en/volumes/)
   > Si no puedes crear el catálogo, usa `workspace` como catálogo y crea el esquema ahí.
3. **Sube los CSV** de `datasets/data_engineer/` al volumen `crudos`.
   Docs: [Subir archivos a un volumen](https://docs.databricks.com/aws/en/ingestion/file-upload/)

---

## 🟢 Nivel Básico — Capa Bronce (datos crudos "tal cual")

**Objetivo:** aterrizar los datos crudos en tablas Bronce, sin transformar, y explorarlos para entender su forma.

Crea las tablas de referencia y Bronce (nombres de columna **en español**, como vienen en los CSV):

- **`nodos`**: `codigo_nodo, nombre_nodo, ciudad, departamento, pais, latitud, longitud`
- **`clima_por_nodo`** (de `weather_meteo_by_node.csv`): `fecha, temp_prom, temp_min, temp_max, precipitacion, humedad, dir_viento, vel_viento, presion, id_nodo`
- **`bronce_despachos`** (de `gas_flows.csv`): **todas las columnas como `STRING`** (incluye el typo `antiguedad_unidd` — se corrige en Plata).
- **`bronce_despachos_interrumpidos`** (de `gas_interrupted.csv`): todas las columnas como `STRING`.

Docs: [Leer CSV](https://docs.databricks.com/aws/en/query/formats/csv) · [`read_files`](https://docs.databricks.com/aws/en/sql/language-manual/functions/read_files)

**Preguntas de reto:**
1. ¿Cuántas filas quedaron en `bronce_despachos`?
2. ¿Cuántas filas quedaron en `bronce_despachos_interrumpidos`?
3. ¿Cuántas filas quedaron en `clima_por_nodo`?
4. ¿Cuántas **columnas** tiene `bronce_despachos`?
5. ¿Cuántos **días distintos** hay en `fecha_despacho` (ignorando valores inválidos/`'null'`)?
6. ¿Cuántos **nodos de salida distintos** aparecen en `bronce_despachos` (válidos)? *(pista: el nº de nodos de entrada NO es el mismo)*

---

## 🟡 Nivel Medio — Capa Plata + Control de Calidad

**Objetivo:** limpiar y validar los datos, aislando lo defectuoso en cuarentena, y cargar lo válido y tipado en Plata.

Implementa **7 reglas de calidad** sobre `bronce_despachos` (y las mismas, menos `modelo_nulo`, sobre `bronce_despachos_interrumpidos`):

| Regla | Falla si… |
|-------|-----------|
| `dia_semana_nulo` | `dia_semana` es nulo o el texto `'null'` |
| `remitente_nulo` | `remitente` ausente |
| `nodo_entrada_nulo` | `nodo_entrada` ausente |
| `nodo_salida_nulo` | `nodo_salida` ausente |
| `modelo_nulo` | `modelo` ausente *(solo `bronce_despachos`)* |
| `id_unidad_longitud_invalida` | `id_unidad` **no** tiene entre 5 y 6 caracteres |
| `duplicados` | la fila está **completamente duplicada** (aparece más de una vez) |

Reglas de construcción:
- Registra el **resumen** de cada regla (fuente, prueba, fallas, timestamp) en **`calidad_datos`**.
- Envía a **`calidad_datos_cuarentena`** las filas que fallan **cualquier** regla. En `duplicados`, **cuarentena todas las copias** (no dejes ninguna).
- Carga en **`plata_despachos`** (tipada) solo las filas válidas; agrega `interrumpido`/`reenrutado` (vacío para las de `bronce_despachos`), `hora_actualizacion`, y **corrige el typo** `antiguedad_unidd` → `antiguedad_unidad`.

Docs: [Funciones SQL](https://docs.databricks.com/aws/en/sql/language-manual/) · [`length`](https://docs.databricks.com/aws/en/sql/language-manual/functions/length) · [Window functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions)

**Preguntas de reto:**
7. ¿Cuántas filas quedaron en total en `calidad_datos_cuarentena`?
8. ¿Cuántas filas válidas quedaron en `plata_despachos`?
9. Fallas totales (bd+bi) de `id_unidad_longitud_invalida`.
10. Fallas de `modelo_nulo`.
11. Fallas totales (bd+bi) de `remitente_nulo`.
12. Fallas totales (bd+bi) de `nodo_salida_nulo`.
13. ¿Cuántos **grupos de filas duplicadas distintos** hay (bd+bi)? *(⚠️ no es el nº de filas duplicadas)*
14. ¿Cuántas filas se enviaron a cuarentena **por duplicados**, contando **todas las copias** (bd+bi)?
15. ¿Qué **porcentaje** de las filas de Bronce pasó a Plata (1 decimal)?
16. ¿Cuántas filas de la cuarentena **provienen de `bronce_despachos_interrumpidos`**? *(grano por fuente)*

---

## 🔴 Nivel Avanzado — Capa Oro (lista para el negocio)

**Objetivo:** enriquecer Plata con lógica de negocio y dejar `oro_despachos` lista para analítica.

A partir de `plata_despachos` (unida a `nodos`), calcula: `mes_despacho`; `departamento_entrada`/`salida` (parseado de `"Ciudad, DEP"` o cruzado con `nodos`); **clasificación** `tipo_desbalance_*` (`Sin desbalance en entrega` ≤0 · `Bajo <15` 1–15 · `Medio >15` 16–60 · `Alto >60` >60); **marcas** `marca_desbalance_*` (>0) y `marca_final_desbalance_*` (≥15); **tramo** estandarizado (`Troncal >300Km`/`Regional 100-300Km`/`Ramal <100Km`/NULL); **atribución de causas** (`marca_*` = 1 si la causa > 1 KPCD; `otro_desbalance` = parte del desbalance NO explicada por las 5 causas).

Docs: [`CASE`](https://docs.databricks.com/aws/en/sql/language-manual/functions/case) · [`split`](https://docs.databricks.com/aws/en/sql/language-manual/functions/split) · [`stddev`](https://docs.databricks.com/aws/en/sql/language-manual/functions/stddev) · [`percentile_cont`](https://docs.databricks.com/aws/en/sql/language-manual/functions/percentile_cont) · [Window functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions)

**Preguntas de reto:**
17. Filas con `tipo_desbalance_salida = 'Alto >60'`.
18. Filas con `tipo_tramo` nulo (tramo no reconocido).
19. Filas con `marca_otro_desbalance = 1`.
20. **% del desbalance total del sistema atribuible a clima** = `sum(desbalance_clima)/sum(desbalance_salida)×100` (1 decimal).
21. **% del desbalance total NO explicado** por las 5 causas = `sum(otro_desbalance)/sum(desbalance_salida)×100` (1 decimal).
22. Despachos `'Alto >60'` **en tramo Troncal y NO interrumpidos** (las 3 condiciones).
23. **Pérdida en tránsito:** despachos donde `desbalance_salida − desbalance_entrada > 20` KPCD.
24. **2º `departamento_salida`** en el ranking por **desbalance total** (`sum(desbalance_salida)`). (código de 3 letras)
25. Remitente con mayor **variabilidad** de desbalance (`stddev(desbalance_salida)`).
26. **Percentil 95** de `duracion_transito` (1 decimal).
27. Despachos con **las 5 causas marcadas a la vez** (todas las `marca_desbalance_*` de causa = 1).
28. **Desbalance neto del sistema** = `sum(desbalance_salida) − sum(desbalance_entrada)` (entero).
29. **Mes con mayor crecimiento intermensual (MoM)** en número de despachos (número de mes). *(usa `lag()` sobre la serie mensual)*
30. **Unidades reincidentes:** ¿cuántas `id_unidad` distintas tienen **3 o más** despachos `'Alto >60'`?
31. ¿Cuántos **`departamento_salida`** tienen un **desbalance promedio superior al promedio global** del sistema?

---

## 🟣 Nivel Experto — Orquestación + Gobierno + IA + Capa semántica

Cuatro retos; algunos se validan por **evidencia** (captura + el prompt que usaste).

### 32. Orquestación con Lakeflow Jobs
Convierte tu pipeline en un **Job** que ingesta las **dos fuentes** con una tarea **For each** parametrizada, con dependencias Bronce → Plata → Oro. Ejecútalo completo.
Docs: [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/) · [For each](https://docs.databricks.com/aws/en/jobs/for-each) · [Parámetros](https://docs.databricks.com/aws/en/jobs/parameters)
- **Reto:** ¿cuántas filas ingesta el Job en total a Bronce (ambas fuentes crudas)?

### 33. Capa semántica con Metric Views
Crea una **Metric View** sobre `oro_despachos` con dimensiones (`departamento_salida`, `remitente`, `mes_despacho`) y medidas `desbalance_total_sistema` = `sum(desbalance_salida)` y `pct_no_explicado` = `sum(otro_desbalance)/sum(desbalance_salida)×100`.
Docs: [Metric Views](https://docs.databricks.com/aws/en/metric-views/)
- **Reto A:** valor de `desbalance_total_sistema` (entero).
- **Reto B:** valor de `pct_no_explicado` en % (1 decimal).

### 34. IA en SQL (funciones de IA) — *evidencia*
Usa **`ai_classify`** o **`ai_gen`** para categorizar la **causa principal** de una muestra de `oro_despachos`, o generar un **resumen** por departamento.
Docs: [`ai_classify`](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_classify) · [`ai_gen`](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_gen) · [`ai_query`](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_query)
- **Reto (evidencia):** pega el **prompt/consulta** y una **muestra del resultado**.

### 35. Gobierno (tags + máscara + linaje) — *evidencia*
Aplica una **etiqueta** de Unity Catalog a `oro_despachos`, define una **máscara de columna** sobre un campo sensible (p. ej. `id_unidad`) y revisa el **linaje** Bronce → Plata → Oro.
Docs: [Tags UC](https://docs.databricks.com/aws/en/data-governance/unity-catalog/tags) · [Column masks](https://docs.databricks.com/aws/en/tables/column-mask) · [Linaje](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage)
- **Reto (evidencia):** captura del tag aplicado y del **grafo de linaje**.

---

¿Terminaste el Experto? Puedes intentar el **track Analytics Engineer** como bonus (otro catálogo, otra Oro provista).
