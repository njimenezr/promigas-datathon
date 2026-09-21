# Datos del Datathon

Dataset del datathon de transporte de gas de Promigas, en **español**. Está organizado por track: cada track parte de datos distintos y trabaja en un catálogo distinto (por eso los tracks son independientes).

## `data_engineer/` — punto de partida del track Data Engineer (datos crudos)

Cárgalos en el catálogo **`hackathon_data_eng`**. Tú construyes el pipeline Bronce → Plata → Oro.

| Archivo | Filas | Descripción |
|---------|------:|-------------|
| `gas_flows.csv` | 10.980 | Despachos de gas (crudo). Trae problemas de calidad reales: nulos, longitudes de `id_unidad` inválidas, duplicados y un typo en la columna `antiguedad_unidd`. |
| `gas_interrupted.csv` | 2.940 | Despachos interrumpidos/reenrutados (crudo). |
| `nodos.csv` | 10 | Nodos del sistema de transporte (geolocalización). |
| `weather_meteo_by_node.csv` | 3.650 | Clima diario 2023 por nodo. |

## `analytics_engineer/` — punto de partida del track Analytics Engineer (Oro provista)

Cárgalos en el catálogo **`hackathon_analytics_eng`**. Partes de una capa **Oro ya construida**: no armas el pipeline, te enfocas en análisis y visualización.

| Archivo | Filas | Descripción |
|---------|------:|-------------|
| `gold_gas_flows.csv` | 12.935 | Capa **Oro ya construida** (`oro_despachos`), lista para consumir. |
| `nodos.csv` | 10 | Nodos del sistema. |
| `weather_meteo_by_node.csv` | 3.650 | Clima diario 2023 por nodo. |

## Diccionario de columnas (español)

**`nodos`** — `codigo_nodo`, `nombre_nodo`, `ciudad`, `departamento`, `pais`, `latitud`, `longitud`

**`clima_por_nodo`** (archivo `weather_meteo_by_node.csv`) — `fecha`, `temp_prom`, `temp_min`, `temp_max`, `precipitacion`, `humedad`, `dir_viento`, `vel_viento`, `presion`, `id_nodo`

**`gas_flows.csv`** (crudo) — `fuente`, `fecha_despacho`, `dia_semana`, `remitente`, `id_unidad`, `nodo_entrada`, `ciudad_entrada`, `franja_horaria`, `desbalance_entrada`, `marca_desbalance_entrada`, `tipo_desbalance_entrada`, `nodo_salida`, `ciudad_salida`, `desbalance_salida`, `tipo_desbalance_salida`, `duracion_transito`, `tipo_tramo`, `desbalance_operacional`, `desbalance_clima`, `desbalance_sistema`, `desbalance_integridad`, `desbalance_aguas_arriba`, `fabricante`, `modelo`, `antiguedad_unidd` *(typo a propósito → se corrige a `antiguedad_unidad`)*

**`gas_interrupted.csv`** (crudo) — igual que `gas_flows.csv` pero sin `fabricante`/`modelo`/`antiguedad`, y con `interrumpido` y `reenrutado`.

**`gold_gas_flows.csv`** (`oro_despachos`) — datos de negocio listos: incluye `mes_despacho`, nombres de nodo (`nombre_nodo_entrada`/`salida`), `departamento_entrada`/`salida`, clasificación de desbalance (`tipo_desbalance_entrada`/`salida`), marcas (`marca_*`), `tipo_tramo` estandarizado, causas de desbalance (`desbalance_operacional`/`clima`/`sistema`/`integridad`/`aguas_arriba`), `otro_desbalance`, y `interrumpido`/`reenrutado`.

## Unidades y convenciones
- Volúmenes / desbalances en **KPCD** (kilo pies cúbicos por día).
- Clasificación de desbalance: `Sin desbalance ...` (≤0) · `Bajo <15` · `Medio >15` · `Alto >60`.
- Tipo de tramo: `Troncal >300Km` · `Regional 100-300Km` · `Ramal <100Km`.

> Dataset sintético y **congelado**. Tamaño ≈ 6,2 MB.
