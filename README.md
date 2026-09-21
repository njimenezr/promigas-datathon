# Datathon Promigas — Plataforma de Inteligencia de Operaciones de Transporte de Gas

Reto técnico de datos sobre Databricks, aterrizado al negocio de **transporte y distribución de gas natural**. Es una actividad de **formación y práctica**: construyes soluciones reales de datos y las validas tú mismo/a.

## Formato

- **Individual.** Cada participante resuelve su propio reto en su propio workspace de **[Databricks Free Edition](https://www.databricks.com/learn/free-edition)**.
- **Dos tracks a elegir** (uno principal; el otro es bonus). Corren **en paralelo e independientes** — catálogos distintos, ninguno bloquea al otro.
- **4 niveles por track** (🟢 Básico → 🟡 Medio → 🔴 Avanzado → 🟣 Experto), **en cascada** dentro del track.
- **Evaluación por App de scoring:** pegas el **valor calculado** y el **prompt de IA** que usaste; la App valida el resultado. Leaderboard con desempate **por velocidad**.

## Empieza aquí

0. **Crea tu cuenta gratuita** en [Databricks Free Edition](https://www.databricks.com/learn/free-edition) (si aún no tienes workspace).
1. **Clona este repo** como Git folder en tu workspace de Free Edition.
   Docs: [Git folders](https://docs.databricks.com/aws/en/repos/)
2. Lee la [**Guía del participante**](guia_participante.md) — formato, requisitos, cómo se evalúa.
3. Elige tu track, **corre su notebook de Paso 0** (crea catálogo/esquema/volumen y carga los datos) y sigue su guía:

| Track | Notebook de setup | Guía | Catálogo |
|-------|-------------------|------|----------|
| 🛠️ **Data Engineer** | [`notebooks/00_setup_data_engineer`](notebooks/00_setup_data_engineer.py) | [`track_data_engineer.md`](track_data_engineer.md) | `hackathon_data_eng` |
| 📊 **Analytics Engineer** | [`notebooks/00_setup_analytics_engineer`](notebooks/00_setup_analytics_engineer.py) | [`track_analytics_engineer.md`](track_analytics_engineer.md) | `hackathon_analytics_eng` |

4. Consulta el [diccionario de datos](datasets/README.md) cuando lo necesites.

## Los dos tracks

| Track | Punto de partida (provisto) | Qué hace |
|-------|-----------------------------|----------|
| **Data Engineer** | CSV **crudos** (despachos, interrupciones, nodos, clima) | Bronce → Plata + Calidad → Oro → Jobs, gobierno, IA, Metric Views |
| **Analytics Engineer** | Una **capa Oro ya construida** (`oro_despachos`) + nodos + clima | Explora → AI/BI + Genie → correlación + `ai_forecast` → AutoML + Metric Views |

Cada track parte de un punto autocontenido, por eso **no dependen entre sí**.

## Estructura del repo

```
promigas-datathon-repo/
├── README.md                        ← este archivo
├── guia_participante.md             ← formato, app, reglas, FAQ
├── track_data_engineer.md           ← guía del track DE (4 niveles)
├── track_analytics_engineer.md      ← guía del track AE (4 niveles)
├── notebooks/
│   ├── 00_setup_data_engineer.py       ← Paso 0 DE (catálogo + carga CSV crudos)
│   └── 00_setup_analytics_engineer.py  ← Paso 0 AE (catálogo + carga Oro provista)
└── datasets/
    ├── README.md                    ← diccionario de columnas
    ├── data_engineer/               ← CSV crudos (track DE)
    └── analytics_engineer/          ← capa Oro + referencia (track AE)
```

## Datos

Dataset **sintético y congelado** (≈ 6 MB), en **español**. Refleja la operación de transporte de gas: desbalances en KPCD (nominado vs. entregado), nodos del Caribe, remitentes (Surtigas, Gases del Caribe, etc.) y clima diario por nodo. Las respuestas son deterministas porque el dataset no se regenera. Ver [`datasets/README.md`](datasets/README.md).
