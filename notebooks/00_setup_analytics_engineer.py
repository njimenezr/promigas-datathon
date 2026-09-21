# Databricks notebook source
# MAGIC %md
# MAGIC # Paso 0 — Setup Track Analytics Engineer
# MAGIC
# MAGIC Este notebook prepara tu entorno para el **track Analytics Engineer**:
# MAGIC 1. Crea el **catálogo**, el **esquema** y el **volumen**.
# MAGIC 2. Copia los CSV del repo (capa **Oro provista** + nodos + clima) al volumen.
# MAGIC 3. Crea las tablas `oro_despachos`, `nodos` y `clima_por_nodo`.
# MAGIC
# MAGIC > Partes de una **Oro ya construida**: no armas pipeline. Tras correr esto, abre `track_analytics_engineer.md` y arranca con el **🟢 Nivel Básico**.
# MAGIC >
# MAGIC > Ejecútalo **una sola vez**. Si no puedes crear el catálogo (permisos), cambia el widget `catalogo` a `workspace`.

# COMMAND ----------

dbutils.widgets.text("catalogo", "hackathon_analytics_eng", "Catálogo")
dbutils.widgets.text("esquema", "oro", "Esquema")
dbutils.widgets.text("volumen", "crudos", "Volumen")

catalogo = dbutils.widgets.get("catalogo").strip()
esquema  = dbutils.widgets.get("esquema").strip()
volumen  = dbutils.widgets.get("volumen").strip()

print(f"Catálogo: {catalogo}\nEsquema:  {esquema}\nVolumen:  {volumen}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Crear catálogo, esquema y volumen
# MAGIC Docs: [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/) · [Volumes](https://docs.databricks.com/aws/en/volumes/)

# COMMAND ----------

try:
    spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalogo}")
    print(f"✅ Catálogo '{catalogo}' listo.")
except Exception as e:
    print(f"⚠️  No se pudo crear el catálogo '{catalogo}': {e}")
    print("   → Usando 'workspace' como catálogo.")
    catalogo = "workspace"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalogo}.{esquema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalogo}.{esquema}.{volumen}")
print(f"✅ Esquema y volumen listos: {catalogo}.{esquema}.{volumen}")

vol_path = f"/Volumes/{catalogo}/{esquema}/{volumen}"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Copiar los CSV del repo al volumen

# COMMAND ----------

import os, shutil

ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
nb_path = ctx.notebookPath().get()
repo_root = "/".join(nb_path.split("/")[:-2])
origen = f"/Workspace{repo_root}/datasets/analytics_engineer"

print(f"Origen (repo): {origen}")
print(f"Destino (volumen): {vol_path}\n")

archivos = ["gold_gas_flows.csv", "nodos.csv", "weather_meteo_by_node.csv"]
for a in archivos:
    src = f"{origen}/{a}"
    dst = f"{vol_path}/{a}"
    shutil.copyfile(src, dst)
    print(f"  ✅ {a}  ({os.path.getsize(src):,} bytes)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Crear las tablas (Oro provista + referencia)
# MAGIC Docs: [`read_files`](https://docs.databricks.com/aws/en/sql/language-manual/functions/read_files)

# COMMAND ----------

spark.sql(f"USE CATALOG {catalogo}")
spark.sql(f"USE SCHEMA {esquema}")

def cargar(tabla, archivo):
    df = (spark.read
          .option("header", "true")
          .option("inferSchema", "true")
          .csv(f"{vol_path}/{archivo}"))
    df.write.mode("overwrite").saveAsTable(tabla)
    n = spark.table(tabla).count()
    print(f"  ✅ {tabla}: {n:,} filas")

cargar("oro_despachos",  "gold_gas_flows.csv")
cargar("nodos",          "nodos.csv")
cargar("clima_por_nodo", "weather_meteo_by_node.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Verificación

# COMMAND ----------

display(spark.sql("SELECT * FROM oro_despachos LIMIT 10"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### ✅ Listo
# MAGIC Tienes `oro_despachos` (12.935 filas), `nodos` y `clima_por_nodo`. Abre **`track_analytics_engineer.md`** y arranca con el **🟢 Nivel Básico**.
