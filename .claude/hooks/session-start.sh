#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

mkdir -p "$HOME/.claude"

cat > "$HOME/.claude/CLAUDE.md" << 'CLAUDE_MD_EOF'
# JWI — Claude Operating System

Always give me the next concrete action I can take today. Never tell me to interview people, survey, or do market research — I learn by shipping, not talking.

## Who I Am
I am JWI. I am a creative marketing agency, helping clients improve marketing and creative outcomes.

## Operating Rules
- Give me a direct recommendation, not a list of options
- Keep responses tight — I'll ask for more if I need it
- Don't add features or sections I didn't ask for
- When something is ambiguous, make a reasonable assumption and flag it
- Verify before calling anything done
- Prioritize practical agency impact and visually strong execution
- Do not make any changes until you have 95% confidence in what you need to build. Ask follow-up questions one at a time until you reach that confidence level.
- Be concise. No filler, no preamble, no flattery — straight to the point, fewer words. When I ask a question, answer it directly first, then add detail only if needed.

## Never
- Never use em dashes
- Never add fluff or generic filler

## When to Read Each File

All four live in `~/.claude/`. Read the relevant one before acting, don't guess when a real answer is one file away.

Read `~/.claude/soul.md` when:
- Writing anything personal, biographical, or that requires my perspective
- Telling my story, referencing my background, or making a values-based judgment call

Read `~/.claude/voice.md` when:
- Writing any copy, caption, post, script, email, or DM in my name
- Unsure whether a word, phrase, or tone sounds like me

Read `~/.claude/design.md` when:
- Generating any visual output: carousels, graphics, slides, infographics, UI
- Choosing colors, fonts, or layout for anything

Read `~/.claude/audience.md` when:
- Writing content for my audience, not just about a topic
- Crafting CTAs, pitch copy, or anything meant to convert
- Unsure what language or framing will land with my people

## Applied Learning

When something fails repeatedly, when I have to re-explain something, or when a workaround is found for a tool limitation, add a one-line bullet here. Keep each bullet under 15 words, no explanations. Only add things that will save time in future sessions.

## Captured Preferences

Whenever I give feedback on something you built or wrote — a correction, a redo, or telling you a version worked — add a dated entry here immediately, without being asked. Never let feedback disappear at the end of a session.

Each entry: what I told you to fix, what I liked, what I didn't like. Tight, no fluff, no restating the task. The point is that you never make the same mistake twice.
CLAUDE_MD_EOF

cat > "$HOME/.claude/soul.md" << 'SOUL_MD_EOF'
# JWI Soul

## Origin Story
JWI is an independent creative advertising agency based in Dubai. Founded in 2015, we exist to help ambitious brands grow across the Middle East without compromising on global standards.

We were built for a region that is dynamic, influential and increasingly complex. Brands here face higher creative expectations, more cultural nuance and greater commercial pressure. Our answer is advertising rooted in regional intelligence, held to global standards and guided by commercial thinking.

## Beliefs
- The most effective advertising is rooted in regional intelligence, held to global standards and guided by commercial thinking.
- Creativity is a long-term investment in business growth, not a short-term output.
- Local relevance is not achieved through assumption. It comes from lived regional understanding.
- Distinctive ideas must also be durable: able to grow with the brand and the business.
- Great work is persuasive and accountable.
- Strong partnerships require trust, accountability, continuity and senior involvement.

## Philosophy
We operate at the intersection of creative intelligence, cultural integrity and commercial impact.

Creative intelligence means turning insight into effective creative responses: clear, usable answers, platforms and campaigns shaped around real consumer and cultural challenges.

Cultural integrity means building teams that last. Our clients work with invested, senior-led partners who stay embedded with their brands, rather than rotating teams.

Commercial impact means thinking beyond the brief and beyond the moment. We make creative decisions that compound: strengthening brand equity and driving measurable growth over time.

We do not force a service. We build the right strategic and creative response around the challenge.

## Defining Moments
- Founded in Dubai in 2015 as an independent creative advertising agency.
- More than a decade embedded in the GCC, building a perspective grounded in lived regional understanding.
- Chose long-term strategic partnership over project-by-project delivery.
- Chose sustained business growth over the industry's pursuit of quick wins.
- Built work for global brands expanding across the Middle East, regional organisations strengthening their position and ambitious businesses creating stronger, more consistent brands.

