# Bloque 5 — Pulido Final y Deploy

## Lecciones del Bloque 4

| Problema | Causa | Solucion |
|---|---|---|
| Bar chart sin nombres en eje Y | `tickvals`/`ticktext` no especificados, margen izquierdo de 10px | Añadir `tickmode="array"`, `margin=dict(l=180)` y `automargin=True` |
| Grouped bar chart mostraba solo una barra | Pandas Series con indice propio desalineaba los traces | Convertir a listas Python con `.tolist()` |
| Graficos con fondo blanco sobre tema oscuro | `plot_bgcolor="white"` no encaja con dark theme de Streamlit | `plot_bgcolor="rgba(0,0,0,0)"` + colores de texto/grid en blanco |

---

## Objetivo

Preparar el proyecto para produccion: configuracion de deploy, README final,
ajuste del `.gitignore` para incluir datos mock en el repo, y configuracion
de Streamlit Cloud + Render.

---

## Archivos creados / modificados

```
.gitignore                          <- modificado: CSVs mock incluidos, secrets excluidos
.streamlit/
    config.toml                     <- nuevo: tema dark + config servidor
    secrets.example.toml            <- nuevo: ejemplo de secrets para produccion
render.yaml                         <- nuevo: config de deploy en Render
dashboard/components/api_client.py  <- modificado: soporte Streamlit secrets
README.md                           <- modificado: version final con deploy
docs/bloque-05-deploy.md            <- este archivo
docs/contexto-proyecto.md           <- nuevo: contexto para futuras sesiones (en .gitignore)
docs/comandos.md                    <- nuevo: referencia rapida de comandos
```

---

## Configuracion de deploy

### Streamlit Cloud (dashboard)

Streamlit Cloud conecta directamente con el repo de GitHub y despliega con un click.

1. Ir a https://share.streamlit.io
2. New app → seleccionar repo `Rally-performance-analyzer`
3. Main file path: `dashboard/app.py`
4. En **Advanced settings → Secrets** añadir:
```toml
DASHBOARD_API_URL = "https://tu-api.onrender.com"
```
5. Deploy

El dashboard lee la URL de la API desde `st.secrets["DASHBOARD_API_URL"]` en produccion
y desde `os.getenv("DASHBOARD_API_URL", "http://localhost:8000")` en local.

### Render (FastAPI)

1. Ir a https://render.com → New Web Service
2. Conectar repo de GitHub
3. Configurar:
   - **Build command:** `pip install -r requirements.txt && WRC_USE_MOCK=true python -m ingestion.pipeline`
   - **Start command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11
4. Deploy

El `render.yaml` en la raiz del proyecto tambien permite deploy automatico.

### Nota sobre los datos en produccion

Los CSVs de mock (`data/processed/*.csv`) se incluyen en el repo (no estan en `.gitignore`)
para que el deploy funcione sin necesidad de ejecutar el pipeline. El build command
de Render los regenera igualmente como medida de seguridad.

---

## Cambios en .gitignore

| Cambio | Motivo |
|---|---|
| `data/processed/*.csv` → incluidos | Los CSVs de mock son pequeños y necesarios para el deploy |
| `repomix-output.md` → excluido | Archivo temporal de analisis, no pertenece al repo |
| `docs/contexto-proyecto.md` → excluido | Documento de uso personal, no publico |
| `.streamlit/secrets.toml` → excluido | Contiene URLs y credenciales de produccion |

---

## Streamlit theme

Configurado en `.streamlit/config.toml`:

| Parametro | Valor | Descripcion |
|---|---|---|
| `base` | `dark` | Tema oscuro base |
| `primaryColor` | `#C8102E` | Rojo Toyota (color primario del proyecto) |
| `backgroundColor` | `#0E1117` | Fondo principal |
| `secondaryBackgroundColor` | `#1A1A2E` | Fondo sidebar y cards |
| `textColor` | `#FAFAFA` | Texto principal |

---

## Validaciones del Bloque 5

### V1 — Tests siguen pasando
```bash
pytest backend/tests/ -v
→ 51 passed
```

### V2 — Dashboard arranca con tema correcto
```
streamlit run dashboard/app.py
→ Tema oscuro con color primario rojo visible
```

### V3 — .gitignore correcto
```bash
git status
→ data/processed/*.csv aparece como untracked (para anadir al repo)
→ repomix-output.md no aparece
→ docs/contexto-proyecto.md no aparece
```

### V4 — README final completo
```
README.md incluye: stack, funcionalidades, arquitectura,
instrucciones de ejecucion, instrucciones de deploy, tabla de estado
```

### V5 — Deploy en Streamlit Cloud
```
URL publica del dashboard funcionando
```

### V6 — Deploy en Render
```
URL publica de la API con /docs funcionando
```

---

## Commits sugeridos para cerrar el proyecto

```bash
# 1. Anadir CSVs de mock al repo
git add data/processed/
git commit -m "feat: include mock CSVs in repo for deploy"

# 2. Config de deploy y pulido final
git add .streamlit/ render.yaml .gitignore README.md
git add dashboard/components/api_client.py
git add docs/bloque-05-deploy.md docs/comandos.md
git commit -m "feat: bloque 5 - deploy config, Streamlit theme, README final"

# 3. Push
git push
```

---

## Posibles errores en deploy

| Error | Causa | Solucion |
|---|---|---|
| Dashboard no conecta con API | `DASHBOARD_API_URL` no configurado en secrets | Añadir en Streamlit Cloud secrets |
| Render falla en build | Python version incorrecta | Asegurar `PYTHON_VERSION=3.11.9` en env vars |
| `ModuleNotFoundError` en Render | PYTHONPATH no incluye root | Añadir `PYTHONPATH=.` en env vars de Render |
| CSVs no encontrados | Pipeline no se ejecuto en build | Verificar build command incluye `python -m ingestion.pipeline` |
