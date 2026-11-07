---
name: local-ci
description: One recipe, two kitchens. Your GitHub Actions workflow, cooked on your own machine.
colors:
  ink: "#24292e"
  ink-soft: "#4a525a"
  cream: "#fcfaf4"
  card: "#fffdf7"
  rule: "#d9e4ec"
  coral: "#fd9b83"
  coral-press: "#fc8a6e"
  coral-wash: "#feeae3"
  green: "#38d084"
  gold: "#f1c362"
typography:
  display:
    fontFamily: "Kalam, Segoe Print, cursive"
    fontSize: "clamp(2.6rem, 6vw, 4.25rem)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Kalam, Segoe Print, cursive"
    fontSize: "clamp(1.9rem, 4vw, 2.75rem)"
    fontWeight: 700
    lineHeight: 1.08
  title-hand:
    fontFamily: "Kalam, Segoe Print, cursive"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: "1.75rem"
  title:
    fontFamily: "Atkinson Hyperlegible, system-ui, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 700
    lineHeight: 1.3
  lede:
    fontFamily: "Atkinson Hyperlegible, system-ui, sans-serif"
    fontSize: "clamp(1.15rem, 2vw, 1.35rem)"
    fontWeight: 400
    lineHeight: "1.75rem"
  body:
    fontFamily: "Atkinson Hyperlegible, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
  body-compact:
    fontFamily: "Atkinson Hyperlegible, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  small:
    fontFamily: "Atkinson Hyperlegible, system-ui, sans-serif"
    fontSize: "0.92rem"
    fontWeight: 400
    lineHeight: 1.5
  label-hand:
    fontFamily: "Kalam, Segoe Print, cursive"
    fontSize: "1.05rem"
    fontWeight: 700
    lineHeight: 1.3
  label:
    fontFamily: "Atkinson Hyperlegible, system-ui, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 700
    lineHeight: 1
  mono:
    fontFamily: "Courier Prime, ui-monospace, monospace"
    fontSize: "0.95em"
    fontWeight: 400
    fontFeature: "tnum"
rounded:
  focus: "3px"
  field: "4px"
  card: "6px"
  pill: "999px"
  circle: "50%"
spacing:
  line: "1.75rem"
  gutter: "1.25rem"
  column-gap: "clamp(1.5rem, 4vw, 3.5rem)"
  section: "clamp(3rem, 7vw, 5.5rem)"
  container: "72rem"
components:
  recipe-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "1.1rem clamp(1.25rem, 3.5vw, 2.75rem) 2rem clamp(1.75rem, 5vw, 3.75rem)"
  button-copy:
    backgroundColor: "{colors.coral}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0.5rem 0.85rem"
    width: "5.2rem"
  button-copy-hover:
    backgroundColor: "{colors.coral-press}"
  button-copy-done:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
  button-copy-fail:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.ink}"
  command-line:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.ink}"
    typography: "{typography.mono}"
    rounded: "{rounded.field}"
    padding: "0.25rem 0.4rem 0.25rem 0.9rem"
  prompt-slip:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    typography: "{typography.mono}"
    rounded: "{rounded.field}"
    padding: "0.6rem 0.9rem"
  output-panel:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    typography: "{typography.mono}"
    rounded: "{rounded.card}"
    padding: "1rem 1.2rem"
  step-number:
    backgroundColor: "{colors.coral-wash}"
    textColor: "{colors.ink}"
    rounded: "{rounded.circle}"
    size: "3rem"
---

# Design System: local-ci

## Overview

**Creative North Star: "The Recipe Card"**

The workflow YAML is a recipe card, and GitHub and the visitor's own machine are two kitchens cooking from it. Everything visual comes from that one object: cream index-card stock, pale blue ruled lines on a fixed 1.75rem pitch, a coral margin rule, ink borders, and headings in a handwritten weight. The page reads like a card in a kitchen drawer, not a SaaS product page or a hacker terminal.

Density is calm and predictable. One accent does most of the work (Coral), the ink is a near-black blue-grey rather than pure black, and motion is limited to a one-time ink line drawing in and the ingredient ticks being drawn, both of which turn off under reduced motion. Hand lettering carries the titles and nothing else. Running text is set in Atkinson Hyperlegible because the product's audience includes neurodivergent and low-vision readers. Typewriter mono marks literal things the visitor types or reads back.

The world uses a single mark vocabulary everywhere: a green-filled tick for covered, a coral-filled cross for GitHub-only, and a dashed circle with a question mark for "your decision". The illustration is flat hand-drawn ink with sparse fills, never photographic.

**Key Characteristics:**
- Cream card stock with a ruled 1.75rem baseline and a 2px coral margin rule
- 2px ink borders on cards and section dividers; nothing is borderless and floating
- Kalam for headings and labels only; Atkinson Hyperlegible for reading; Courier Prime for literals
- One three-mark vocabulary (tick, cross, dashed ask) reused on every surface
- Flat ink line illustration, one continuous line, a few charter-colour fills

## Colors

A warm paper palette: Ink on Cream, with Coral as the single working accent and Green kept for one meaning.

