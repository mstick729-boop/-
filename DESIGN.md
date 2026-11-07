---
name: Хитър Петър
description: The restaurant's own sign, lit at night above its hidden garden in Plovdiv.
colors:
  night: "#0A1612"
  canopy: "#10221B"
  moss: "#183128"
  leaf: "#23453A"
  text: "#ECE4D2"
  muted: "#A9B5AA"
  line: "rgba(236, 228, 210, .14)"
  neon: "#FFE6C9"
  neon-1: "#FFB373"
  neon-2: "#FF7A33"
  neon-dim: "#9C8C78"
  bulb: "#FFD7A6"
  enamel: "#C7372A"
  enamel-deep: "#A0281E"
  enamel-ink: "#FFF4E4"
  paper: "#F2E6CF"
  postcard: "#FBF5EA"
  ink: "#221C16"
  ink-muted: "#66594A"
  ink-line: "rgba(34, 28, 22, .22)"
  error-ink: "#9E2318"
  street-blue: "#1F3E6B"
  street-white: "#F6F0E2"
typography:
  neon-sign:
    fontFamily: "Marck Script, Segoe Script, cursive"
    fontSize: "clamp(88px, 12.4vw, 200px)"
    fontWeight: 400
    lineHeight: 0.9
    letterSpacing: "0em"
  display:
    fontFamily: "Oranienbaum, Times New Roman, Georgia, serif"
    fontSize: "clamp(52px, 6.4vw + 10px, 124px)"
    fontWeight: 400
    lineHeight: 0.92
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Oranienbaum, Times New Roman, Georgia, serif"
    fontSize: "clamp(44px, 4.4vw + 10px, 92px)"
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Oranienbaum, Times New Roman, Georgia, serif"
    fontSize: "clamp(34px, 2.4vw + 14px, 56px)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "-0.01em"
  dish-name:
    fontFamily: "Oranienbaum, Times New Roman, Georgia, serif"
    fontSize: "clamp(21px, .5vw + 17px, 25px)"
    fontWeight: 400
    lineHeight: 1.2
  body:
    fontFamily: "Onest, Segoe UI, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.65
  lead:
    fontFamily: "Onest, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(18px, .5vw + 15px, 21px)"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Onest, Segoe UI, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 500
    lineHeight: 1
  price:
    fontFamily: "Onest, Segoe UI, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 500
    lineHeight: 1
    fontFeature: "tnum, lnum"
  script-note:
    fontFamily: "Marck Script, Segoe Script, cursive"
    fontSize: "21px"
    fontWeight: 400
    lineHeight: 1
rounded:
  rule: "3px"
  card: "6px"
  field: "8px"
  control: "10px"
  plaque: "12px"
  street: "18px"
  pill: "999px"
spacing:
  gutter-phone: "20px"
  gutter: "40px"
  column-gap: "24px"
  plaque-gap: "12px"
  wrap: "1320px"
  nav: "76px"
  nav-phone: "60px"
components:
  plaque-enamel:
    backgroundColor: "{colors.enamel}"
    textColor: "{colors.enamel-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.plaque}"
    padding: "0 28px"
    height: "56px"
  plaque-enamel-hover:
    backgroundColor: "{colors.enamel-deep}"
  plaque-cream:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.plaque}"
    padding: "0 28px"
    height: "56px"
  plaque-cream-hover:
    backgroundColor: "#FFF5E3"
  plaque-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    rounded: "{rounded.plaque}"
    padding: "0 28px"
    height: "56px"
  plaque-small:
    padding: "0 20px"
    height: "46px"
  menu-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "clamp(28px, 4vw, 64px)"
  menu-tab:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "10px 18px"
  menu-tab-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  postcard:
    backgroundColor: "{colors.postcard}"
    textColor: "{colors.ink}"
    padding: "10px 10px 40px"
  street-plaque:
    backgroundColor: "{colors.street-blue}"
    textColor: "{colors.street-white}"
    rounded: "{rounded.street}"
    padding: "clamp(28px, 3.4vw, 52px) clamp(28px, 4vw, 64px)"
  order-pad-field:
    backgroundColor: "{colors.postcard}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "10px 14px"
    height: "50px"
  occasion-chip:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    rounded: "{rounded.pill}"
    padding: "8px 16px"
  menu-nav-pill-active:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.night}"
    rounded: "{rounded.pill}"
    padding: "10px 16px"
---

# Design System: Хитър Петър

## Overview

**Creative North Star: "The Lit Sign Above the Hidden Garden"**

Every surface is an evening visit to the restaurant. The ground is a night garden, deep green going to black. On it hang the things a Balkan restaurant actually puts in front of a guest after dark: its name in a warm neon tube of script, red enamel plaques that say what to do, the restaurant's own photographs as white-bordered postcards pegged to a string of bulbs, a cream printed menu card with dotted price leaders, and a blue enamel street plaque with the address. Nothing is a generic card or a flat panel; each container is one of these objects, and its material decides its colour, corner and shadow.

