# Borrador de diseño completo — Sat-xml

Documento de diseño. **No es implementación.**  
Alcance: **todo el roadmap** (núcleo WS + CONTPAQi + reportes + auditoría + sync).

## Arquitectura

- Canal: Web Service SAT 1.5 (CFDI y Retenciones).
- Auth: e.firma (FIEL), multi-empresa.
- Sin portal / sin CIEC.
- Persistencia local: archivos + `state/` (JSON).
- Destinos: disco organizado, CONTPAQi ADD, Excel/CSV, PDF opcional.

## Mapa de módulos

| Módulo | Responsabilidad |
|--------|-----------------|
| `empresas` | Registro multi-RFC / rutas FIEL |
| `fiel` | Cargar .cer/.key, firmar |
| `soap` | HTTP SOAP + firmas |
| `auth` | Token WRAP (CFDI y Retenciones) |
| `solicitud` | SolicitaDescargaEmitidos/Recibidos/Folio |
| `retenciones` | Mismo flujo en hosts de retenciones |
| `verificacion` | Estados 1–6 + IdsPaquetes |
| `descarga` | Descargar ZIP y extraer |
| `particion` | Cortar rangos por mes/día ante tope 200k / 5003 |
| `estado` | Cola IdSolicitud, reanudación, anti-duplicado 5005 |
| `inventario` | Índice UUID → ruta; dedupe |
| `metadata` | Parsear TXT metadata (~) a registros |
| `reportes.excel_csv` | Exportar listados a Excel/CSV |
| `exportadores.contpaqi_add` | Carpeta/ZIP para Almacén Digital |
| `auditoria.faltantes` | Metadata vs XML en disco |
| `auditoria.cancelados` | Detectar cancelaciones vía metadata |
| `auditoria.lista_69b` | Cruzar RFC vs listas SAT 69/69-B |
| `pdf` | Representación impresa (opcional) |
| `scheduler` | Sync diario (cron / tarea) |
| `client` | Orquestación end-to-end |
| `cli` | Interfaz de comandos |

## Contratos principales

### Auth
Entrada FIEL → token WRAP (renovar al expirar).

### Solicitud
Entrada: fechas, dirección (emitidos/recibidos/folio), `CFDI|Metadata`,
filtros (tipo comprobante, complemento, estado, RFC, a cuenta terceros).  
Salida: `IdSolicitud`.

### Verificación
Estados: 1 Aceptada, 2 En proceso, 3 Terminada, 4 Error, 5 Rechazada, 6 Vencida.

### Descarga
`IdPaquete` → ZIP (XML o metadata TXT).

### Metadata
Archivo TXT delimado por `~` → registros con UUID, RFCs, nombres, PAC,
fechas, monto, efecto, estatus, fecha cancelación.

### Export CONTPAQi ADD
Carpeta/`{UUID}.xml` + ZIP con XML en raíz + `manifiesto.csv`.  
Uso: Administrador del Almacén Digital → Analizar directorio → Importar todos.

### Reportes
Excel/CSV por RFC/periodo (desde metadata y/o XML parseado).

### Auditoría
- **Faltantes:** en metadata pero sin XML (o viceversa).
- **Cancelados:** vigentes en inventario local, cancelados en metadata nueva.
- **69-B:** RFC emisor/receptor contra archivo oficial en `listas/`.

### Scheduler
Job diario: sync recibidos (+ emitidos opcional) del día/mes anterior por cada empresa.

## Reglas de negocio

1. Recibidos XML: `EstadoComprobante=Vigente`.
2. Atributos firmados en orden alfabético.
3. Partir rangos si hay riesgo de `5003` (~200k).
4. No duplicar solicitudes vigentes (`5005` / `5002`).
5. Paquetes: máx. 2 descargas, ~72 h de vida.
6. Deduplicar UUID al guardar.
7. CONTPAQi: RFC empresa debe coincidir; ZIP sin subcarpetas.
8. Multi-empresa: nunca mezclar FIEL/RFC en la misma solicitud.
9. Listas 69-B: versionar fecha de archivo descargado del SAT.
10. Cancelados: no se pretende bajar XML cancelados recibidos por WS; se detectan con metadata.

## Almacenamiento

```text
fiel/{rfc}/certificado.cer
fiel/{rfc}/llave.key
downloads/{rfc}/{aaaa-mm}/paquetes/
downloads/{rfc}/{aaaa-mm}/xml/{uuid}.xml
downloads/{rfc}/{aaaa-mm}/metadata/
export/contpaqi_add/{rfc}/...
export/reportes/{rfc}/{aaaa-mm}.xlsx
state/solicitudes.json
state/inventario/{rfc}.json
listas/69b_YYYYMMDD.csv
```

## Orden de implementación (cuando se autorice programar)

1. `fiel` → `soap` → `auth`
2. `solicitud` / `verificacion` / `descarga` (CFDI)
3. `estado` + `particion` + `inventario`
4. `exportadores.contpaqi_add`
5. `metadata` + `reportes.excel_csv`
6. `empresas` (multi-FIEL)
7. `retenciones`
8. `auditoria.*`
9. `pdf` + `scheduler`
10. `cli` unificado

## Fuera de alcance

- Scraping portal / CIEC
- Escritura SQL directa al ADD
- Generación automática de pólizas CONTPAQi
- SaaS multi-tenant (salvo petición futura)