### Primary
- **Recipe Coral** (coral): the margin rule, the rule under the card title, Copy buttons, the drift highlight in terminal output, link underlines, text selection, and the fork node in the illustration. It is the hand of the person writing on the card.
- **Pressed Coral** (coral-press): Copy button hover only.
- **Coral Wash** (coral-wash): fill inside the circled step numbers in Method. A tint, never used for text.

### Secondary
- **Kitchen Green** (green): the fill of the "covered" tick mark. Nothing else.
- **Meter Gold** (gold): the copy-failed state of the Copy button, and the quota meter in the illustration.

### Neutral
- **Ink** (ink): all text, every border, the ruled-card edge, section dividers, the focus ring, the terminal output background, and the illustration line.
- **Soft Ink** (ink-soft): notes, captions, figcaption sub-lines, the dashed border of the prompt slip, scrollbar thumb.
- **Cream** (cream): the page background, the command-line field, and text on Ink.
- **Card Stock** (card): the card surface, a hair warmer and lighter than the page so the card reads as an object laid on it.
- **Rule Blue** (rule): the ruled lines on cards and the hairlines between table rows and ladder rows.

### Named Rules
**The One Meaning Rule.** Green means "covered" and appears only as the fill of the tick mark. A success state, a badge, or a highlight never takes Green. (The Copy button's success state is Ink with Cream text for this reason.)

**The Ink-Not-Black Rule.** Text and lines are Ink, never pure `#000`. Cream is the light, never pure `#fff`.

**The Two-Or-Three Rule.** From the Atypical charter accents, a composition uses Coral plus at most two others. Coral, Green and Gold are the system's set.

## Typography

**Display Font:** Kalam 700 (with Segoe Print, cursive)
**Body Font:** Atkinson Hyperlegible 400/700 (with system-ui, sans-serif)
**Label/Mono Font:** Courier Prime 400 (with ui-monospace, monospace)

**Character:** A handwritten title on a typed card. Kalam is the cook's hand writing the name and the headings; Atkinson does the reading; Courier Prime is the typewriter that set the literal ingredients. All three are self-hosted woff2 under the OFL.

### Hierarchy
- **Display** (Kalam 700, clamp(2.6rem, 6vw, 4.25rem), line-height 1, -0.01em): the title on a recipe card. One per card.
- **Headline** (Kalam 700, clamp(1.9rem, 4vw, 2.75rem), 1.08): section headings in the left column, balanced wrap.
- **Title, hand** (Kalam 700, 1.5rem on the 1.75rem line): headings inside a ruled card (Ingredients, Step 1). Tasting-notes title runs at 1.6rem.
- **Title** (Atkinson 700, 1.3rem, 1.3): step titles in Method. Steps are instructions, so they are set in the reading face.
- **Lede** (Atkinson 400, clamp(1.15rem, 2vw, 1.35rem), on the 1.75rem line): the card's one-sentence summary, max 36ch.
- **Body** (Atkinson 400, 1.0625rem, 1.65; 1rem under 560px): prose, max 66ch.
- **Label, hand** (Kalam 700, ~1.05–1.1rem): metadata keys (Serves, Needs, For), table headers, ladder levels, figcaption names, stacked-table field labels.
- **Label** (Atkinson 700, 0.85rem, 1): button text.
- **Mono** (Courier Prime 400, 0.95em, tabular numbers): code, commands, file names, scores and measurements.

### Named Rules
**The Hand-For-Names Rule.** Kalam sets titles, headings and short labels only. Sentences, instructions and anything over one line are Atkinson.

**The Literal-Is-Typed Rule.** Anything the visitor would type or read back from a tool (file names, commands, scores, timings) is Courier Prime. Numbers in tables use tabular figures.

## Layout

A single centred column, `min(72rem, 100% - 2.5rem)`. The hero is a two-column grid, 1.7fr card and 1fr illustration, with a column gap of clamp(1.5rem, 4vw, 3.5rem). Each later section is a 1fr/2fr grid: headline (and an optional short intro) on the left, content on the right. Sections are separated by a 2px Ink rule and padded clamp(3rem, 7vw, 5.5rem) top and bottom.

Inside a ruled card, vertical rhythm locks to the 1.75rem line: headings, list rows, the lede and table rows sit on it, and headings that must start a new line pad to 3.65rem so the next row lands back on the ruling.

At 860px the hero and section grids collapse to one column and the illustration caps at 26rem, centred. At 560px body drops to 1rem, the nav keeps only the GitHub link, command lines stack with the Copy button aligned right underneath, and the limits table turns into stacked rows: mark in a 2rem column, fields below with hand-lettered labels.

## Elevation & Depth

Mostly flat, with one object lifted: the recipe card. Depth comes from borders and the paper colour step (Card Stock on Cream) more than from shadow. Sections, tables, command fields and the output panel carry no shadow.

### Shadow Vocabulary
- **Card lift** (`box-shadow: 0 1px 0 #24292e, 0 18px 40px -22px rgba(36, 41, 46, 0.45)`): recipe cards only. A 1px ink edge for card thickness plus a soft, tucked ambient shadow below.

### Named Rules
**The One Object Rule.** Only recipe cards are lifted. Everything else lies flat on the page and separates by Ink rules or Rule Blue hairlines.

## Shapes

Corners are slightly softened, like cut card stock: 6px on cards and the output panel, 4px on command fields and prompt slips, 3px on the focus ring. Two round forms carry meaning: the pill (Copy button) is the only control, and the circle is reserved for marks and step numbers. Borders are drawn, not hairline: 2px Ink on cards, section dividers and table heads, 1.5px Ink on fields and buttons, 1.5px Rule Blue between rows. Dashed strokes mean "yours to decide or type": the ask mark's dashed circle and the prompt slip's dashed Soft Ink border.

## Components

### Buttons
Small, tactile and single-purpose. The Copy button is the only button.
- **Shape:** full pill (999px), 1.5px Ink border, minimum width 5.2rem so the label change doesn't shift layout.
- **Primary:** Coral fill, Ink label in Atkinson 700 0.85rem, padding 0.5rem 0.85rem.
- **Hover / Focus:** hover deepens to Pressed Coral over 160ms ease-out; active nudges down 1px; focus is the global 3px Ink outline at 3px offset.
- **Done:** Ink fill, Cream label, reads "Copied" for 1.8s. **Fail:** Gold fill, reads "Select it".

### Cards / Containers
- **Corner Style:** 6px.
- **Background:** Card Stock with Rule Blue lines every 1.75rem, starting 4.75rem down under a 2px Coral title rule; a 2px Coral vertical margin rule inset clamp(1rem, 3.2vw, 2.4rem) from the left.
- **Shadow Strategy:** card lift (see Elevation & Depth).
- **Border:** 2px Ink.
- **Internal Padding:** 1.1rem top, 2rem bottom, extra left padding to clear the margin rule.
- Recurs mid-page as the Tasting notes card, where a table sits directly on the ruling, and as the closing install card.

### Inputs / Fields
No form inputs. The **command line** is the field-like element: Cream fill, 1.5px Ink border, 4px corners, Courier Prime command on the left (horizontal scroll, never truncated) and a Copy button on the right; minimum height is two ruled lines.

### Navigation
A plain masthead: product name in Kalam 700 1.4rem on the left, Atkinson 700 0.95rem links on the right with no underline at rest and a Coral underline on hover. Under 560px only the GitHub link stays.

### Marks (signature component)
Three 24px inline SVG symbols, each a 10.5r circle with a 2px Ink stroke and a 2.6px rounded Ink glyph: **covered** = Green fill + tick, **GitHub-only** = Coral fill + cross, **your decision** = Card Stock fill, dashed (3 2.5) circle + question mark. Rendered at 1.5rem. Used in the ingredient list, the limits table and its legend. Decorative instances are `aria-hidden`; table instances carry `role="img"` and a label. The tick draws itself in once, staggered, unless reduced motion is set.

### Output panel
Real tool output on Ink: Cream Courier Prime at 0.86rem/1.55, 6px corners, padding 1rem 1.2rem, horizontal scroll, focusable. Only the drift marker is Coral. A Soft Ink caption below says what was edited for width.

### Method steps
An ordered list in a 3rem / 1fr grid. The counter is a 3rem circle: 2px Ink border, Coral Wash fill, Kalam 700 2.4rem numeral. Prompts the visitor should say are set in a **prompt slip**: Card Stock fill, 1.5px dashed Soft Ink border, Courier Prime.

### Ruled table and ladder
Tables use Kalam headers on a 2px Ink rule, 1.5px Rule Blue row hairlines, no last-row rule, and a Soft Ink caption below. The trade-off ladder is the same idea as a list: 7.5rem hand-lettered level, then the option, separated by Rule Blue hairlines.

## Do's and Don'ts

### Do:
- **Do** start new surfaces from the recipe card: Card Stock, 1.75rem Rule Blue ruling, 2px Coral margin rule, 2px Ink border, 6px corners.
- **Do** lock in-card text to the 1.75rem line; pad headings to 3.65rem when the following row must land on the ruling.
- **Do** use the three marks (tick, cross, dashed ask) wherever status is shown, with a legend nearby.
- **Do** set every literal (command, file, score, timing) in Courier Prime with tabular figures.
- **Do** separate sections with a 2px Ink rule and the 1fr/2fr headline-then-content grid.
- **Do** gate every animation behind `prefers-reduced-motion: no-preference`, and play it once.
- **Do** keep illustration flat hand-drawn ink, 3px round-capped strokes, sparse charter-colour fills.

### Don't:
- **Don't** use Green for anything except the fill of the covered tick, including success states.
- **Don't** set sentences or instructions in Kalam; it is for names, headings and short labels.
- **Don't** lift anything but recipe cards; other containers stay flat.
- **Don't** use pure black or pure white; use Ink and Cream.
- **Don't** add a fourth charter accent beyond Coral, Green and Gold to a composition.
- **Don't** dress the page as a hacker terminal: the Cream-on-Ink output panel shows real tool output, never decorative code.
