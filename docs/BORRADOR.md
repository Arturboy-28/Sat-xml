# Borrador de diseño — Descarga masiva SAT (Web Service 1.5)

Documento de diseño. **No es implementación.**

## Decisión de arquitectura

- Canal: **solo Web Service** del SAT.
- Auth: **e.firma (FIEL)**, no CIEC ni portal.
- Transporte: SOAP + WS-Security / firma XML.
- Token: header `Authorization: WRAP access_token="..."`.
- Destino contable: **exportador** para Almacén Digital (ADD) de
  **CONTPAQi Contabilidad** (archivos listos para importar; sin tocar SQL del ADD).

## Módulos previstos

| Módulo | Responsabilidad |
|--------|-----------------|
| `fiel` | Leer `.cer`/`.key`, RFC, firmar SHA1-RSA |
| `soap` | POST SOAP, parseo XML, firmas de solicitud |
| `auth` | Operación `Autentica` → token |
| `solicitud` | Emitidos / Recibidos / Folio |
| `verificacion` | Polling de `EstadoSolicitud` e `IdsPaquetes` |
| `descarga` | `Descargar` paquete + guardar ZIP/XML |
| `exportadores.contpaqi_add` | Empaquetar XML para Almacén Digital CONTPAQi |
| `client` | Orquestar descarga + export |
| `cli` | Comandos de usuario |

## Contratos (entrada / salida)

### Autenticación
- Entrada: FIEL
- Salida: token WRAP (vida corta; renovar al expirar)

### Solicitud
- Entrada: rango de fechas, tipo (emitidos/recibidos/folio), `TipoSolicitud` CFDI|Metadata, filtros opcionales
- Salida: `IdSolicitud`, `CodEstatus`, `Mensaje`

### Verificación
- Entrada: `IdSolicitud`
- Salida: estado (`1..6`), número de CFDIs, lista de paquetes

Estados:

1. Aceptada  
2. En proceso  
3. Terminada  
4. Error  
5. Rechazada  
6. Vencida  

### Descarga
- Entrada: `IdPaquete`
- Salida: bytes del ZIP (CFDI o Metadata)

### Exportador CONTPAQi ADD
- Entrada: carpeta de XML descargados, RFC empresa, tipo (emitidos/recibidos), periodo
- Salida:
  - Carpeta plana o por periodo con `{UUID}.xml`
  - ZIP opcional con XML **en la raíz** (formato que CONTPAQi suele aceptar al cargar)
  - `manifiesto.csv` (auditoría: UUID, fecha, RFCs, total, ruta)
- Uso en CONTPAQi Contabilidad:
  1. Empresa con RFC correcto y ADD creado
  2. `Empresa` → `Administrador del Almacén Digital`
  3. `Analizar directorio` sobre la carpeta/ZIP exportada
  4. Pestaña `Válidos` → `Importar todos`

## Reglas de negocio a respetar

1. Para XML recibidos: `EstadoComprobante=Vigente`.
2. Atributos firmados de `solicitud` en **orden alfabético**.
3. Partir rangos de fechas si una consulta supera el tope (~200k).
4. No re-solicitar con los mismos parámetros mientras exista una vigente.
5. Descargar paquetes antes de 72 h; máx. 2 descargas por paquete.
6. Guardar `IdSolicitud` / `IdsPaquetes` en estado local (archivo o DB simple).
7. En export CONTPAQi: validar que el RFC de empresa aparezca como emisor (emitidos) o receptor (recibidos).
8. En el ZIP de importación CONTPAQi: no anidar subcarpetas; XML en raíz.
9. No sobrescribir XML ya exportados sin flag explícito.

## Almacenamiento previsto

```text
downloads/
  {rfc}/
    {aaaa-mm}/
      paquetes/
        {id_paquete}.zip
      xml/
        {uuid}.xml
export/
  contpaqi_add/
    {rfc}/
      recibidos/{aaaa-mm}/{uuid}.xml
      emitidos/{aaaa-mm}/{uuid}.xml
      *.zip
      manifiesto.csv
state/
  solicitudes.json
```

## Fuera de alcance (v0)

- Portal SAT / CIEC
- Retenciones (puede añadirse después con otros hosts)
- UI web
- Parsing contable / reportes Excel
- Escritura directa a SQL Server / Lucene del ADD
- Generación automática de pólizas en CONTPAQi

## Criterios para pasar de borrador a código

- [ ] Confirmar FIEL de prueba o productiva disponible
- [ ] Definir defaults: solo `recibidos` + `CFDI` primero
- [ ] Definir política de reintentos y polling
- [ ] Validar con una carga real en CONTPAQi Contabilidad (Analizar directorio)
- [ ] Implementar módulos en el orden: fiel → auth → solicitud → verificación → descarga → exportador contpaqi → cli
