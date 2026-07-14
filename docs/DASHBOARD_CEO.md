# Dashboard CEO (borrador)

Vista ejecutiva para dirección. **No es implementación** — diseño + preview.

## Objetivo

Que el CEO/dueño vea en **un vistazo del mes**:
qué entró, qué salió, qué ya está contabilizado, qué falta,
y qué impuestos/pagos tienen riesgo fiscal (no deducibles).

## KPIs principales

| Bloque | Métrica | Fuente prevista |
|--------|---------|-----------------|
| Flujo | Ingresos vs egresos (monto y trend) | CFDI I / E (+P relacionados) |
| Contabilidad | Pólizas del mes | CONTPAQi / layout pólizas |
| Contabilidad | Pólizas contabilizadas | Pólizas con UUID asociado |
| Contabilidad | Faltantes | XML/metadata sin póliza (o viceversa) |
| Impuestos | Pagados | CFDI + complementos pago / declaraciones |
| Impuestos | Retenidos | Retenciones en CFDI / retenciones WS |
| Impuestos | Por pagar | Estimado mes (pagados vs causados) |
| Riesgo | No deducibles fiscalmente | Motor de reglas |
| Riesgo | Categorías del “por qué no” | Reglas + detalle |

## Categorías de no deducibles (lista inicial)

1. **Sin CFDI** — gasto sin UUID / sin XML  
2. **CFDI cancelado** — vigente en póliza, cancelado en SAT  
3. **RFC en 69 / 69-B** — EFOS / supuestos  
4. **No estrictamente indispensable** — gasto fuera de actividad  
5. **Fuera de plazo** — deducción en periodo incorrecto  
6. **Complemento incompleto** — pagos/nóminas/retenciones mal timbrados  
7. **Uso CFDI / forma pago inválidos** — para el tipo de deducción  
8. **Operación con partes relacionadas sin soporte** — (opcional)

Cada categoría muestra: **conteo**, **importe**, **% del no deducible**, link a detalle.

## Layout de pantalla

```text
┌─────────────────────────────────────────────────────────┐
│ ALSUA logo │ Dashboard CEO │ Mes ▾ │ Empresa ▾          │
├──────────────────────────────┬──────────────────────────┤
│                              │ KPIs:                    │
│  Ingresos vs Egresos (chart) │  Pólizas mes             │
│                              │  Contabilizadas          │
│                              │  Faltantes               │
│                              │  Impuestos pagados       │
│                              │  Retenidos / Por pagar   │
├──────────────────────────────┼──────────────────────────┤
│ No deducibles (monto / %)    │ Categorías ¿por qué no?  │
│                              │  lista con importes      │
└──────────────────────────────┴──────────────────────────┘
```

## Módulo previsto

```text
sat_xml/
  dashboard/
    ceo.py
    reglas_deduccion.py
web/src/pages/
  DashboardCeo.tsx
```

## Preview

Ver `docs/mockups/alsua-ceo-dashboard-preview.png`.

## Nota de alcance

- v0: descargar + export CONTPAQi + faltantes básicos  
- Dashboard CEO: fase posterior (parseo de montos/impuestos + vínculo a pólizas)
