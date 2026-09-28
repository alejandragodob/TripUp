# Handoff: TripUp — group-trip app (Lisbon scenario prototype)

## What's in this folder
- `README.md` — this spec. Self-sufficient: build from it alone.
- `BRIEF.md` — the original design challenge, verbatim in substance.
- `TripUp-design.standalone.html` — the full design document, single offline file. Open it in a browser. Newest work is at the TOP (turn 5). **Build from turn 5 (`#5a` screens, `#5w` app map).** Turns 1–4 are earlier explorations kept for history — ignore them.
- `src/TripUp.dc.html`, `src/ios-frame.jsx` — the source of the design document (HTML with inline styles). Useful for lifting exact values.

## About the design files
These HTML files are **design references**, not production code. The task is to recreate the turn-5 screens as a **working, mobile-optimised web prototype** (the primary deliverable in the brief) — React/Next/Vite or any framework you choose; mock data is fine, computations may be faked. The prototype must walk through the full Lisbon user journey below and the two key screens (02 Trip group view, 06 Live poll) must match the design pixel-close.

## Fidelity
- Turn 5 `#5a` (11 phone screens): **high-fidelity.** Recreate exactly: colors, type, spacing, radii, copy.
- Turn 5 `#5w` (app map): **low-fidelity** wireframes of every flow beyond the scenario. Use for structure and navigation only.

## Product concept (drives the UX decisions)
- TripUp does not fight WhatsApp; it lives next to it. Every poll / expense / balance is a **share-able live card** — votes can happen from the chat or push notification without opening the app.
- **Zero new accounts.** Identity = phone number (4-digit SMS code). Guests join via a link that opens in the browser; the app is optional. **No wallet:** money moves through Apple Pay / Revolut / Wise / bank transfer / cash. TripUp never holds funds.
- **Group wishlist (Google Maps).** Each trip has a shared pool of places fed by (1) members' connected Google Maps saved lists for that city, (2) Maps links pasted into the trip or group chat, (3) places already visited. Poll drafting ranks the wishlist (saved by more people › open now › walking distance › price spread) and only falls back to Places search when the wishlist is empty. Each option shows a source line ("Saved by Maya & Theo").
- **AI, quietly and always editable:** drafts the three poll options; reads a receipt into line items and suggests exclusions from habits ("Nic and Ren usually skip wine"); explains each simplified transfer in one sentence; writes the nudge; suggests fillers for empty itinerary slots. Never auto-applies.
- Polls have **no timer**. A poll closes when everyone has voted or when the creator closes it (allowed once a majority is reached).
- Organizer vs participant: identical powers; organizer only gets a small `ORGANIZER` tag.

## Reference device
iPhone 15 — 393 × 852 CSS px, portrait. Status bar 56 px safe area at top. Home indicator area at bottom. Design the web prototype at exactly this viewport (center it on desktop).

## Design tokens
Colors
- Background cream `#F7F3EC`
- Feature panel beige `#F1EBE2`
- Card white `#FFFFFF`, card shadow `0 2px 10px rgba(20,20,20,.04)` (hero cards `.05`)
- Hairline `#EAE3D8`, panel divider `#E0D8CB`
- Ink (text, primary button) `#141414`
- Muted text `#5C5750`; grey text / secondary title line `#8A837A`; disabled number `#C4BDB2`
- Accent gradient (leading poll bar, occasional italic word) `linear-gradient(90deg,#FF7A3D,#FF5CA8)`; leading-card border `#FF9AA8`; "LEADING" label `#E0562E`
- Success green `#2F7D5B`; WhatsApp green dot `#25D366`; link blue in chat mock `#1B7CF2`
- Pastel icon circles: peach `#FFE2C9` (icon `#E0562E`), mint `#DDEFE4` (icon `#2F7D5B`), periwinkle `#E3E9FF` (icon `#3B5BB5`), pink `#F9D9E6` (icon `#C2477A`)
- Avatar fills: A `#FFB48A`, N `#FFD9A8`, M `#BFE6D2`, T `#C9D8FF`, S `#F9C4DF`, R `#E8DDF5`; 2.5 px ring in the parent background color; stacked with −10 px overlap