## The Line We Come Back To
We built this because we were sick of creative work that chases quick wins instead of creating sustained business growth.
SOUL_MD_EOF

cat > "$HOME/.claude/voice.md" << 'VOICE_MD_EOF'
# JWI Voice

Built from JWI's own LinkedIn posts. Rules below are extracted from that text, not assumed.

## Tone
1. **Direct** — say the thing plainly. No throat-clearing before the point.
2. **Confident** — declarative sentences. State beliefs as facts ("We believe X" is followed by a flat claim, not a hedge).
3. **Precise** — specific vocabulary over vague filler. "Cultural Integrity," not "good vibes." "Strategic toolkit," not "campaign stuff."
4. **Proof-driven** — every abstract claim gets anchored to something real within a line or two: a named client, a number, a person, a project. Claims don't float unsupported.
5. **Restrained** — emphasis comes from line breaks, short fragments and structure, never from exclamation points or stacked adjectives.

## Word Rules

**Always**
- Plain, concrete nouns: brands, culture, people, platforms, work
- Active voice, subject-verb-object
- Specific numbers over vague quantities ("35 marketing leaders," not "dozens of leaders")
- Named proof over generic claims (a client, a campaign, a person's title and name)
- Contractions are fine and used often: don't, isn't, we're

**Never**
- Generic agency jargon: synergy, leverage (as a verb), disrupt / disruptive, solutions (as filler), passionate, innovative, cutting-edge, best-in-class, world-class, unlock, journey (as metaphor), ecosystem, holistic
- Em dashes. For an aside or definition, use a spaced hyphen instead ("Cultural Integrity - one of our guiding principles")
- Exclamation points
- Emoji in copy
- Hedging qualifiers: very, really, quite, just, kind of, sort of, we hope

## Sentence Structure
- Most sentences run short: 5 to 15 words. One longer, detail-loaded sentence is allowed per post to carry the concrete proof point (project name, channels, mechanics).
- Fragments are allowed and expected for rhythm. They don't need a verb: "One idea. Built to scale." "Stay tuned."
- Signature device: state what something is **not**, then what it **is**. Often split across two short lines.
  - "Not because people know them. / Because people trust them, generation after generation."
  - "Not to find all the answers, but to share experiences, challenge perspectives..."
- One thought per paragraph. Line breaks do the pacing work a comma would do elsewhere, use them generously.

## Post Anatomy (LinkedIn)
Every post follows the same three-beat shape.

1. **Open** — one short declarative line, the thesis. Often the not/because contrast above.
2. **Develop and prove** — one to three short paragraphs that build the idea and land it on something specific and real: a client name, an event, a quote from Charli, a mechanic.
3. **Close** — one of two moves, never both:
   - A plain, logistical pointer: "Link in comments." "Full article in comments." "Stay tuned."
   - A one-line takeaway that reframes the whole post as a lesson: "A good reminder that the strongest brand platforms are the ones that stay consistent as they scale."

**Hashtags** — optional, not every post has them. When used: 2 to 4, lowercase, industry/topic terms (#brandstrategy, #creativeagency), never a branded tagline or a hype phrase.

**Voice** — company posts speak as "we" / "our." Charli is referenced in third person even on her own agency's account: "our CEO, Charli Wright, shares why..."

## Platform Rules

**Social (LinkedIn, Instagram, and other channels)**
One voice, same copy across every social channel, no separate Instagram-shortened rewrite. Use the Post Anatomy above as-is regardless of platform.

**Website / brand copy**
Full sentences, all-caps headline treatment for statement moments, the parenthesis pull-quote for beliefs. CTAs are plain instructions ("Get in touch"), never pitch lines.

**Email / DM outreach**
No "Hope this finds you well." Open with the point. Close with a direct ask.

**Scripts (video / ads)**
Built for the ear. One beat per line. No adjective stacking.

## Reference Lines
"Strong platforms don't scale because they're everywhere. They scale because they stay one idea."

"Senior people don't rotate off an account. They grow with it."
VOICE_MD_EOF

cat > "$HOME/.claude/design.md" << 'DESIGN_MD_EOF'
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
DESIGN_MD_EOF

cat > "$HOME/.claude/audience.md" << 'AUDIENCE_MD_EOF'
# JWI Audience

Sources: JWI's own site content (via search index, direct fetch was blocked in this session), a named 2024 client-agency relationship survey, and industry publications. Reddit's crawler blocks this tool outright, so nothing here is a scraped Reddit quote, every line is sourced and linked below. Treat this as a working draft, not a finished persona, until it's checked against real client conversations.

## Who We're Reaching
Marketing and brand leaders (CMOs, marketing directors, brand managers) inside multinational and regional consumer brands operating in the Middle East and GCC. Not startups, not SMBs. Named global and regional brands like: Patron, Grey Goose, Bacardi, Gillette, Spotify, Air Arabia, Braun, Epson, Colgate, Vicks, Bombay Sapphire. These are people managing a global brand's consistency while needing the work to actually land in a regional market they answer for.

## The Problem We Solve
Global campaigns get built for "the world" and then don't land locally, or local execution drifts from what head office signed off on. JWI's own positioning names this directly: built to stand for creativity that is "culturally informed, commercially accountable and consistently high quality," helping brands "create local impact without compromising global standards." The second half of the problem is continuity: clients get sold by senior staff and then handed off to whoever's free. JWI's answer is staying senior-led instead of rotating the account team.

## What We Offer
Marketing strategy and consultancy, creative advertising, experiential and events, content and social. Pricing isn't public, engagements are project or retainer-based and not something to guess at here, confirm actual numbers before quoting them anywhere.

## Where They Hang Out
LinkedIn, primarily. This is a B2B audience, they're not scrolling Reddit or forums for this decision, they're reading LinkedIn.

## Real Language

**Pain points**
- "They don't understand our business" is the recurring line in agency-client research. The specific industry changes (spirits vs. tech vs. FMCG) but the sentence doesn't. ([source](https://brandauditors.com/blog/marketing-doesnt-work/))
- Global campaigns are "designed for 'The World' rather than the technical and cultural algorithms of a local market," and local teams end up quietly rebuilding half of it after launch. ([source](https://dominasiserp.com/en/fail/))
- Agencies use junior staff as their margin lever: "you don't get the person who pitched you, you get a junior managing 12 accounts." Every account manager change costs roughly 6 to 8 weeks of lost context while the new person learns the business. ([source](https://www.slaymakermarketing.com/post/why-changing-your-account-manager-and-what-it-costs-you))
- 40% of clients surveyed said they'll switch agency partners within six months, and clients name delivery and value as the reason relationships end, while agencies tend to blame budgets instead. That gap between what clients say and what agencies think is happening is itself a real finding. ([source](https://setup.us/blog/the-truth-about-agency-breakups-what-clients-and-agencies-really-think))

**Fears**
- Creative quality is the top reason marketers pass on a new agency, cited by 55% of respondents in North America. Getting the creative wrong isn't a small miss, it's disqualifying. ([source](https://www.emarketer.com))
- Over half of brands are pulling work in-house: 32% expect to handle nearly all creative internally within a year, another 23% plan to bring at least half in-house. The fear isn't abstract, "do we need an agency at all" is a live question inside these companies right now. ([source](https://setup.us/blog/the-truth-about-agency-breakups-what-clients-and-agencies-really-think))

**Dreams / goals**
- Clients want fewer agency partners with deeper, more complete capability, bringing "product, packaging, retail, digital and content design into one ecosystem" rather than a pile of disconnected vendors. This is exactly what "integrated campaigns" in JWI's own offer answers. ([source](https://setup.us/blog/the-truth-about-agency-breakups-what-clients-and-agencies-really-think))
- Underneath the churn and in-house pressure is one plain want: a partner who already understands the market well enough that the client stops having to explain it every meeting.

## Phrases Worth Echoing
"Doesn't understand our market/business" (the complaint to position against). "Local impact without compromising global standards" (JWI's own line, already proven). "Senior team," "in-house" (the alternative clients are actively weighing).

## Open Gaps
- Pricing and engagement structure aren't confirmed, get real numbers before this goes near a pitch deck.
- No direct client quotes yet, everything here is industry-pattern language, not a JWI client's actual words. Worth pulling 2 to 3 real quotes from account leads next time you're on a client call.
AUDIENCE_MD_EOF
