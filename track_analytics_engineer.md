# Track Analytics Engineer — Guía del participante

Convierte una capa **Oro ya construida** de operaciones de transporte de gas en **análisis, visualización, pronóstico y ML**. Trabajas **individual**, en **tu propio workspace de Databricks Free Edition**, en el catálogo **`hackathon_analytics_eng`**.

A diferencia del track Data Engineer, **no armas el pipeline**: partes de datos limpios y de negocio, y te enfocas en explotarlos.

Avanzas por **4 niveles en cascada** (cada uno desbloquea el siguiente):

| Nivel | Foco | Pts/pregunta |
|-------|------|:---:|
| 🟢 Básico | Explorar la capa Oro | 10 |
| 🟡 Medio | Tablero AI/BI + Genie | 20 |
| 🔴 Avanzado | Correlación clima + Pronóstico + Ventanas | 30 |
| 🟣 Experto | ML/AutoML + Capa semántica + IA | 40 |

En cada nivel respondes **preguntas de reto** en la App de scoring pegando el **valor calculado** y, si usaste IA, el **prompt** que usaste. Algunas preguntas del nivel Experto se validan por **evidencia** (captura + prompt).

> 💡 Puedes apoyarte en el **Databricks Assistant / Genie**. **Aquí lo difícil no es escribir el SQL — es interpretar bien la pregunta.** Ojo con las trampas: "mayor promedio" ≠ "más frecuente", "mayor tasa" ≠ "mayor volumen", "mediana" ≠ "promedio". Si confundes la definición, el número te saldrá mal-pero-plausible.

---

## Paso 0 — Preparación (una sola vez)

