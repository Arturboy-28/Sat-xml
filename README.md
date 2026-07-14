# Sat-xml (borrador)

Borrador de un sistema de **descarga masiva de XML CFDI** usando solo el
**Web Service del SAT v1.5** (e.firma / FIEL), con **exportador** hacia el
**Almacén Digital (ADD) de CONTPAQi Contabilidad**.

> No usa portal web ni CIEC.  
> Estado: **borrador / esqueleto**. Sin lógica programada.

## Alcance

| Incluye | No incluye |
|--------|------------|
| WS Autenticación, Solicitud, Verificación, Descarga | Scraping del portal SAT |
| CFDI emitidos / recibidos / por folio | Límite de 2,000 XML/día del portal |
| Extracción de paquetes ZIP → XML | Timbrado o cancelación de CFDI |
| Exportador CONTPAQi ADD (carpeta/ZIP) | Integración SQL directa al ADD |
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
4. Descargar ──────────────► ZIP SAT
      │
      ▼
5. Extraer XML
      │
      ▼
6. Exportar CONTPAQi ADD ──► carpeta / ZIP listos para importar
```

## Exportador CONTPAQi Contabilidad (ADD)

Objetivo: dejar XML listos para cargar en el **Administrador de Documentos
Digitales / Almacén Digital** de CONTPAQi Contabilidad.

### Cómo se importa en CONTPAQi (referencia)

1. Abrir empresa (RFC debe coincidir con los XML).
2. `Empresa` → `Administrador del Almacén Digital` (o Visor de documentos digitales).
3. `Analizar directorio` / `Cargar XML` apuntando a la carpeta o ZIP generado.
4. Revisar pestaña **Válidos** → `Importar todos`.

### Salida prevista del exportador

```text
export/contpaqi_add/
  {RFC}/
    recibidos/
      2026-01/
        {UUID}.xml
    emitidos/
      2026-01/
        {UUID}.xml
    contpaqi_add_recibidos_2026-01.zip   # XML en la raíz del ZIP
    manifiesto.csv                      # UUID, tipo, fecha, RFCs, ruta
```

Reglas de diseño:

- XML **sueltos** (no anidados en subcarpetas dentro del ZIP de importación).
- Nombre de archivo = **UUID** del CFDI.
- Filtrar por RFC de la empresa (emisor o receptor según emitidos/recibidos).
- Opcional: solo CFDI vigentes; excluir cancelados si se pidió metadata.
- No escribe en la base SQL del ADD: solo prepara archivos para importación manual/asistida.

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
  fiel.py
  models.py
  soap.py
  auth.py
  solicitud.py
  verificacion.py
  descarga.py
  client.py
  cli.py
  exportadores/
    __init__.py
    contpaqi_add.py   # exportador Almacén Digital CONTPAQi
docs/
  BORRADOR.md
examples/
  .env.example
fiel/
downloads/
export/               # salida para CONTPAQi
state/
tests/
```

## Requisitos previstos

- Python 3.10+
- FIEL vigente: `.cer`, `.key`, contraseña
- Dependencias planeadas: `cryptography`, `requests`, `lxml`
- CONTPAQi Contabilidad con Almacén Digital (ADD) creado y RFC correcto

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
sat-xml exportar contpaqi-add --tipo recibidos --mes 2026-01 --zip
```

## Roadmap (investigación de mercado)

Ver `docs/INVESTIGACION_MERCADO.md`.

| Fase | Ideas tomadas de programas tipicos |
|------|-------------------------------------|
| **MVP** | WS CFDI, cola de solicitudes, export ADD CONTPAQi |
| **v1** | Metadata→Excel, filtros, partición rangos, multi-RFC, retenciones |
| **v2** | Cancelados, faltantes, 69-B, PDF, sync diario |