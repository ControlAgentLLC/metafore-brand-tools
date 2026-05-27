# Line Icons — Approved Library

The library holds 29 approved line icons, **bundled with this plugin** at `../../../assets/graphics/line-icons/` (relative to this file). **Use these first** before generating anything new. Reference an icon by filename in the output HTML (or embed the PNG directly) rather than redrawing in SVG.

**Runtime convention:** when generating HTML that uses these icons, copy them into a `Graphics/LineIcons/` folder next to the output file the first time (one-time bootstrap), then reference them as relative paths:

```
Graphics/LineIcons/{IconName}.png
```

If no library icon matches the concept you need, generate a new one that follows the visual language documented at the bottom of this file, save it to `Graphics/LineIcons/generated/` in the working directory, and flag it for review. (Promoted icons get added back to the plugin's `assets/graphics/line-icons/` in a future version.)

---

## Index — concept → file

Use this table to find the right approved icon for a concept. The "Use for" column lists the marketing concepts the icon naturally represents.

| File | Pattern | Use for |
|---|---|---|
| `Amplify.png` | 3 nested squares, black focal middle | Amplification, scale-up, growth from a core |
| `Axis.png` | Coordinate axes + ellipse on a plane + black node | Measurement, dimensions, plotted state, baseline |
| `Collaborate.png` | Two overlapping circles, intersection marked with black squares | Collaboration, partnership, shared boundary |
| `Connect.png` | Three isometric diamond planes in sequence, lined together | Connection, sequenced systems, linked stages |
| `Connected.png` | Three diamonds with a thin grey line passing through, two black connection squares | Integration, line-of-sight, threaded systems |
| `CrossSell.png` | Two adjacent squares + bi-directional arrows passing between them | Exchange, cross-sell, mutual flow, sync |
| `Cycle.png` | Outer grey arrow loop + inner black circle | Loop, cycle, iteration, feedback |
| `Detection.png` | Outer square with thin centered cross-line splitting it, inner small square accent | Detection, scope, isolate, focus |
| `Ellipses.png` | Four vertical ellipses light → dark, side by side | Progression, time series, sequencing, layered states |
| `Ensemble.png` | Rotated parallelogram crossing axes + grey companion shapes | Ensemble, composition, overlaid models |
| `Fan.png` | Three progressive ellipses light → dark with an arrow piercing them | Throughput, progression with direction, fan-out |
| `Icon1.png` | Four black nodes in a square, arrows looping clockwise inside a grey circle | Circular flow, lifecycle, recurring process |
| `Icon2.png` | Trio of circles, two grey outline (bottom-left, bottom-right) + one solid black bottom-center, connected to top circle | Choice, selection, root + alternatives |
| `Icon3.png` | Black-outline square with corner brackets and a tiny center black square | Focus, target, scope, scanned subject |
| `Integration.png` | Two abutting squares — solid grey outer + solid black inner — overlapping at a vertical line | Integration, merge, two-system join |
| `Measure.png` | Two concentric arcs above a horizontal line with a black square at the pivot | Measurement, gauge, range, threshold |
| `NestedSquares.png` | Three concentric/nested squares from light → mid → black, anchored bottom-right | Nesting, refinement, drill-down, hierarchy |
| `Nodes.png` | Six black nodes connected in two adjacent squares, inside a grey circle | Network topology, node graph, mesh |
| `Nodes2.png` | Two ellipses with two black nodes + two grey hollow nodes at intersection points | Orbital intersection, shared points, contact |
| `Orbit.png` | Three concentric circles + three planet nodes (black, mid, light) | Orbit, planetary model, layered system, gravity |
| `Process.png` | Black square with four light-grey circles around it, dashed connectors, inner black-outline circle | Process surrounded by inputs, hub-and-spoke, orchestration |
| `Scale.png` | Three nested squares (light → mid → black) anchored to bottom-right corner | Scale up, growth, expansion from a base |
| `Scale2.png` | Three nested squares (light → mid → black) inside coordinate axes | Measured growth, plotted scale, dimensioned expansion |
| `Squares.png` | Two overlapping squares — solid black + outline grey, offset | Overlap, intersection of two states, layered |
| `Squares2.png` | Three vertical plane outlines (light, black focal middle, light) with center accent square | Layered planes, parallel systems, stacked layers |
| `Stack.png` | Three stacked isometric planes (top light, middle black, bottom light-grey) | Stack, layered architecture, tiered system |
| `ThroughLine.png` | Three progressive ellipses with a dashed arrow piercing through left → right | Through-line, transformation arc, continuity, end-to-end |
| `Transform.png` | Source black-outline square + center black focal + L-shaped grey flow arrows to destination grey square | Transformation, source → target, conversion |
| `Venn.png` | Three-circle Venn diagram in light grey with a black intersection wedge | Convergence, three-way intersection, common ground |

---

## Quick-pick guide by concept family

When a teammate asks for an icon for a concept, scan this guide first:

**Growth / scale / amplification**
→ `Amplify`, `Scale`, `Scale2`, `NestedSquares`, `Fan`

**Connection / network / integration**
→ `Connect`, `Connected`, `Nodes`, `Nodes2`, `Integration`, `Process`

**Process / flow / cycle**
→ `Cycle`, `Icon1`, `ThroughLine`, `Transform`, `Process`

**Collaboration / overlap / intersection**
→ `Collaborate`, `Venn`, `Squares`, `Ensemble`

**Measurement / dimension / range**
→ `Axis`, `Measure`, `Scale2`

**Focus / detection / scope**
→ `Detection`, `Icon3`

**Progression / sequencing / layered states**
→ `Ellipses`, `Stack`, `Squares2`, `Orbit`

**Choice / branching**
→ `Icon2`, `Transform`

**Exchange / bi-directional**
→ `CrossSell`

---

## Using an approved icon in HTML

The library icons are PNGs. Two ways to use them inline in a graphic:

```html
<!-- Direct img reference -->
<img src="../Graphics/LineIcons/Amplify.png" alt="Amplify" width="120" height="80">

<!-- Or as a background-image so size is fully controllable -->
<div class="ic" style="background-image:url('../Graphics/LineIcons/Amplify.png');background-size:contain;background-repeat:no-repeat;background-position:center;width:120px;height:80px"></div>
```

Use the PNG at its native aspect ratio. Don't recolor it.

---

## When to generate a new icon

Two situations call for generation:

1. **The user explicitly asks for one.** Phrasing like "design a new icon for X", "make a fresh icon", "generate a custom icon for [concept]", "don't reuse — draw a new one", "create an icon from scratch" → generate directly, even if a library icon could have fit.
2. **No library icon fits the concept.** Scan the index above first; if nothing represents the idea, generate.

In both cases, the new icon must match the library exactly so it can be added to the approved set.

### Visual language

- **Pure greyscale on white.** No teal, no color of any kind. The line icons are the one place in the Metafore graphic system where brand teal does NOT appear — they live in a neutral zone so they read cleanly alongside teal-accented marketing surfaces.
- **Three-tier value hierarchy:**
  - **Focal — `#0A0A0A` / black.** Exactly ONE element per icon. The "thing being emphasized." Outline stroke or filled solid.
  - **Secondary — `#666666` / mid-grey.** The next layer of meaning.
  - **Background — `#CCCCCC` / light grey.** Supporting shapes, faded earlier states, tertiary context.
- **Strokes 1 to 1.5px.** Never thicker than 2px. Round caps and joins.
- **Fills only on small nodes** (~4–8px) at connection points. Solid black for the focal node, mid-grey for secondary, hollow circles outlined in light-grey for tertiary.
- **Generous whitespace.** Icon occupies the middle 50–70% of the frame; never edge-to-edge.
- **Geometric primitives only.** Circle, square, isometric diamond (rotated parallelogram), ellipse, line, simple arrow. No skeuomorphic detail. No iconography of literal objects (no airplane, no phone, no person silhouette).
- **Arrowhead apex at end of line.** When using directional arrows, the arrowhead's apex sits at the line's terminus — never floating before it.

### Compositional templates

When generating, start from one of the library's compositional patterns rather than inventing layouts from scratch.

| Pattern | Construction |
|---|---|
| **Concentric scaling** | Same shape repeated at 3 sizes, light → mid → black. Anchor at center, or anchor at corner for "growth from a base" feel. |
| **Trio with one accent** | Three identical shapes (circles, planes, ellipses) in a row or stacked. One is solid black; the others are light/mid grey outlines. |
| **Connected nodes** | 4–6 nodes (small filled squares or circles) arranged in a grid or polygon, connected by thin grey lines. One node black for emphasis. |
| **Overlap / Venn** | Two or three identical shapes overlapping. The intersection region marked — solid black wedge, or small filled black squares at the boundary crossings. |
| **Frame + subject** | Outer corner brackets (light grey L-shapes at each corner) framing a central black-outline shape with a small accent inside. |
| **Cycle / flow** | Closed loop of arrows around a central shape. Inner shape black; outer loop light grey with a small arrowhead. |
| **Axis / coordinate** | Perpendicular grey arrows defining a plane, with the focal subject (ellipse, square, parallelogram) positioned on or around the axes. |

### SVG starter

```css
.ic svg{width:80px;height:80px;fill:none;stroke-linecap:round;stroke-linejoin:round}
.ic svg .bg{stroke:#CCCCCC;stroke-width:1.2}      /* light-grey tertiary */
.ic svg .mid{stroke:#666666;stroke-width:1.2}     /* mid-grey secondary */
.ic svg .fg{stroke:#0A0A0A;stroke-width:1.5}      /* black focal */
.ic svg .node-bg{fill:#CCCCCC;stroke:none}
.ic svg .node-mid{fill:#666666;stroke:none}
.ic svg .node-fg{fill:#0A0A0A;stroke:none}
```

Use exactly ONE `.fg`/`.node-fg` element per icon. The rest of the composition is `.bg` and `.mid`.

### Save location

New icons → `Graphics/LineIcons/generated/{ConceptName}.svg` (or `.png` after raster export).

Flag for review. Approved icons are promoted by moving them to `Graphics/LineIcons/` directly.

---

## Forbidden in line icons

- **No teal or any brand color.** Greyscale only.
- **No strokes thicker than 2px.**
- **No more than one black focal element per icon.** The "one black thing" is the rule — adding more dilutes the focal hierarchy.
- **No skeuomorphic illustration.** Not a literal airplane, lock, person, document, etc. Use geometric abstraction.
- **No gradients or fills on outline shapes.** Outlines are strokes only; fills are reserved for tiny connection nodes.
- **No drop shadows.**
- **No backgrounds.** The icon sits on plain white (or transparent if used over a card).