1. **Clona el repo** del datathon como Git folder en tu workspace.
   Docs: [Git folders](https://docs.databricks.com/aws/en/repos/)
2. **Crea el catálogo, el esquema y el volumen:**
   ```sql
   CREATE CATALOG IF NOT EXISTS hackathon_analytics_eng;
   CREATE SCHEMA  IF NOT EXISTS hackathon_analytics_eng.oro;
   CREATE VOLUME  IF NOT EXISTS hackathon_analytics_eng.oro.crudos;
   ```
   Docs: [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/) · [Volumes](https://docs.databricks.com/aws/en/volumes/)
   > Si no puedes crear el catálogo, usa `workspace` como catálogo y crea el esquema ahí.
3. **Sube los CSV** de `datasets/analytics_engineer/` al volumen `crudos` y cárgalos en tablas:
   - **`oro_despachos`** ← `gold_gas_flows.csv` · **`nodos`** ← `nodos.csv` · **`clima_por_nodo`** ← `weather_meteo_by_node.csv`
   Docs: [Subir archivos a un volumen](https://docs.databricks.com/aws/en/ingestion/file-upload/) · [`read_files`](https://docs.databricks.com/aws/en/sql/language-manual/functions/read_files)

---

## 🟢 Nivel Básico — Explorar la capa Oro

**Objetivo:** entender `oro_despachos` y sus estadísticos con SQL.

Docs: [Consultas SQL](https://docs.databricks.com/aws/en/sql/language-manual/) · [Agregación](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin#aggregate-functions) · [`percentile_cont`](https://docs.databricks.com/aws/en/sql/language-manual/functions/percentile_cont)

**Preguntas de reto:**
1. ¿Cuántos despachos hay en total en `oro_despachos`?
2. `desbalance_salida` **promedio** (1 decimal).
3. **Mediana** (`percentile_cont 0.5`) de `desbalance_salida` (1 decimal). *(compárala con el promedio)*
4. **Percentil 95** de `duracion_transito` (1 decimal).
5. `antiguedad_unidad` promedio en años (1 decimal).
6. `remitente` con más despachos.

---

## 🟡 Nivel Medio — Tablero AI/BI + Genie

**Objetivo:** construir un tablero y hacer preguntas en lenguaje natural, distinguiendo bien **volumen** de **intensidad**.

1. **Dashboard AI/BI** sobre `oro_despachos`: despachos por `mes_despacho`; desbalance **promedio** por `departamento_salida`; proporción `interrumpido` / por `tipo_tramo`.
   Docs: [AI/BI Dashboards](https://docs.databricks.com/aws/en/dashboards/)
2. **Espacio Genie** sobre `oro_despachos` (+ `nodos`) para validar hallazgos en español.
   Docs: [Genie](https://docs.databricks.com/aws/en/genie/)

**Preguntas de reto:**
7. **Mes** (`mes_despacho`, número) con más despachos.
8. **Mes** con **menos** despachos.
9. `departamento_salida` con **mayor desbalance promedio** (código de 3 letras).
10. **Tasa de interrupción** del sistema (%, 1 decimal).
11. **% de despachos en fin de semana** (`dia_semana` 6 o 7) (1 decimal).
12. **Franja horaria con mayor desbalance _promedio_.** *(⚠️ no es la franja con más despachos)*
13. **Remitente con mayor _tasa_ de despachos `'Alto >60'`** (%). *(⚠️ no es el que más despachos tiene)*
14. Remitente con **menor** desbalance promedio.
15. **% del desbalance total del sistema que aporta el `departamento_salida` #1** (1 decimal).
16. **% de despachos `'Alto >60'`** sobre el total (1 decimal).
17. **Cuota de los 2 remitentes con más despachos** = % del total que concentran entre ambos (1 decimal).
18. ¿Cuántos **`departamento_salida`** tienen un desbalance promedio **superior al promedio global** del sistema?

---

## 🔴 Nivel Avanzado — Correlación clima + Pronóstico + Ventanas

**Objetivo:** cruzar clima con desbalances, aplicar lógica de **ventana/serie de tiempo** y pronosticar.

1. **Matriz resumen clima ↔ desbalance:** une `oro_despachos` con `clima_por_nodo` (por `codigo_nodo_entrada` = `id_nodo` y `fecha_despacho` = `fecha`), agregada por **fecha × nodo de entrada**.
2. **Serie de tiempo:** desbalance **promedio diario** por nodo y **rachas** (días consecutivos sobre un umbral) con funciones de ventana.
3. **Pronóstico con `ai_forecast`:** serie **diaria** de Surtigas desde `2024-01-01` hasta `2024-01-31`.

Docs: [JOINs](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-join) · [Window functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions) · [`ai_forecast`](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_forecast)

**Preguntas de reto:**
19. Filas de `oro_despachos` con `desbalance_clima >= 15`.
20. Despachos donde la causa **clima** supera a la **operacional** (`desbalance_clima > desbalance_operacional`).
21. **Filas-resumen** (combinaciones fecha × nodo de entrada) de tu matriz. *(pista: ¿cuántos nodos de entrada hay?)*
22. **Nodo de entrada con mayor _tasa_ de despachos `'Alto >60'`** (nombre).
23. **Racha máxima** de días **consecutivos** en que el desbalance **promedio diario** del nodo **Ballena** superó **60** KPCD. *(gaps-and-islands con ventanas)*
24. ¿En cuántos **días** el desbalance promedio diario **del sistema** superó 60 KPCD?
25. ¿En cuántos **días** hubo precipitación (`> 0`) en **los 10 nodos** simultáneamente?
26. **Mes con mayor crecimiento intermensual (MoM)** en número de despachos (número de mes). *(usa `lag()`)*
27. **Unidades reincidentes:** ¿cuántas `id_unidad` distintas tienen **3 o más** despachos `'Alto >60'`?
28. ¿Cuántas **unidades** (`id_unidad`) tienen **5 o más** despachos en total?
29. **Días pronosticados** por `ai_forecast` para Surtigas (serie diaria hasta `2024-01-31`).

---

## 🟣 Nivel Experto — ML/AutoML + Capa semántica + IA

Cuatro retos; algunos se validan por **evidencia** (captura + prompt).

### 30. Predicción con AutoML — *evidencia + valor*
Entrena un modelo (regresión) que prediga `desbalance_salida` a partir de `remitente`, `tipo_tramo`, `franja_horaria`, `duracion_transito`, `antiguedad_unidad`, `mes_despacho`. Usa **AutoML** y revisa la importancia de variables.
Docs: [AutoML](https://docs.databricks.com/aws/en/machine-learning/automl/)
- **Reto (valor):** ¿cuántas filas usa el entrenamiento (todo `oro_despachos`)?
- **Reto (evidencia):** el mejor modelo y su métrica (R²/RMSE) + captura del experimento.

### 31. Capa semántica con Metric Views
Crea una **Metric View** sobre `oro_despachos` con dimensiones (`departamento_salida`, `remitente`, `mes_despacho`) y medidas `desbalance_total_sistema` = `sum(desbalance_salida)` y `pct_no_explicado` = `sum(otro_desbalance)/sum(desbalance_salida)×100`. Conéctale un **espacio Genie**.
Docs: [Metric Views](https://docs.databricks.com/aws/en/metric-views/) · [Genie](https://docs.databricks.com/aws/en/genie/)
- **Reto A:** valor de `desbalance_total_sistema` (entero).
- **Reto B:** valor de `pct_no_explicado` en % (1 decimal).

### 32. Resumen ejecutivo con IA — *evidencia*
Usa **`ai_query`** o **`ai_gen`** para generar en SQL un **resumen ejecutivo** de los desbalances por departamento (hallazgos + recomendación).
Docs: [`ai_query`](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_query) · [`ai_gen`](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_gen)
- **Reto (evidencia):** el **prompt/consulta** y una **muestra del resumen**.

### 33. Gobierno + alertas — *evidencia*
Aplica una **etiqueta** de Unity Catalog a tu Metric View o a `oro_despachos`, y crea una **alerta SQL** que notifique si el desbalance promedio diario supera un umbral.
Docs: [Tags UC](https://docs.databricks.com/aws/en/data-governance/unity-catalog/tags) · [Alerts](https://docs.databricks.com/aws/en/sql/user/alerts/)
- **Reto (evidencia):** captura del tag y de la alerta configurada.

---

¿Terminaste el Experto? Puedes intentar el **track Data Engineer** como bonus (otro catálogo, arma el pipeline Bronce → Plata → Oro desde los CSV crudos).
