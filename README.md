# Sat-xml (borrador completo)

App local de **descarga masiva CFDI** (Web Service SAT v1.5 + FIEL) con
**UI web atractiva**, exportador a **Almacén Digital CONTPAQi** y herramientas
de auditoría.

> Canal: **solo Web Service** (no portal / no CIEC).  
> Estado: **borrador**. Sin lógica programada.

## Formato de programación

| Capa | Stack |
|------|--------|
| Backend | Python + FastAPI + paquete `sat_xml/` |
| Frontend | Vite + React — UI marca **ALSUA** (naranja #F89D2D) |
| Extra | CLI `sat-xml` para automatización |

Detalle visual y pantallas (marca **ALSUA**): [`docs/STACK_Y_UI.md`](docs/STACK_Y_UI.md)

## Alcance (todo el roadmap)

| Área | Incluye |
|------|---------|
| Descarga WS | CFDI + Metadata + Retenciones; emitidos / recibidos / folio |
| Filtros | Tipo I/E/T/N/P, complemento, estado, RFC contraparte, a cuenta terceros |
| Operación | Partición de rangos, cola/historial, reanudación, dedupe UUID |
| Multi-empresa | Varias FIEL (`fiel/{rfc}/`) |
| Contabilidad | Export Almacén Digital (ADD) CONTPAQi Contabilidad |
| Reportes | Metadata → Excel/CSV; manifiesto de export |
| Auditoría | Faltantes metadata vs XML; alertas cancelados; lista 69/69-B |
| Extras | PDF representación (opcional); sync/scheduler diario |
| Interfaces | **UI web** (principal) + CLI |
| Dashboard CEO | Ingresos/egresos, pólizas, faltantes, impuestos, no deducibles |

## Flujo general

```text
FIEL(s) multi-empresa
        │
        ▼
   Autentica (token WRAP)
        │
        ▼
   Solicita (CFDI | Metadata | Retenciones)
   + partición de fechas / filtros
        │
        ▼
   Verifica (cola + reintentos)
        │
        ▼
   Descarga paquetes → XML / TXT metadata
        │
        ├─► Deduplicar UUID / organizar carpetas
        ├─► Export CONTPAQi ADD (carpeta + ZIP)
        ├─► Excel/CSV reportes
        ├─► Auditoría (faltantes, cancelados, 69-B)
        └─► PDF (opcional) + sync programado
```

## Estructura del borrador

```text
sat_xml/
  api.py                  # FastAPI (UI)
  fiel.py
  ...
web/                      # React + Vite (UI atractiva)
  styles/tokens.css.draft
docs/
  STACK_Y_UI.md           # stack + dirección visual
  BORRADOR.md
  INVESTIGACION_MERCADO.md
fiel/{rfc}/
downloads/
export/contpaqi_add/
export/reportes/
export/pdf/
state/
listas/
```

## Endpoints SAT (referencia)

**CFDI**

- Auth / Solicitud / Verificación: `cfdidescargamasivasolicitud.clouda.sat.gob.mx`
- Descarga: `cfdidescargamasiva.clouda.sat.gob.mx`

**Retenciones**

- Auth / Solicitud / Verificación: `retendescargamasivasolicitud.clouda.sat.gob.mx`
- Descarga: `retendescargamasiva.clouda.sat.gob.mx`

## CLI prevista

```bash
# Multi-empresa
sat-xml empresas listar
sat-xml empresas agregar --rfc AAA010101AAA --cer ... --key ...

# Descarga
sat-xml sync --rfc AAA010101AAA --tipo recibidos --desde 2026-01-01 --hasta 2026-01-31
sat-xml sync --rfc AAA010101AAA --tipo emitidos --solicitud Metadata
sat-xml sync-retenciones --rfc AAA010101AAA --desde 2026-01-01 --hasta 2026-01-31
sat-xml verificar --id <IdSolicitud>
sat-xml reanudar

# Export / reportes
sat-xml exportar contpaqi-add --rfc AAA010101AAA --mes 2026-01 --zip
sat-xml reportes excel --rfc AAA010101AAA --mes 2026-01

# Auditoría
sat-xml auditar faltantes --rfc AAA010101AAA --mes 2026-01
sat-xml auditar cancelados --rfc AAA010101AAA --mes 2026-01
sat-xml auditar 69b --rfc AAA010101AAA

# Automático
sat-xml scheduler instalar   # cron / tarea diaria
sat-xml pdf --rfc AAA010101AAA --mes 2026-01
```

## Setup (cuando se implemente)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp examples/.env.example .env
mkdir -p fiel/MI_RFC downloads export/contpaqi_add export/reportes state listas
```

## Docs

- `docs/STACK_Y_UI.md` — formato de programación + UI visual
- `docs/BORRADOR.md` — diseño de módulos y reglas
- `docs/INVESTIGACION_MERCADO.md` — origen de las features
- `docs/DASHBOARD_CEO.md` — vista ejecutiva + preview
