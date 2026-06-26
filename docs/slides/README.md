# Presentaciones Marp — Capillas de la Fe

## Tema personalizado

Usamos el tema `capillas` definido en `theme-capillas.css`.
Paleta de grises corporativos, tipografía Inter, sin imágenes generadas por IA.

## Cómo usar

### Ver presentación en vivo

```bash
marp --theme theme-capillas.css --watch pitch-deck.md
```

### Exportar a PDF

```bash
marp --theme theme-capillas.css --pdf pitch-deck.md
```

### Exportar a HTML (autocontenido)

```bash
marp --theme theme-capillas.css --html pitch-deck.md
```

### Exportar a PPTX

```bash
marp --theme theme-capillas.css --pptx pitch-deck.md
```

## Atajos (vista en vivo)

| Tecla | Acción |
|-------|--------|
| `→` / `Space` | Siguiente slide |
| `←` | Slide anterior |
| `Shift + →` | Siguiente slide (animaciones) |
| `f` | Pantalla completa |
| `p` | Modo presentador (notas) |
| `Esc` | Vista general |

## Slides disponibles

| Archivo | Descripción |
|---------|-------------|
| `pitch-deck.md` | Presentación técnico-comercial |
| `theme-capillas.css` | Tema personalizado |

## Generación de imágenes

Ver `prompts-imagenes.md` para prompts listos para generar diagramas
técnicos con herramientas externas.
