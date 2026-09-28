# TripUp. challenging the idea

What holds up, what's missing, and what I'd change before building the prototype.

## What the turn-5 design gets right

- **Lives next to WhatsApp instead of fighting it.** The chat-card twin for every event is the single best decision in the file. It directly answers "more than two taps and they switch to WhatsApp".
- **No accounts, no wallet.** Phone-number identity plus existing payment rails removes the two biggest reasons people abandon Splitwise-style apps.
- **Polls close on people, not timers.** Correct for a group of friends; a timer would create a deadline nobody asked for.
- **Explained transfers.** "Ren pays Maya instead of you" with a one-line why is a genuine improvement over Splitwise's opaque simplification.

## Gaps I think the brief and the design both miss

1. **Ari isn't the organizer, yet she does everything.** The brief's scenario is a participant driving the whole evening. That's the point (shared ownership), but neither the brief nor the design shows *any* moment where the organizer's role matters. Either drop the ORGANIZER tag entirely (cleaner) or give it one real job: the organizer is the default recipient of unclaimed debts and the one who can archive the trip. Right now it's decoration.

2. **The poll assumes everyone will vote. They won't.** Real groups leave one person who never opens the link. "Close when everyone has voted" plus a manual close is fine, but the close rule should have a *default fallback*: auto-close at the itinerary slot time (19:30) with the current leader. Otherwise Ari has to babysit the poll. The 19:30 slot already exists on screen 04; use it.

3. **Ties.** Three options and six voters means 2-2-2 or 3-3 is realistic. The design never shows a tie state. Cheapest answer: the creator breaks the tie on close; the button reads "Close poll · pick the winner" and shows the tied options.

4. **The receipt scan is doing a lot of quiet work.** "Food €166 / Wine €48" appearing pre-split is the most magical step in the flow and the least explained. If the scan misreads, the user has to edit line items on a mobile screen. Show the fallback: a plain "€214, split evenly" path that's one tap, with item-level splitting as an opt-in. Most groups split dinner evenly; the wine exclusion is the brief's edge case, not the norm.

5. **"Nic and Ren usually skip wine" is a privacy line.** Suggesting exclusions from habits is clever, but it means the app tells the group what individuals do or don't consume, inferred from past receipts. Some people will find that uncomfortable (alcohol, dietary, religious). Keep the suggestion but phrase it neutrally ("Same split as last time?") and never show the reason to other members.

6. **Settlement currency and rails are hand-waved.** Apple Pay person-to-person isn't available in most of Europe (Portugal included). Revolut and MB Way are what a Lisbon group actually uses. Since the scenario is Lisbon, the rail list should be MB Way / Revolut / bank transfer / cash. Small thing, but a PM in Lisbon would notice immediately.

7. **Ren, the guest, has a balance but no app.** She owes €28 and gets a push, but she joined via a browser link. Where does she pay from, and how does she get reminded a week later when the browser tab is gone? The design needs one more state: the guest's SMS nudge with a pay link. That's the same "no app needed" promise applied to money, and it's currently only applied to voting.

8. **Nothing happens mid-trip without Ari.** The brief stresses spontaneous, on-the-fly decisions. Screen 02's beige panel ("Dinner tonight is still open") is the only proactive moment, and it's triggered by an empty slot. There's an easy extra: at ~17:00 with no dinner in the plan, the app itself drops the draft poll into the chat, not just a nudge to Ari. That's the "value beyond the brief" reviewers ask for.

9. **The wireflow deliverable was missing.** Turn 5 has an app map (lo-fi, every lane) and hi-fi screens, but the brief's layer 1 is a *wireflow*: the scenario with decisions and state changes called out. The file in this folder (`wireflow.svg`) fills that gap: ten screens, red decision callouts, green state-change callouts.

## What I'd change in the hi-fi screens

- **Screen 06**: "Close poll · Ramiro wins" should be disabled until a majority exists (the spec says so; the screen doesn't show the disabled state). Add it as a variant.
- **Screen 02**: the money row says "You're owed €42" while screen 01's chip says the same and screen 09 says "+€188". The €42 is before tonight's dinner, so it's consistent, but the jump to €188 after one dinner surprises. Consider making tonight's dinner the whole difference on screen 09 ("+€146 from tonight").
- **Screen 08**: "Save · updates 6 balances" is good copy. Keep it.

## What I'd cut

- "Import from Splitwise" on Home. It's a nice acquisition hook, but it promises a migration feature the prototype can't demonstrate, and a reviewer will tap it. Either build a two-screen mock or remove it.
