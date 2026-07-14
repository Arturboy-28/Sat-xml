# Sat-xml (borrador completo)

Borrador de un sistema de **descarga masiva de XML CFDI** vía **Web Service SAT v1.5**
(e.firma), con **exportador CONTPAQi Almacén Digital** y el resto de capacidades
habituales del mercado (metadata, Excel, multi-empresa, retenciones, auditoría, sync).

> Canal: **solo Web Service** (no portal / no CIEC).  
> Estado: **borrador**. Sin lógica programada.

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
| CLI | Comandos de sync, export, reportes y auditoría |

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
  fiel.py                 # e.firma
  soap.py / auth.py
  solicitud.py            # CFDI emitidos/recibidos/folio
  retenciones.py          # WS retenciones
  verificacion.py
  descarga.py
  particion.py            # partir rangos (tope 200k / 5003)
  estado.py               # cola IdSolicitud + reanudación
  inventario.py           # dedupe UUID / índice local
  metadata.py             # parse metadata TXT → estructuras
  reportes/
    excel_csv.py          # export Excel/CSV
  exportadores/
    contpaqi_add.py       # Almacén Digital CONTPAQi
  auditoria/
    faltantes.py          # metadata vs XML
    cancelados.py         # re-chequeo estatus
    lista_69b.py          # EFOS / 69-B
  pdf.py                  # representación impresa (opcional)
  scheduler.py            # sync diario
  empresas.py             # multi-FIEL / multi-RFC
  client.py / cli.py
docs/
  BORRADOR.md
  INVESTIGACION_MERCADO.md
fiel/{rfc}/               # una carpeta por empresa
downloads/
export/contpaqi_add/
export/reportes/
state/
listas/                   # archivos 69-B oficiales
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

- `docs/BORRADOR.md` — diseño completo de módulos y reglas
- `docs/INVESTIGACION_MERCADO.md` — origen de las features
