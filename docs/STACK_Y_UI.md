# Stack y dirección visual

Documento de decisión. **No es implementación.**

## Formato de programación elegido

| Capa | Tecnología | Motivo |
|------|------------|--------|
| Backend | **Python 3.10+** + **FastAPI** | Ideal para FIEL, SOAP SAT, firmas y archivos |
| Motor SAT | Paquete `sat_xml/` (ya esbozado) | Reutilizable desde API y CLI |
| Frontend | **Vite + React** | UI moderna, atractiva y rápida |
| Estilos | CSS propio + variables (sin tema “IA genérico”) | Control total del look |
| Datos locales | Carpetas + JSON en `state/` | Simple de respaldar |
| Automatización | CLI (`sat-xml`) + scheduler | Despachos / servidores |
| Empaque local | App web en `localhost` (abrir en navegador) | Fácil de usar en Windows contable |

**No usaremos:** Streamlit, Tkinter ni solo terminal como interfaz principal  
(la CLI queda como complemento para scripts).

## Arquitectura UI

```text
Navegador (UI React)
      │  HTTP / JSON
      ▼
FastAPI (API local)
      │
      ├─► sat_xml (WS SAT, FIEL, export, auditoría)
      ├─► downloads / export / state
      └─► CONTPAQi ADD (carpeta/ZIP listos)
```

## Dirección visual (marca Sat-xml)

Objetivo: que se sienta como una **herramienta profesional de despacho**,
no como un dashboard genérico ni un portal gubernamental gris.

### Identidad

- Nombre hero: **Sat-xml**
- Tagline corto: “Descarga masiva CFDI → Almacén Digital”
- Atmósfera: formal, limpia, con carácter

### Paleta (propuesta)

```css
--ink: #0e1a17;          /* fondo profundo */
--panel: #162420;        /* paneles */
--line: #2a3d36;         /* bordes suaves */
--mist: #d7e3dc;         /* texto secundario */
--paper: #f3f6f2;        /* texto principal sobre oscuro / fondos claros */
--accent: #c4a35a;       /* dorado oliva — CTAs (no púrpura) */
--ok: #3d9a6a;
--warn: #d4a017;
--danger: #c45c4a;
```

### Tipografía

- Display / títulos: **Fraunces** o **Libre Baskerville** (carácter, no Inter)
- UI / cuerpo: **Source Sans 3** o **IBM Plex Sans**
- Mono (UUID, logs): **IBM Plex Mono**

### Composición de pantallas

1. **Home / empresas** — marca Sat-xml grande, lista de RFC, CTA “Sincronizar”
2. **Sync** — una sola tarea: rango + tipo + botón; progreso visible
3. **Inventario** — tabla limpia de CFDI (sin cards decorativos)
4. **Export CONTPAQi** — flujo claro de 3 pasos
5. **Auditoría** — hallazgos (faltantes / cancelados / 69-B)
6. **Reportes** — descarga Excel/CSV

Reglas de UI:

- Primera vista = una composición (no dashboard saturado)
- Sin chips/badges flotantes sobre el hero
- Motion sutil: transición de paneles, barra de progreso de sync, fade de resultados
- Responsive: usable en laptop contable y pantalla ancha

## Estructura de carpetas (frontend)

```text
web/                 # React + Vite
  index.html
  src/
    main.tsx
    App.tsx
    styles/
      tokens.css     # variables de marca
      app.css
    pages/
      Empresas.tsx
      Sync.tsx
      Inventario.tsx
      ExportContpaqi.tsx
      Auditoria.tsx
      Reportes.tsx
    components/
api/                 # FastAPI (o sat_xml/api.py)
  main.py            # uvicorn entry
```

## Experiencia de uso objetivo

1. Abrir app → ver **Sat-xml** y tus empresas
2. Elegir RFC → Sync recibidos del mes
3. Ver progreso en vivo (solicitud → verificación → descarga)
4. Un clic: **Exportar a CONTPAQi**
5. Revisar auditoría / bajar Excel

## Qué queda en CLI

Mismos flujos para automatizar:

```bash
sat-xml sync --rfc ... --desde ... --hasta ...
sat-xml exportar contpaqi-add --rfc ... --mes ...
sat-xml auditar 69b --rfc ...
```
