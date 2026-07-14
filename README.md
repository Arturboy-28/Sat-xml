# Sat-xml

Esqueleto de un sistema de **descarga masiva de XML CFDI** vía el Web Service del SAT (versión 1.5).

> Estado: solo estructura de proyecto. Sin lógica implementada aún.

## Requisitos previstos

- Python 3.10+
- e.firma (FIEL): archivos `.cer`, `.key` y contraseña

## Estructura

```
sat_xml/
  __init__.py      # Paquete
  __main__.py      # python -m sat_xml
  fiel.py          # Carga de e.firma
  models.py        # Tipos y estados
  soap.py          # Cliente SOAP / firma
  auth.py          # Autenticación → token
  solicitud.py     # Emitidos / recibidos / folio
  verificacion.py  # Estatus de solicitud
  descarga.py      # Paquetes ZIP + XML
  client.py        # Orquestación
  cli.py           # Línea de comandos
tests/
examples/
  .env.example
fiel/              # Colocar aquí tu FIEL (no versionar)
downloads/         # Salida de XMLs/ZIPs
```

## Flujo objetivo (a implementar)

1. Autenticar con FIEL → token `WRAP`
2. Solicitar descarga (emitidos / recibidos / folio)
3. Verificar hasta estado terminada
4. Descargar paquetes y extraer XMLs

## Setup local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp examples/.env.example .env
```

## Comandos futuros

```bash
sat-xml autenticar
sat-xml solicitar --tipo recibidos --desde 2026-01-01 --hasta 2026-01-31
sat-xml verificar --id <IdSolicitud>
sat-xml descargar --id <IdSolicitud>
sat-xml sync --tipo recibidos --desde 2026-01-01 --hasta 2026-01-31
```