Typography (Google Fonts)
- Display: **Newsreader** 400 (opsz auto). Titles 38/1.05 (two lines, second line `#8A837A`), 34 for secondary screens, 26–30 in cards, 24–28 for big numbers, 40 for the expense total.
- UI: **Figtree**. Section header 700 17; row title 700 15; row label 400 14; meta 400 13 `#8A837A`; small meta 400 12; caption 400/600 12; chip 700 13; button 700 15; tab label 11 (700 active, 500 inactive).
- Icons: **Material Symbols Rounded** (opsz 20–48, wght 400, FILL 1 for active). Tab icons 26 px; row/arrow icons 16–22 px.
- Wireframes only: Open Sans.

Spacing & shape
- Screen padding 20 px sides; vertical stack gap 12 px; top bar min-height 40.
- Cards radius 20; hero/panel radius 22; chat card 10–12; thumbnails 14; icon circle 46 (42 in poll options, 36 small).
- Row: white card, padding 12 × 14, `[icon circle 46] gap 12 [text] [black arrow circle 34]`.
- Primary button ("pill"): ink, radius 999, padding 14 × 22, white 28 px circle with `arrow_forward` at right, shadow `0 8px 18px rgba(20,20,20,.18)`. Full-width inside panels. On scrolling screens it is sticky at the bottom with a cream fade behind it.
- Outlined chip: 1.5 px ink border, radius 999, padding 8 × 14, optional 16 px leading icon; solid variant inverts.
- Tab bar: 82 px tall, cream, 1 px top hairline, four tabs `home / how_to_vote / calendar_month / account_balance_wallet` labelled Trips / Polls / Plan / Money.
- Poll progress bar: 5 px, track `#F1EBE2`, fill gradient (leading) or `#C4BDB2`.

## Screens (turn 5, `#5a`) — build all eleven, in this order
Cast: Ari (you), Nic (organizer), Maya, Theo, Sam; Ren joins tonight. Trip: Lisbon, Sep 24–28, day 4 of 4, Saturday 18:52. Currency €.

**01 Home.** Top: "Hi Ari" + bell button. Title "Your trips / one happening now". Beige hero card: group photo (92 px), "Lisbon" (Newsreader 28) + stacked avatars, "Sep 24 – 28 · Day 4 of 4 · 5 friends", soft chips "Tonight: dinner still open" · "You're owed €42", pill "Open trip". Section "Coming up": rows Primavera Sound, Barcelona (Jun 3 – 6, 2027 · 8 friends) and Dolomites hut-to-hut (Past · settled). Chips "New trip" / "Import from Splitwise". Tabs (Trips active). → tap Lisbon card → 02.

**02 Trip group view ★.** Back + bell. Title "Last night in / Lisbon". Group photo card (96 px) with dark bottom gradient: "Nic ORGANIZER · Ari · Maya · Theo · Sam" and avatars + dashed "+" (→ 03). Beige panel: "Dinner tonight is still open" / "Three places from the group's wishlist, ready to poll." / pill "Start the poll" (→ 04). Section "Today" (right label "Full plan"): 10:00 Torre de Belém; 14:00 LX Factory "€86 · logged by Maya"; Trip money "You're owed €42 / Settle with Apple Pay or Revolut" (→ 09). Tabs.

**03 Add Ren — Ari's side.** Bottom sheet over dimmed 02. Grab handle. Title "Add someone / to Lisbon". Row "Share the join link — Sends tripup.app/j/lisbon to your group chat". White card with three numbered steps: 1 They tap the link (opens in the browser — nothing to install); 2 They confirm their number (we text a 4-digit code, no password, no profile); 3 They're in (vote and pay from the chat right away). "or add from contacts". Selected row Ren Okafor "+351 ··· 42 18 · joining for dinner tonight" (check icon, ink border). Toggle "Joining tonight only — Skips the earlier expenses automatically" (on). Pill "Add Ren" → toast "Ren joined" and group becomes 6.

