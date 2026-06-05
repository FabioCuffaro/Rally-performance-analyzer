# Bloque 4 — Graficos Avanzados y Pulido Visual

## Lecciones del Bloque 3

| Problema | Causa | Solucion |
|---|---|---|
| `utf-8 codec can't decode` en dashboard | Windows guarda archivos como cp1252 | `encoding="utf-8-sig"` al leer/escribir CSVs |
| `ModuleNotFoundError: dashboard` en Streamlit | Streamlit ejecuta desde subcarpeta, root no esta en sys.path | `sys.path.insert(0, ...)` al inicio de cada pagina |
| Archivo `app.py` corrupto | Windows corrompio emojis y caracteres al copiar del zip | Reescribir desde terminal con encoding UTF-8 explicito |

---

## Objetivo

Corregir todos los bugs visuales detectados en el Bloque 3 y pulir la calidad
visual del dashboard para que quede a nivel de portfolio profesional.

---

## Bugs corregidos

### Bug 1: Bump chart y gap chart comprimidos (root cause)

**Problema:** Todos los datos aparecian en una sola columna. El eje X no mostraba
las etapas SS1-SS5.

**Causa raiz:** Los CSVs generados por el pipeline incluyen la columna `stage_code`.
Las funciones de `analytics.py` hacian un merge adicional con la tabla de stages
(que tambien tiene `stage_code`), generando columnas duplicadas `stage_code_x`
y `stage_code_y`. Al intentar acceder a `row["stage_code"]`, Pandas devolvia `""`
porque la columna real era `stage_code_x`.

**Solucion:** Eliminar el merge redundante en `analytics.py`. Si `stage_code` ya
existe en el DataFrame, no volver a hacer merge con stages.

```python
# ANTES (bug)
result = df.merge(stages[["stage_id", "stage_code"]], on="stage_id", how="left")
# → crea stage_code_x y stage_code_y

# DESPUES (fix)
# stage_code ya existe en el CSV, no hace falta merge adicional
result = df.copy()
```

### Bug 2: Tabla comparativa con filas duplicadas

**Problema:** La tabla de comparativa mostraba muchas filas repetidas con los
mismos tiempos para el piloto A.

**Causa:** El merge `df_a.merge(df_b, on="stage_code")` en `03_compare.py`
generaba un producto cartesiano cuando los DataFrames tenian indices no alineados.

**Solucion:** Reescribir la tabla iterando sobre las etapas del piloto A y haciendo
lookup manual del piloto B, garantizando exactamente una fila por etapa.

### Bug 3: Bar chart sin nombres de pilotos visibles

**Problema:** El eje Y del bar chart de etapas no mostraba los nombres.

**Causa:** La columna `y_label` no tenia `automargin=True` en el layout, cortando
los nombres largos.

**Solucion:** Añadir `automargin=True` al eje Y y ajustar `margin=dict(l=10, r=100)`.

### Bug 4: Eje X categorico no respetado

**Problema:** Plotly interpretaba los codigos de etapa (SS1, SS2...) como strings
ordinarios, no como categorias ordenadas.

**Solucion:** Usar `type="category"` y `categoryorder="array"` con el orden
explicito en todos los graficos con eje X de etapas.

---

## Mejoras visuales aplicadas

### Paleta de colores profesional

Sustitucion de rojo/azul puros por colores motorsport mas sobrios:

| Fabricante | Color anterior | Color nuevo |
|---|---|---|
| Toyota | `#EB0A1E` (rojo puro) | `#C8102E` (rojo Toyota oficial) |
| Hyundai | `#003399` (azul puro) | `#003B8E` (azul marino Hyundai) |

### Layout base compartido

Todos los graficos usan `_base_layout()` con configuracion consistente:
- Fondo: `#FAFAFA` (casi blanco, no blanco puro)
- Grid: `#E8E8E8` (gris muy suave)
- Fuente: Inter/Arial, 12px, `#1A1A2E`
- Hover: fondo blanco, borde suave

### Mejoras por grafico

| Grafico | Mejora |
|---|---|
| Bar chart etapas | `automargin=True` en eje Y, nombres completos visibles |
| Bump chart | Eje X categorico ordenado, marcadores con borde blanco |
| Gap chart | Eje Y con `rangemode="tozero"`, etapas ordenadas cronologicamente |
| Comparativa | Tiempos ordenados por `stage_id`, sin duplicados |

---

## Archivos modificados

```
backend/app/services/analytics.py   ← fix: eliminar merge redundante de stage_code
dashboard/components/charts.py      ← reescrito: paleta profesional + axes fixes
dashboard/pages/01_stages.py        ← sys.path fix + mejoras menores
dashboard/pages/02_evolution.py     ← sys.path fix + fix datos bump chart
dashboard/pages/03_compare.py       ← fix tabla duplicada + fix wins calculation
docs/bloque-04-graficos.md          ← este archivo
```

---

## Validaciones del Bloque 4

### V1 — Tests siguen pasando
```bash
pytest backend/tests/ -v
→ 51 passed
```

### V2 — Bump chart muestra todas las etapas
```
Pagina Evolucion → bump chart con SS1-SS5 en eje X
→ Cada piloto tiene una linea continua a traves de las 5 etapas
```

### V3 — Gap chart con ejes correctos
```
Pagina Evolucion → gap chart
→ Eje X: SS1-SS5. Eje Y: segundos. Lineas separadas por piloto
```

### V4 — Bar chart con nombres visibles
```
Pagina Etapas → bar chart
→ Eje Y muestra "Nombre Piloto #XX" para cada barra
```

### V5 — Tabla comparativa sin duplicados
```
Pagina Comparativa → tabla detalle
→ Exactamente 5 filas (una por etapa), sin repeticiones
```

### V6 — Paleta de colores profesional
```
Todos los graficos → colores sobrios, consistentes entre paginas
```

---

## Posibles errores comunes

| Error | Causa | Solucion |
|---|---|---|
| Graficos siguen en blanco | Cache del navegador | Ctrl+Shift+R para hard reload |
| `stage_code` vacio en DataFrame | Pipeline antiguo sin la columna | `rm data/processed/*.csv && WRC_USE_MOCK=true python -m ingestion.pipeline` |
| Bump chart con un solo punto | `stage_code` sigue siendo `stage_code_x` | Verificar que `analytics.py` esta actualizado |

---

*Siguiente: Bloque 5 — Pulido final, README y deploy.*
