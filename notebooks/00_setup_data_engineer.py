# Databricks notebook source
# MAGIC %md
# MAGIC # Paso 0 — Setup Track Data Engineer
# MAGIC
# MAGIC Este notebook prepara tu entorno para el **track Data Engineer**:
# MAGIC 1. Crea el **catálogo**, el **esquema** y el **volumen**.
# MAGIC 2. Copia los **CSV crudos** del repo al volumen `crudos`.
# MAGIC
# MAGIC > **No crea las tablas Bronce/Plata/Oro** — eso es tu reto (empieza por el Nivel Básico en `track_data_engineer.md`).
# MAGIC >
# MAGIC > Ejecútalo **una sola vez**. Si no puedes crear el catálogo (permisos), cambia el widget `catalogo` a `workspace`.

# COMMAND ----------

dbutils.widgets.text("catalogo", "hackathon_data_eng", "Catálogo")
dbutils.widgets.text("esquema", "medallion", "Esquema")
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
    print("   → Usando 'workspace' como catálogo. (Cambia el widget si prefieres otro.)")
    catalogo = "workspace"
    dbutils.widgets.get("catalogo")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalogo}.{esquema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalogo}.{esquema}.{volumen}")
print(f"✅ Esquema y volumen listos: {catalogo}.{esquema}.{volumen}")

vol_path = f"/Volumes/{catalogo}/{esquema}/{volumen}"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Copiar los CSV crudos del repo al volumen

# COMMAND ----------

import os, shutil

# Ubica la carpeta del repo a partir de la ruta de este notebook
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
nb_path = ctx.notebookPath().get()                 # /Users/.../promigas-datathon-repo/notebooks/00_setup_data_engineer
repo_root = "/".join(nb_path.split("/")[:-2])       # .../promigas-datathon-repo
origen = f"/Workspace{repo_root}/datasets/data_engineer"

print(f"Origen (repo): {origen}")
print(f"Destino (volumen): {vol_path}\n")

archivos = ["gas_flows.csv", "gas_interrupted.csv", "nodos.csv", "weather_meteo_by_node.csv"]
for a in archivos:
    src = f"{origen}/{a}"
    dst = f"{vol_path}/{a}"
    shutil.copyfile(src, dst)
    print(f"  ✅ {a}  ({os.path.getsize(src):,} bytes)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Verificación

# COMMAND ----------

display(dbutils.fs.ls(vol_path))

# COMMAND ----------

# MAGIC %md
# MAGIC ### ✅ Listo
# MAGIC Tus CSV crudos están en el volumen. Ahora abre **`track_data_engineer.md`** y arranca con el **🟢 Nivel Básico** (crear las tablas Bronce).
# MAGIC
# MAGIC Ruta de tus archivos:
# MAGIC ```
# MAGIC /Volumes/<catalogo>/<esquema>/<volumen>/
# MAGIC ```