**03b Add Ren — Ren's side (mobile web).** Address bar "tripup.app/j/lisbon". Group photo with avatars. Title "Ari added you / to Lisbon". Copy: "Sep 24 – 28 · you're joining for dinner tonight. Confirm your number and you're in — no app, no password." Phone field "+351 912 ··· 42 18". Pill "Join as Ren". Caption "We text a 4-digit code. That's the whole sign-up." Section "What you can do from here": vote on tonight's dinner; pay your share with Apple Pay, Revolut or your bank; get the app later — optional.

**04 Create poll.** Back; right label "Draft · edit anything". Title "Where for / dinner?". Chip row (horizontal scroll): "Wishlist · 7" (solid, bookmark icon), "Near me", "Search Maps". Caption "From places your group saved in Google Maps — nearby, open now, a spread of price and vibe." Three option rows with 60 px photo, name, meta, source line with a small "G" badge: Cervejaria Ramiro (Seafood · €€ · 12 min walk · open till 00:30 — Saved by Maya & Theo); Taberna da Rua das Flores (Petiscos · €€ · 6 min walk · no bookings — Saved by Nic); Time Out Market (Food hall · € · 15 min · something for everyone — Pasted in chat by Sam). Each has an × to remove. Beige row "4 more on the wishlist — swap one in". Section "Settings": "Closes — when everyone has voted"; "Winner goes into tonight's plan — 19:30". Sticky pill "Send to the group" → 05/06.

**05 Push + group chat.** Chat mock (generic messaging look, doodle wallpaper `#E5DDD5` with faint radial-gradient dots). Push banner at top: TripUp · now — "Ari asks: Where for dinner? Ramiro · Taberna · Time Out — tap to vote". Chat header "Lisboa — Ari, Nic, Maya, Theo, Sam, Ren". System line "Ren joined the trip via Ari's link". Bubbles: Maya "ok back at the house, dinner?? I'm starving"; Theo "anything but a tourist trap pls". Outgoing green bubble containing the live poll card: header "TRIPUP · LIVE POLL / 4 of 6 voted", "Where for dinner?", "Tap to vote — no app needed", three compact option rows with 40 px photo and count (3 / 1 / 0, leading has gradient tint), button "Vote". Sam "voted, ramiro obviously". Input bar.

**06 Live poll ★.** Back + share. White header card: peach `restaurant` icon circle + "Where for dinner?" (Newsreader 26); "Tonight 19:30 · asked by Ari · **4 of 6 voted**"; chips "Share to chat" (chat icon) and "Nudge Theo & Ren" (notifications_active). Section "Options": three cards with 56 px photo, name, meta, big Newsreader count at right, progress bar with voter names ("You, Nic, Sam" / "Maya" / "—"). Leading card (Ramiro, 3, 62 %) has `#FF9AA8` border and "LEADING". Section "Group": avatar stack (Theo, Ren at 45 % opacity) + "4 voted · Theo and Ren haven't yet". Caption "Closes when everyone has voted, or when you close it." Sticky pill "Close poll · Ramiro wins" → 07. **Behavior:** votes arrive live (simulate: Theo votes Ramiro after ~4 s, counts and bar widths animate 300 ms ease-out, cards re-sort by count).

**07 Plan updated.** Title "Ramiro it is. / Added to tonight". White card: photo strip (72 px), "Cervejaria Ramiro — Won 4 of 6 · 19:30 · 12 min walk", 44 px map thumbnail, chips "Directions" (directions_walk) and "Book a table" (restaurant). Section "Today · Sat 27": 10:00 Torre de Belém; 14:00 LX Factory; 19:30 "Dinner · Cervejaria Ramiro — From tonight's poll · 6 going" with `poll` tag and ink border. Beige suggestion row: 44 px photo, "AFTER DINNER · SUGGESTION / Miradouro da Graça · 8 min / Saved by Sam", chip "Poll it". Tabs (Plan active).