Density is low and theatrical on the night ground (huge script, few words, one scene per screen) and high and orderly on the paper (two columns of dishes, tabular prices). The two never blend: night-ground surfaces glow, paper surfaces are printed. Motion is the sign switching on: tubes flicker and hum, bulbs light one by one, the leaf wall parts on scroll, postcards drop and swing, the menu wipes in like a turned page. Every one of these keeps a reduced-motion form built from opacity, glow, blur and clip, because the client's own machine runs with reduced motion; the motion is translated, never removed.

**Key Characteristics:**
- Night-garden green ground (`night`, `canopy`, `moss`, `leaf`) with warm radial glows, never a pale page.
- Three faces with fixed jobs: Marck Script for light, Oranienbaum for speech, Onest for information.
- Actions are enamel plaques; nothing else is a button.
- Photographs are objects (postcards) or scenes (full-bleed with night shade), never bare grid tiles.
- Paper is a separate material with its own ink, its own red, and no glow.
- A two-tier motion grammar: movement under full motion, light and clarity under reduced motion.

## Colors

A night palette of four greens, one warm neon family, one red enamel family and one cream paper family, plus a single cobalt reserved for the street plaque.

### Primary
- **Enamel Red** (`enamel`): the call and reserve plaques, the order pad's header band, text selection. On the night ground it is the only saturated solid; it means "act".
- **Fired Enamel** (`enamel-deep`): plaque hover, and red ink on paper (the menu's script subtitles, group names, category counts).
- **Enamel Ink** (`enamel-ink`): text on red plaques.

### Secondary
- **Neon Tube** (`neon`): the lit core of script; always paired with the glow stack.
- **Amber Halo** (`neon-1`) and **Hot Orange Halo** (`neon-2`): the inner and outer layers of the glow, the focus ring on night surfaces, the nav underline, the search focus border.
- **Unlit Tube** (`neon-dim`): neon text before it is switched on by scroll.
- **Bulb Filament** (`bulb`): bulbs on the string, list bullets (with an amber halo), the lit open-now lamp.

### Tertiary
- **Street Cobalt** (`street-blue`) and **Street White** (`street-white`): the enamel street plaque only.
- **Brass hardware** (gradient `#d9c08f` to `#a8864f`): the postcard clips only; metal, never text. Carried as a literal, not a token.

### Neutral
- **Night Garden** (`night`): page ground, drawer, header when scrolled (at 90%), action bar (at 96%).
- **Canopy** (`canopy`): input fill on night (menu search).
- **Moss** (`moss`): the radial pool of light under the menu card.
- **Leaf Wall** (`leaf`): the leaf wall panels, scrollbar thumb, hero corner glow.
- **Candlelit Linen** (`text`) and **Sage Grey** (`muted`): text and secondary text on night.
- **Night Rule** (`line`): hairlines on night.
- **Menu Paper** (`paper`): the menu card, order pad, cream plaque, active menu-nav pill, footer logo plate.
- **Postcard White** (`postcard`): postcard borders, fields on the pad, lightbox frame.
- **Menu Ink** (`ink`), **Faded Ink** (`ink-muted`), **Ink Rule** (`ink-line`): text, secondary text and rules on paper.
- **Error Ink** (`error-ink`): field errors on paper.

### Named Rules
**The Act-In-Red Rule.** On the night ground, solid enamel red appears only on things you press to call, reserve or send. Its scarcity is what makes the phone number findable.

**The Glow-Needs-Night Rule.** The neon glow stack exists only on night surfaces. On paper the same script is printed in `enamel-deep` with no shadow.

## Typography

**Neon Font:** Marck Script (with Segoe Script, cursive)
**Display Font:** Oranienbaum (with Times New Roman, Georgia, serif)
**Body Font:** Onest (with Segoe UI, system-ui, sans-serif)

All three are self-hosted WOFF2, split into Cyrillic and Latin subsets by `unicode-range`; copy is Bulgarian first.

**Character:** a hand-bent neon script, a condensed high-contrast Cyrillic display that reads like a painted sign, and a plain modern grotesque for every fact. Light, speech, information.

### Hierarchy
- **Neon sign** (400, clamp 88–200px; 76–120px on phones, 0.9): the restaurant name in the hero, footer sign (84–260px), inner-page H1s (72–168px), the phone number (50–84px), feature figures (72–140px).
- **Display** (400, clamp 52–124px, 0.92, -0.02em): the leaf-wall words.
- **Headline** (400, clamp 44–92px, 0.95): section titles on night and the menu card title.
- **Title** (400, clamp 34–56px, 1.0): sub-section titles; hero H1 runs at 34–60px, 1.02.
- **Dish name** (400, 21–25px, 1.2): Oranienbaum on paper.
- **Body** (400, 17px, 1.65) and **Lead** (18–21px, 1.6): measure held to 30–42em.
- **Label** (500, 15–16px): nav, plaques, tabs, chips.
- **Price** (500, 17px, tabular lining figures); the BGN equivalent sits beside it at 13px in faded ink.
- **Script note** (Marck Script 21–34px): postcard captions, lightbox caption, red script on paper.

### Named Rules
**The Three Jobs Rule.** Script is light, Oranienbaum is speech, Onest is fact. A price, hour or address is never set in script or display; the name of the place is never set in Onest.

**The Tabular Facts Rule.** Every price, phone number and capacity uses tabular lining numerals.

## Layout

A 1320px wrap with 20px gutters on phones and 40px from 760px (both respecting safe-area insets). Inside it, a 12-column grid with 24px column gaps; the hero puts copy on columns 1–7 and the postcard fan on 8–12, the visit section photo on 1–5 and signage on 7–12, the order pad on 7–12. Breakpoints: 1080px (nav collapses to the drawer, grids stack, fan moves below copy), 860px (feature splits stack), 760px (phone: 60px header, fixed bottom action bar of two plaques at 1.3fr / 1fr, menu goes to one column, tabs scroll horizontally), 560px (footer and form to one column).

Sections are scenes, each roughly one viewport: hero at 100svh, the leaf wall as a 230vh sticky scroll stage (200vh on phones), the feast photo at 112svh, generous vertical padding (96–168px) elsewhere. The header is transparent over the hero with the brand hidden until scrolling, then becomes 90% night with a 12px blur and a hairline.

## Elevation & Depth

Depth is physical, not interface: objects hang or lie on the night ground and cast long, soft, dark shadows downward. Light comes from the objects themselves (neon, bulbs) as coloured glow. There is no tonal elevation scale; a surface is either ground or an object.

### Shadow Vocabulary
- **Neon glow** (`0 0 1px #fff7ec, 0 0 8px #FFB373, 0 0 22px #FF7A33, 0 0 46px rgba(255,110,40,.55), 0 0 96px rgba(255,90,30,.32)`): text-shadow on lit script only.
- **Bulb halo** (`drop-shadow(0 0 6px rgba(255,170,90,.9))`, bullets `0 0 8px #FF9B4A`): small light sources.
- **Postcard drop** (`0 30px 60px -20px rgba(0,0,0,.75), 0 8px 16px -8px rgba(0,0,0,.5)` plus a 1px inset highlight): photographs hung or lying.
- **Card on table** (`0 50px 100px -40px rgba(0,0,0,.85)`): menu card and order pad.
- **Plaque lift** (`inset 0 0 0 1px rgba(255,255,255,.14), 0 10px 24px -10px rgba(0,0,0,.6)`): enamel edge plus a short cast shadow.
- **Street plaque** (`inset 0 0 0 6px #1F3E6B, inset 0 0 0 9px #F6F0E2, 0 30px 70px -30px rgba(0,0,0,.8)`): the painted white border inside the enamel.

### Named Rules
**The Objects Cast, Ground Glows Rule.** Shadows belong to objects and always fall downward and soft; colour light belongs to neon and bulbs. Nothing on the ground gets a shadow, and no object glows.

## Shapes

Corners follow the material. Enamel plaques are pressed metal (12px); the street plaque is a larger sign (18px) with two screw heads at mid-height and an inset white painted border; printed paper is barely rounded (6px) with a 1px ink rule inset 12px (3px corners); fields and segmented choices are 8px; outline controls (menu toggle, drawer close, lightbox close) are 10px; tabs, nav pills, occasion chips and the search field are full pills; rail arrows are 52px circles. Postcards have square corners, a 10px white border and a deeper 40px bottom margin for the caption, and sit rotated between -6° and +5°; on the rail each hangs from a brass clip and pivots from a point 30px above it.

## Components

### Enamel plaques (buttons)
Tactile, enamel-sign actions; the only buttons in the system.
- **Shape:** 12px corners, 56px tall (46px small, 50px in the phone bar), 28px side padding, optional 18px stroke icon.
- **Red:** `enamel` on `enamel-ink`; hover deepens to `enamel-deep`. Used for calling and reserving.
- **Cream:** `paper` on `ink`; hover lightens to `#FFF5E3`. Used for "the menu" and secondary destinations.
- **Ghost:** transparent with a 1.5px linen rim at 45%; hover fills 8% linen. Used for the inquiry.
- **States:** press scales to 0.97 in 160ms ease-out; hover only on fine pointers; focus ring 2px `neon-1` offset 3px (2px `enamel` on paper).

### Text link
Medium weight with a 1px drawn underline that retracts right on hover (300ms) while the arrow nudges 4px.

### Navigation
Small set text (15px, 500) along the top, with a 1px amber underline that grows from the left on hover and stays drawn for the current page. Below 1080px it becomes a 10px-cornered outline "Menu" toggle opening a full-screen night drawer that expands as a circle from the toggle (620ms in, 520ms out, `ease-in-out`), with links in Oranienbaum 44–64px fading in 60ms apart and the current page lit as neon. On phones a fixed bottom bar always holds the call plaque and a second plaque.

### Neon script
The name and page titles. `switch-on` flickers on once over 1.6s and then hums (opacity 1 to 0.9 over 5s); under reduced motion it glows in over 1.4s instead. `neon--dim` text sits unlit in `neon-dim` until it scrolls into view, then lights over 900ms. The open-now lamp is a 10px bulb, lit with a double halo when the restaurant is open and grey when closed.

### Postcards
The restaurant's own photographs. White border, 4:3 image, Marck Script caption bottom-left in `#4a3f33`. In the hero three fan out and fan wider on hover; under full motion they drop in (40px, scale 1.06 to 1, 900ms staggered 150ms) and lean toward the pointer; under reduced motion they fade from 6px blur. On the rail they hang from brass clips under a string of bulbs, snap-scroll, drag with the mouse, straighten and lift 6px on hover with the photo zooming to 1.04; arriving, they swing in from four times their tilt (900ms, staggered 90ms), or under reduced motion clear from 4px blur. Gallery postcards tilt in a 3/4-step pattern. All open a lightbox on night at 96% with a 10px postcard frame and swipe on touch.

### String of bulbs
An SVG wire (linen at 28%) with filament bulbs that light in sequence 70ms apart, then twinkle to 45% on 3.6s or 4.4s cycles. The same motion in both modes, since it is light, not movement.

### Leaf wall
A sticky scroll scene: two leaf-photo panels with "Зад стена" in Oranienbaum and "от зеленина" in neon part outward to reveal the garden photograph, which settles from 1.18 scale; copy fades in in the last 14% of the scroll. Under reduced motion the leaves stay put and dissolve by opacity, and the photo does not scale.

### Menu card (on the table)
Cream paper in a moss pool of light, 6px corners, inset ink rule, Oranienbaum title with a red script subtitle. Pill tabs in ink outline; the selected tab inverts to ink. Switching tabs wipes the panel in left to right with a clip (560ms, `ease-in-out`), identical in both motion modes. Dishes run in two columns with a 2px dotted leader to the tabular price; one column on phones. The full menu page stacks one paper sheet per category under a sticky night bar with pill links (active = paper on night) and a pill search field that focuses in amber.

### Street plaque
Cobalt enamel with a painted white inset border, two screw heads, the street name in Oranienbaum 44–96px and "Пловдив · Упътване" with an arrow. It links to directions; on hover it tilts -0.6° and scales 1.01 while the arrow moves 5px. Screws drop and padding tightens on phones.

### Order pad (inquiry form)
Paper with a 14px enamel band across the top. Fields are postcard-white with a 1.5px ink rim at 30%, 8px corners, 50px tall; focus darkens the rim to ink with a 3px red halo; errors turn the rim and message `error-ink`. Event type is a two-up segmented choice that inverts to ink. The prepared message appears below a dashed rule, fading in from blur.

### Occasion chips
Outline pills (1.5px linen at 40%, 8px 16px) listing kinds of celebration; informational, not interactive.

## Do's and Don'ts

### Do:
- **Do** set every surface on the night ground (`night`) and bring warmth with radial glows (amber at 12–16%, leaf at 65%), not with lighter backgrounds.
- **Do** make every action an enamel plaque, red for calling or reserving, cream or ghost for everything else.
- **Do** present photographs as postcards (10px white border, deeper bottom, slight rotation) or as full-bleed scenes under a night gradient.
- **Do** put lists of prices on paper with dotted leaders and tabular numerals.
- **Do** give every movement a reduced-motion twin built from opacity, blur, glow or clip, and keep light-only motion (bulbs, hum, menu wipe) unchanged in both modes.
- **Do** restrict hover effects to `(hover: hover) and (pointer: fine)` and give every pressable a 0.95–0.97 press scale.

### Don't:
- **Don't** put the neon glow on paper or on Onest text; on paper the script is printed in `enamel-deep`.
- **Don't** use solid enamel red on night surfaces for anything that is not an action.
- **Don't** add a fourth typeface or set facts (prices, hours, phone, address) in script or display.
- **Don't** use stock food photography; only the restaurant's own photographs appear.
- **Don't** drop motion entirely under reduced motion, and don't keep parallax, slides, swings or pointer-follow in it.
- **Don't** give ground-level elements shadows or make objects glow; shadows are for objects, glow is for light sources.
