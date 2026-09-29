# Figma sources for TripUp

Paste-into-Figma files. Figma turns SVG into editable frames, vectors and text.

| File | What | Size |
|---|---|---|
| `brief.svg` | Section 0: the brief, and where each ask is answered (context, users, behaviours, scenario steps with screen numbers, deliverables, reviewer questions, constraints) | 2440 × 1221 |
| `wireflow.svg` | Section 1: the Lisbon scenario in 10 lo-fi screens. Numbered triggers on every arrow, decision diamonds, START/END, legend, decision (red) / state (green) / pattern (blue) callouts | 3505 × 2694 |
| `hifi-02-trip.svg` | Layer 2, key screen ★: 02 Trip group view | 393 × 852 |
| `hifi-06-poll.svg` | Layer 2, key screen ★: 06 Live poll | 393 × 852 |
| `*.png` | Previews rendered without the real fonts (serif fallback). In Figma the fonts resolve. | |
| `gen.py` | Generator. `python3 gen.py` rewrites the three SVGs. | |

## How to get them into the Figma file

1. Open the file in Figma desktop or browser.
2. Open an `.svg` in a text editor, select all, copy.
3. In Figma, press Cmd/Ctrl-V on the canvas. Figma pastes it as a frame.
4. Fonts: Figma will list Newsreader, Figtree and Open Sans as Google Fonts and load them automatically. If it shows a "missing fonts" warning, click it and choose the same names.
5. Drag `wireflow` into a section named "Wireflow" and the two hi-fi screens into "Hi-fi".

Alternative: drag the `.svg` file from Finder/Explorer onto the Figma canvas. Same result.

## Design tokens used

Colors, type and spacing follow the handoff spec: cream `#F7F3EC`, beige `#F1EBE2`, ink `#141414`, muted `#5C5750`, grey `#8A837A`, leading gradient `#FF7A3D → #FF5CA8`, leading border `#FF9AA8`, avatar fills A/N/M/T/S/R. Photos are gradient placeholders; drop the real Unsplash images into those rectangles as fills.