**08 Log expense.** Back; right label "Receipt scanned". Title "Dinner at / Ramiro". White card: "TOTAL" / "€214.00" (Newsreader 40) / "Paid by you · 6 people" + 64×84 receipt/photo thumb. Section "Split by item": card "Food €166 — Everyone · €27.67 each"; ink-bordered card "Wine €48 — 4 people · €12 each" with person chips (Ari, Maya, Theo, Sam solid ink; Nic, Ren outlined + strikethrough) and note "Nic and Ren usually skip wine, so they're left out. Tap a name to change." (chips toggle). Sticky pill "Save · updates 6 balances" → 09.

**09 Balances.** Back + share. Title "Trip money / €1,284 total". Beige panel with three stats: €214 per person · €402 you paid · +€188 you're owed (green). Section "3 transfers instead of 7" with help icon (tap → explainer). Transfer rows `[from avatar] → [to avatar] Name pays you €96`: Nic → you €96; Theo → you €92; Ren → Maya €28 "Instead of paying you — one transfer fewer". Beige explainer: "Ren owes you €28 and you owe Maya €28, so Ren pays Maya directly. Nobody pays more than they owe." Chips "Nudge Nic & Theo" (notifications_active), "Paid in cash?". Caption "Friends pay you with Apple Pay, Revolut or a bank transfer — nothing to top up." Tabs (Money active). **Behavior:** tapping a transfer opens a settle sheet: Apple Pay / Revolut · Wise / Bank transfer (IBAN copied) / Paid in cash → marks row Paid; when all paid → 10.

**10 Settled.** Close button. Beige card: Lisbon photo (150 px), "Lisbon is / squared up.", "6 of 6 settled · €1,284 across 4 days", avatar stack of six. Section "Received": €96 from Nic (Apple Pay · just now) Paid; €92 from Theo (Revolut · 2 min ago) Paid; row "Posted to the group chat — “All settled — ready for the next one”". Sticky pill "Plan the next trip" → 01.

## App map (turn 5, `#5w`) — navigation beyond the scenario (lo-fi)
Lanes: ONBOARD (phone sign-in; optional Google Maps connect) · TRIPS (home; new trip; invite; join via link) · TRIP HUB (trip view; plan/itinerary by day; wishlist with sources) · DECIDE (new poll for any decision — eat/stay/do/custom, options from wishlist/near me/search/typed; live poll; result → plan) · PAY (add expense with receipt scan and item exclusions; balances; settle; confirmation) · ALWAYS ON (push + chat-card twin for every event; Polls tab badge). Implement the four tabs and enough of these to make navigation feel complete; stubs are fine.

## State (mock, in memory or localStorage)
- `trip`: name, dates, city, members[] {id, name, initial, color, organizer, joinedFor}, itinerary[] {day, time, title, meta, source}, wishlist[] {place, savedBy[], source}
- `poll`: question, options[] {place, photo, meta, source, votes[]}, status (draft|live|closed), winnerId
- `expenses[]`: {title, total, paidBy, items[] {label, amount, participants[]}}
- `balances`: derived — per-person share, paid, net; `transfers[]` simplified with `why` text; `paid` flags
- `ui`: current screen, sheet open, toast

## Interactions & motion
- Screen transitions: horizontal push 260 ms `cubic-bezier(.2,.8,.2,1)`; sheets slide up 320 ms with dim `rgba(0,0,0,.35)`.
- Buttons: pressed scale .98; arrow circle nudges 2 px right on hover.
- Poll bars: width transition 300 ms; count number cross-fades.
- Toasts: bottom, ink pill, 1.8 s.
- All hit targets ≥ 44 px.

## Assets
- Photos are Unsplash placeholders (URLs in the source) — replace with real ones. Group photo, three restaurants, Lisbon, Miradouro, a map thumbnail.
- Icons: Material Symbols Rounded via Google Fonts. Avatars are initials on pastel fills. The Google badge is a plain "G" in a white circle, not the logo.

## Non-goals
Real payments, real Google auth, real WhatsApp integration — mock all three with convincing UI and copy.
