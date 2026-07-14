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

### Emblema (logo oficial `IMG_2155.png`)

- Círculo naranja con **A** en negativo (fondo negro)
- Wordmark **LSUA** naranja, bold itálico
- Marca registrada ®
- **No rediseñar**: usar el archivo original

Archivos:

```text
IMG_2155.png                      # subido por el usuario
web/public/brand/alsua-logo.png   # copia exacta byte a byte
```

### Paleta ALSUA (del logo oficial)

```css
--alsua-orange: #F89E1B;   /* del logo — no alterar */
--alsua-black: #000000;    /* fondo del wordmark */
--alsua-white: #ffffff;
--alsua-ink: #111111;
--alsua-mute: #6b7280;
--alsua-wash: #141414;     /* UI oscura para respetar el logo */
--alsua-line: #2a2a2a;
```

### Tipografía

- Marca: el PNG oficial (nunca texto CSS fingiendo el logo)
- UI: **Manrope** o **Plus Jakarta Sans**
- Mono: **IBM Plex Mono**

### Atmósfera

- Fondo oscuro cercano al negro del logo
- Acento naranja ALSUA
- Hero: logo oficial a tamaño marca + producto “Descarga masiva CFDI”

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
