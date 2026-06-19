# Nirukta Design System

## Design Mantra
Crisp, modern, sharp. Easy to understand, easy to navigate.

## Palette

| Token | Hex | Usage |
|---|---|---|
| Background | `#E8F0DE` | Page background (white + 15% green) |
| Dashlet / Card | `#FDF0E2` | Metric tiles and dashlet surfaces |
| Text | `#44546A` | Every piece of text, everywhere — one colour only |
| Surface | `#FFFFFF` | Cards, panels, nav, tables |
| Border | `#D5DCE8` | Hairline borders throughout |
| Status — Healthy | `#639922` | Green dot only — never used as text |
| Status — Warning | `#BA7517` | Amber dot only — never used as text |
| Status — Error | `#C0392B` | Red dot only |

## Rules

- **One text colour** — `#44546A` is used for every label, value, heading, and status string. No exceptions.
- **Status via dot** — health and severity are communicated by a small coloured dot next to the text, never by colouring the text itself.
- **Orange for elevation only** — `#FDF0E2` signals a metric dashlet. It carries no semantic meaning (not warning, not alert).
- **Green reserved for status** — the background green tint (`#E8F0DE`) and the healthy dot green (`#639922`) must stay visually distinct. Never use the dashlet colour on status elements.

## Typography

- Font: Inter
- Weights: 400 (body), 500 (labels, headings)
- Body: 13–14px
- Labels: 11px, opacity 0.7
- Page headings: 18–22px, weight 500

## Spacing

- Component padding: 10–14px
- Card gap: 8–12px
- Section gap: 24–32px

## Corner Radius

- Small elements (badges, dots): 4–6px
- Cards and inputs: 8px
- Large panels: 12px
