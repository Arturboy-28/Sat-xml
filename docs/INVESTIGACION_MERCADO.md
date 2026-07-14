# Investigación: programas de descarga masiva SAT

Resumen de funcionalidades habituales en herramientas del mercado
(CONTPAQi XML en línea+, eComprobante/dSoft, DesMas, Facturando, iAudita,
librerías PhpCfdi/NodeCfdi/satcfdi, etc.) para enriquecer el borrador de Sat-xml.

> Solo investigación / diseño. Sin implementación.

## Qué ya contempla nuestro borrador

| Capacidad | Estado en borrador |
|-----------|--------------------|
| Canal Web Service SAT 1.5 + FIEL | Sí |
| Emitidos / recibidos / folio | Sí |
| Autentica → solicita → verifica → descarga | Sí |
| Exportador Almacén Digital CONTPAQi | Sí |
| Portal / CIEC | Fuera de alcance (a propósito) |

## Funcionalidades frecuentes en el mercado

### Núcleo de descarga (casi todos)

1. **Metadata además de CFDI** — TXT/resumen con UUID, RFCs, montos, estatus, fecha cancelación.
2. **Filtros de solicitud** — tipo (I/E/T/N/P), complemento, estado, RFC contraparte, a cuenta de terceros.
3. **Partición automática de rangos** — cortar meses/días para no pasar el tope (~200k) ni duplicar solicitudes.
4. **Cola / historial de solicitudes** — `IdSolicitud`, estatus, reintentos, reanudación.
5. **Deduplicación** — no volver a guardar el mismo UUID.
6. **Organización por carpetas** — RFC / año-mes / emitidos|recibidos / UUID.xml.
7. **Multi-empresa (multi-FIEL)** — varios RFC desde un mismo instalación/despacho.
8. **Scheduler / sync diario** — descargas automáticas sin intervención.
9. **Retenciones** — WS aparte (`retendescargamasiva...`), muchos productos lo incluyen.
10. **Manejo de errores SAT** — 5002/5003/5005/5007/5008/5011 con mensajes claros.

### Valor agregado (productos comerciales)

11. **Exportar a Excel/CSV** — listado de CFDI/metadata para auditoría.
12. **Generar PDF** (representación impresa) masivo.
13. **Validar estatus vigente/cancelado** — via metadata o consulta individual.
14. **Monitoreo de cancelaciones** — alertar CFDI que pasaron a cancelado.
15. **Listas negras 69 / 69-B (EFOS)** — cruzar RFC emisor/receptor.
16. **Detección de faltantes** — comparar metadata vs XML descargados vs pólizas.
17. **Validación estructural CFDI 4.0** — XSD / sellos / TimbreFiscalDigital.
18. **Visor de XML** — consulta rápida sin abrir archivos.
19. **Integración ADD / Contabilidad** — ya planeado (export carpeta/ZIP).
20. **Desglose de impuestos** — IVA, retenciones, bases en reportes.
21. **Correo / bandeja** — algunos recuperan XML también del mail (fuera de WS).
22. **NOM-151 / resguardo** — conservación documental a largo plazo.
23. **Dashboards** — totales por mes, top proveedores, mix de tipos.

## Propuesta para Sat-xml (priorizada)

### MVP (v0) — alineado al borrador actual

- WS CFDI: auth, solicitud, verificación, descarga
- Filtros básicos: fechas, emitidos/recibidos, tipo CFDI|Metadata
- Estado local de solicitudes + reanudación
- Extracción ZIP → `{UUID}.xml`
- Exportador CONTPAQi ADD (carpeta + ZIP + manifiesto)

### v1 — paridad “herramienta contable útil”

- Metadata → Excel/CSV
- Filtros: tipo comprobante, complemento, RFC contraparte
- Partición automática por mes (y fallback por día si `5003`)
- Deduplicación por UUID
- Multi-empresa (varias FIEL en `fiel/{rfc}/`)
- Retenciones (endpoints aparte)
- Logs claros de códigos SAT

### v2 — auditoría / cumplimiento

- Cruce metadata vs XML (faltantes)
- Alerta de cancelados (re-consulta metadata)
- Validación lista 69-B (archivo oficial SAT)
- Representación PDF (opcional, librería externa)
- Scheduler (`cron` / tarea programada) para sync diario

### Fuera de alcance recomendado

- Scraping portal / CIEC
- Contabilización automática de pólizas (eso es CONTPAQi)
- SaaS multi-tenant en la nube (salvo que se pida después)
- Escritura directa a SQL del ADD

## Comparativa rápida

| Feature | Portal SAT | WS puro | Comerciales tipicos | Sat-xml (propuesta) |
|---------|------------|---------|---------------------|---------------------|
| Volumen alto | Bajo (2k/día) | Alto (~200k/solicitud) | Alto | Alto (WS) |
| Metadata | Sí | Sí | Sí + Excel | v1 |
| Cancelados XML recibidos | Limitado | No (Vigente) | Detectan via metadata | v1/v2 |
| ADD CONTPAQi | Manual | N/A | Algunos | MVP |
| 69-B / EFOS | No | No | Sí | v2 |
| Multi-RFC | Manual | Manual | Sí | v1 |
| Sync automático | No | Hay que armarlo | Sí | v2 |

## Fuentes revisadas (mercado / docs)

- CONTPAQi XML en línea+ (descarga, ADD, PDF, reportes, multiempresa)
- eComprobante / dSoft (WS, metadata, dashboards, validaciones)
- DesMas / iAudita / Facturando (Excel, 69-B, cancelaciones, automatización)
- PhpCfdi / NodeCfdi sat-ws-descarga-masiva (filtros WS 1.5, retenciones)
- Documentación SAT descarga masiva (metadata TXT, topes, reglas cancelados)

## Decisión sugerida

Mantener el borrador centrado en **WS + export CONTPAQi**, y documentar el backlog
v1/v2 arriba para no inflar el MVP.
