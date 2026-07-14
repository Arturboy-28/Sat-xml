# Stack y dirección visual — marca ALSUA

Documento de decisión. **No es implementación.**

## Formato de programación

| Capa | Tecnología | Motivo |
|------|------------|--------|
| Backend | **Python 3.10+** + **FastAPI** | FIEL, SOAP SAT, firmas y archivos |
| Motor SAT | Paquete `sat_xml/` | Reutilizable desde API y CLI |
| Frontend | **Vite + React** | UI moderna y atractiva |
| Estilos | CSS propio + tokens ALSUA | Identidad de marca |
| Datos | Carpetas + JSON en `state/` | Fácil respaldo |
| Extra | CLI `sat-xml` + scheduler | Automatización |
| Uso | App web local (`localhost`) | Escritorio contable |

## Marca: ALSUA

La interfaz lleva la identidad **ALSUA** (no un look genérico).

### Emblema

- Círculo naranja con **A** blanca inclinada
- Wordmark **LSUA** en naranja, bold itálico sans
- Marca registrada ®

Colocar el archivo oficial en:

```text
web/public/brand/alsua-logo.png
```

### Paleta ALSUA

```css
--alsua-orange: #F89D2D;   /* primaria / CTAs */
--alsua-orange-deep: #e07f10;
--alsua-white: #ffffff;
--alsua-ink: #1a1a1a;      /* texto */
--alsua-mute: #6b7280;     /* secundario */
--alsua-wash: #fff7ed;     /* fondo cálido suave */
--alsua-line: #f0e6d8;     /* bordes */
--ok: #2f9e6e;
--warn: #d4a017;
--danger: #c45c4a;
```

### Tipografía

- Marca / display: sans bold itálica (estilo del logo ALSUA) — p. ej. **Archivo Black Italic** / **Inter Tight Black Italic**
- UI: **Manrope** o **Plus Jakarta Sans**
- Mono (UUID / logs): **IBM Plex Mono**

### Atmósfera

- Fondo: blanco / wash naranja muy suave (no púrpura, no forestal oscuro)
- Acento dominante: naranja ALSUA
- Formas: esquinas redondeadas moderadas (como el logo)
- Motion: CTAs con leve inclinación/energía, progreso de sync fluido
- Hero: logo ALSUA a tamaño marca + producto “Descarga masiva CFDI”

## Pantallas

1. **Home** — logo ALSUA hero, empresas, CTA naranja “Sincronizar”
2. **Sync** — rango + tipo + progreso
3. **Inventario** — tabla limpia
4. **Export CONTPAQi** — 3 pasos
5. **Auditoría** — faltantes / cancelados / 69-B
6. **Reportes** — Excel/CSV

Reglas:

- La marca ALSUA debe dominar la primera vista (no solo un icono en nav)
- Una composición clara; sin dashboard saturado
- Sin badges flotantes sobre el hero
- Un CTA principal naranja por pantalla

## Estructura UI

```text
web/
  public/brand/alsua-logo.png
  src/
    styles/tokens.css
    pages/...
sat_xml/api.py          # FastAPI
```
