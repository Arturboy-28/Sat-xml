# Descarga automática inteligente (borrador)

Flujo al especificar un **rango de fechas** (emitidos o recibidos).

## Regla de oro

1. **Primero Metadata** (barata y hasta ~1,000,000 registros).  
2. Con el conteo real, **decidir**:  
   - Si cabe en **≤ ~200,000 XML** → una (o pocas) descarga(s) CFDI automática.  
   - Si **supera** → avisar y bajar **por tramos**, con **%** y **ETA**.

```text
Usuario elige fechas + tipo (emitidos/recibidos)
        │
        ▼
 Preflight METADATA del rango completo
        │
        ├─ Error / vacío ──► aviso y fin
        │
        ▼
 ¿Total CFDI (vigentes aplicables) ≤ 200,000?
        │
   Sí   │   No
        │    │
        ▼    ▼
  Descarga     Aviso: “Supera límite.
  CFDI auto    Se descargará por tramos.”
  (1 solicitud  │
   o mínima)    ▼
        │    Partir en tramos (mes → día → horas)
        │    hasta cada tramo ≤ 200k
        │         │
        └────┬────┘
             ▼
   Cola de solicitudes CFDI
             │
             ▼
   UI: tramo i/n · % global · ETA
             │
             ▼
   Extraer XML + inventario UUID
```

## Preflight (Metadata)

Entrada: `fecha_inicial`, `fecha_final`, `emitidos|recibidos`, RFC, filtros opcionales.

Pasos:
1. `TipoSolicitud = Metadata` sobre el rango (partir si Metadata misma pudiera acercarse a 1M).
2. Contar registros / CFDI aplicables a XML:
   - Recibidos XML → solo **Vigentes**
   - Emitidos → según filtro de estado
3. Guardar en `state/preflight_{rfc}_{rango}.json`: total, por día/mes, IdSolicitud metadata.

## Decisión

| Resultado preflight | Acción | Mensaje UI |
|---------------------|--------|------------|
| `total == 0` | No descarga CFDI | “No hay comprobantes en el rango.” |
| `total ≤ 200_000` | Auto CFDI del rango (o por mes si se prefiere) | “OK · Iniciando descarga automática (N XML).” |
| `total > 200_000` | Auto por **tramos** | “Supera el límite de 200,000. Se descargará en T tramos.” |

Siempre automático tras el aviso (no pedir confirmación salvo preferencia `confirmar_tramos=true`).

## Partición de tramos

Algoritmo (`sat_xml/particion.py`):

1. Agrupar conteos de metadata por **día** (o mes si el volumen es bajo).  
2. Empaquetar días consecutivos mientras `suma ≤ 200_000`.  
3. Si **un solo día** `> 200_000` → partir por **horas** (y luego por filtros tipo comprobante si hace falta).  
4. Cada tramo = una solicitud CFDI con su propio `IdSolicitud`.

## Progreso y ETA

### Porcentaje

```text
% = (xml_descargados_ok + xml_en_paquetes_listos) / total_estimado_preflight × 100
```

También mostrar: `Tramo 3/12 · 45% · 92,100 / 204,500 XML`.

### ETA

Estimación simple (suficiente para despacho):

```text
tiempo_por_xml ≈ promedio móvil de (duración_tramos_terminados / xml_de_esos_tramos)
ETA = tiempo_por_xml × xml_restantes
      + tiempo_espera_sat_promedio × tramos_pendientes
```

Mostrar: `ETA ~ 1 h 20 min` (actualizar cada tramo o cada poll).

Estados por tramo: `pendiente | solicitando | en_proceso | descargando | listo | error`.

## UI (Sync inteligente)

```text
┌──────────────────────────────────────────────┐
│ Preflight Metadata · Julio 2025–Junio 2026   │
│ Detectados: 540,200 XML · Límite: 200,000    │
│ ⚠ Supera límite → descarga por tramos (18)   │
│ ████████░░░░░░░░  45%   ETA 1h 12m           │
│ Tramo 8/18 · 2026-03-01 → 2026-03-12 · listo │
│ Tramo 9/18 · 2026-03-13 → 2026-03-22 · 62%   │
└──────────────────────────────────────────────┘
```

## Módulos

| Módulo | Responsabilidad |
|--------|-----------------|
| `preflight.py` | Metadata del rango + conteo |
| `particion.py` | Armar tramos ≤ 200k |
| `progreso.py` | % global, ETA, estado por tramo |
| `client.sync_inteligente()` | Orquestación automática |
| UI `Sync.tsx` | Aviso + barra + lista de tramos |

## Preferencias

```env
SAT_PREFLIGHT_METADATA=true
SAT_LIMITE_XML_SOLICITUD=200000
SAT_AUTO_TRAMOS=true
SAT_CONFIRMAR_TRAMOS=false
```

## Preview

Ver `docs/mockups/alsua-sync-tramos-preview.png`.
