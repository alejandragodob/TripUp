# TripUp

Group travel, organised. Friends plan the trip, poll decisions, and settle expenses without leaving their group chat.

This repo holds the design challenge deliverables:

- **The app** (this folder): interactive prototype of the Lisbon scenario. React + Vite, mobile-optimised, mock data. Live at https://trip-up-three.vercel.app
- **`figma/`**: wireflow and hi-fi sources, the SVG generator, and `CRITIQUE.md` (the review of the brief).

## Run locally

```bash
npm install
npm run dev
```

Designed for iPhone 15 (393 × 852). On desktop it renders inside a phone frame; on a phone it fills the screen.

## The journey

| # | Screen | What happens |
|---|---|---|
| 01 | Home | Lisbon is the live trip. Tap it. |
| 02 | Trip group view | Members, tonight's open slot, today's plan, money. Tap **+** to add Ren. |
| 03 | Add Ren | Join link or contacts. "Joining tonight only" keeps her out of earlier splits. "See what Ren sees" opens her browser view. |
| 04 | Create poll | Three options drafted from the group's Google Maps wishlist. Remove or swap any. |
| 05 | Push + chat | The poll lands in the group chat as a live card. Vote from there. |
| 06 | Live poll | Votes arrive live (Theo votes after a few seconds, bars animate, cards re-sort). Close once a majority exists. |
| 07 | Plan updated | Winner is in tonight's itinerary, tagged "poll", with directions and booking. |
| 08 | Log expense | Receipt scanned into items. Wine split excludes Nic and Ren; tap names to change. |
| 09 | Balances | 7 debts simplified to 3 transfers, each explained. Tap one to settle. |
| 10 | Settled | Group-wide confirmation posted to the chat. |

Tabs (Trips / Polls / Plan / Money) work throughout.

## Structure

- `src/App.jsx` · screens and app state
- `src/ui.jsx` · shared components
- `src/styles.css` · design tokens (cream `#F7F3EC`, ink `#141414`, Newsreader + Figtree, Material Symbols Rounded)
- `src/data.js` · mock data
- `public/img/` · photos (Unsplash placeholders from the design file; swap before shipping)

## Deploy

Connected to Vercel; every push to `main` deploys. `vercel.json` carries the build settings.

## Non-goals

Real payments, Google auth and WhatsApp integration are mocked with convincing UI, per the brief.
