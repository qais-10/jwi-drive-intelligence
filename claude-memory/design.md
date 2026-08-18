# JWI Design

## Brand Colors
- `#141414` Black — primary text, dark backgrounds, high-contrast anchor
- `#FBFBFB` White — primary background, negative space, reversed text
- `#EFEEEA` Beige — secondary background, section breaks, warmth against black/white

Usage rule: black and white carry the contrast. Beige is the resting tone, never the loudest one on the page. No tints, no gradients, no colors outside this set unless a client's brand requires it.

## Typography

### Display Font — Miller Display, Light
File: `~/.claude/fonts/MillerDisplay-Light.ttf`
Use for: headlines, pull quotes, cover slides, hero statements. Anything meant to be felt before it's read.
Fallback stack: `"Miller Display", Georgia, "Times New Roman", serif`
Rule: display weight only. Never bold it for emphasis, size and spacing carry the weight instead.

### Body Font — Maison Neue
Files: `~/.claude/fonts/MaisonNeue-Book.ttf`, `~/.claude/fonts/MaisonNeue-Light.ttf`, `~/.claude/fonts/MaisonNeue-Medium.ttf`
Use for: body copy, captions, UI text, decks, documents.
- Book: default reading weight, use for paragraphs and anywhere legibility matters most
- Light: secondary text, captions, metadata, anywhere the copy should sit quieter than the main read
- Medium: emphasis within body copy, labels, buttons, small headers that need weight without switching to Miller
Fallback stack: `"Maison Neue", -apple-system, "Helvetica Neue", Arial, sans-serif`

### Pairing Logic
Miller Display is the voice. Maison Neue is the ear. Serif display against a clean grotesque body gives JWI's work an editorial, agency-grade feel rather than a startup-sans look. Never substitute a different serif for Miller or a different grotesque for Maison Neue, the pairing is the signature.

## Visual Aesthetic
Editorial, premium, restrained.

In practice:
- Sparse layout, generous whitespace, nothing crowded
- Large, confident type doing the heavy lifting
- Limited palette, the three brand colors only
- Imagery that feels art-directed, not decorative or stock
- Copy kept concise and structured, hierarchy and composition carry meaning instead of visual noise

The target feel: a high-end regional agency with global discipline. If a layout needs an extra color, effect, or decorative element to feel finished, the composition is wrong, fix the hierarchy first.

## Hierarchy Rules
1. Headline: Miller Display Light, largest size on the page, generous line height
2. Subhead / lead-in: Maison Neue Book, mid-size, tight to the headline
3. Body: Maison Neue Book
4. Caption / metadata: Maison Neue Light, smallest size, lowest visual weight

## What to Avoid
- No em dashes in any typeset copy
- No drop shadows, no gradients, no decorative color outside the three brand hex codes
- No competing display fonts on the same layout

## Reference: jwi-global.com Patterns
Confirmed from the live site, treat these as the applied version of the rules above.

**Nav** — three-part flex: `CONTACT` left, `JWI` wordmark centered, `MENU` right. All caps, letter-spaced, small size, Miller Display. Sits on a solid black bar at the top of the page.

**Hero** — full black ground, headline in beige (not pure white), Miller Display Light, all caps, two lines max, centered, tight leading. Statement-first, no supporting copy in the hero itself.

**Headline convention** — section and hero headlines are set in all caps, centered, and capped at two to three lines. This is a house rule, not a one-off: any new headline should default to this treatment unless there's a specific reason to break it.

**Pull-quote motif** — a short, centered statement wrapped in oversized parenthesis characters as the sole decorative device. No boxes, no rules, no icons around quoted copy. Used on beige/white ground under a headline.

**Standard section (three-column)** — black ground, three columns: a labeled headline (Miller Display), a small sans-serif eyebrow label ("How We Think" / "How We Partner" / "The Outcomes We Create"), and a short sans-serif paragraph. One column pairs with art-directed photography, cropped and stacked, not decorative.

**Client grid** — logos rendered strictly in black (grayscale, no brand colors retained), evenly gridded, separated by thin black hairlines, generous cell padding. Proof of range without visual noise.

**Alignment rule (updated)** — headlines and pull-quote statements are centered by default, that's the house voice. Long-form running copy (multi-paragraph body text, documents, decks) stays left-aligned for readability. Center for moments, left-align for reading.

**Resolved: pull-quote font** — only one Miller cut was delivered (Display, Light), no separate Miller Text file exists in the asset set. Decision: pull-quote statements use Miller Display Light at a reduced size (roughly half the hero headline size), not Maison Neue. This matches the serif look on the live site without requiring a font that isn't in hand. If a true Miller Text cut is licensed later, swap it in for quotes and keep Miller Display Light for headlines only.
