# Sat-xml (borrador)

Borrador de un sistema de **descarga masiva de XML CFDI** usando solo el
**Web Service del SAT v1.5** (e.firma / FIEL).

> No usa portal web ni CIEC.  
> Estado: **borrador / esqueleto**. Sin lógica programada.

## Alcance

| Incluye | No incluye |
|--------|------------|
| WS Autenticación, Solicitud, Verificación, Descarga | Scraping del portal SAT |
| CFDI emitidos / recibidos / por folio | Límite de 2,000 XML/día del portal |
| Extracción de paquetes ZIP → XML | Timbrado o cancelación de CFDI |
| CLI futura | UI / dashboard |

## Endpoints SAT (producción CFDI)

| Servicio | URL |
|----------|-----|
| Autenticación | `https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc` |
| Solicitud | `https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc` |
| Verificación | `https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc` |
| Descarga | `https://cfdidescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc` |

Operaciones de solicitud (v1.5):

- `SolicitaDescargaEmitidos`
- `SolicitaDescargaRecibidos`
- `SolicitaDescargaFolio`

## Flujo (diseño)

```text
FIEL (.cer + .key)
      │
      ▼
1. Autentica ──────────────► token WRAP
      │
      ▼
2. SolicitaDescarga* ──────► IdSolicitud
      │
      ▼
3. VerificaSolicitud ──────► Estado + IdsPaquetes
      │  (poll hasta Terminada)
      ▼
4. Descargar ──────────────► ZIP (base64)
      │
      ▼
5. Extraer XML en downloads/
```

## Límites relevantes del WS

- Hasta **~200,000** CFDI por solicitud (error `5003` si se excede).
- Mismos parámetros: límites/duplicados (`5002`, `5005`).
- Paquete: máx. **2 descargas**, vigencia **~72 h** (`5007`, `5008`).
- XML cancelados: en recibidos, descarga CFDI solo **Vigente**.
- Antigüedad: hasta 5 ejercicios + año en curso.

## Estructura del borrador

```text
sat_xml/
  __init__.py
  __main__.py
  fiel.py           # (pendiente) carga FIEL
  models.py         # (pendiente) enums / resultados
  soap.py           # (pendiente) HTTP SOAP + firma
  auth.py           # (pendiente) Autentica → token
  solicitud.py      # (pendiente) Emitidos/Recibidos/Folio
  verificacion.py   # (pendiente) VerificaSolicitud
  descarga.py       # (pendiente) Descargar + unzip
  client.py         # (pendiente) orquestación
  cli.py            # (pendiente) comandos
docs/
  BORRADOR.md       # diseño detallado
examples/
  .env.example
fiel/               # FIEL local (no versionar)
downloads/
tests/
```

## Requisitos previstos

- Python 3.10+
- FIEL vigente: `.cer`, `.key`, contraseña
- Dependencias planeadas: `cryptography`, `requests`, `lxml`

## Setup (cuando se implemente)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp examples/.env.example .env
# colocar FIEL en fiel/
```

## CLI futura (borrador)

```bash
sat-xml autenticar
sat-xml solicitar --tipo recibidos --desde 2026-01-01 --hasta 2026-01-31
sat-xml verificar --id <IdSolicitud>
sat-xml descargar --id <IdSolicitud>
sat-xml sync --tipo recibidos --desde 2026-01-01 --hasta 2026-01-31
```
