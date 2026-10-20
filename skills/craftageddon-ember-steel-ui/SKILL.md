---
name: craftageddon-ember-steel-ui
description: Create consistent Craftageddon Ember Steel interface assets, design tokens and motion states. Use for Pattern Forge, EmberChat, website/mobile UI, Figma components and Android visual concepts.
---

# Craftageddon Ember Steel UI

## Design constraints
- Brand baseline: dark forged metal, rich controlled ember emission, legible typography, fantasy-industrial craftsmanship; keep visuals visually consistent across Pattern Forge, EmberChat and Craftageddon app.
- Deliver individual usable assets (not just montages) with transparent variants, consistent naming, scale variants and state metadata.
- Never bake an orange glow permanently into the base artwork when runtime lighting is the requirement.
- Separate neutral material textures/masks, bright inner core, localized hot spots, bloom and reflected light; ensure both performance and readability.
- States: normal, focused, hovered, pressed, disabled, selected; document duration/easing, and reduced-motion alternative.
- Avoid gold/yellow button color when the user prefers darker button treatments; make labels fit without touching edges.
- Keep editable masters (Figma/SVG/source shaders) and export PNG/WebP as needed. Provide true transparency and file hashes.
- For Android prototypes, map visual assets to actual implementable rendering layers. Do not assume a launcher alone can restyle protected Android framework elements.
- V1 design/spec audit; V2 contrast, asset transparency, format, responsiveness and performance; V3 fresh independent target-device rendering comparison where possible.

## Scope protection
The Android 16 / AYN Thor 103-work-package roadmap Revision 1.1 is **REFERENCE ONLY**. This skill may prepare tokens/assets/workflows but MUST NOT begin ROM or OS implementation without fresh explicit permission.
