# kitchen.ag-renovations.co.uk

Google Ads landing page for complete kitchen renovations. Same theme as the bathroom page (forest greens,
mint, DM Sans) with its own layout, a brass accent and a kitchen-specific journey.

No build step: plain HTML and one CSS file. Edit, then push.

## What's in this repo

| Path | What it is |
|---|---|
| `index.html` | The page, including all scripts. The master copy: edit here only. |
| `css/kitchen.css` | All styles. If you change it, bump `css/kitchen.css?v=` in `index.html` in the same commit. |
| `images/optimized/` | Andrius's photo, the award photo, commercial client photos, accreditation marks (`marks/`). |
| `images/placeholders/` | Marked placeholder images. Delete once every placeholder is replaced. |
| `images/kitchen/`, `images/kitchen-testimonials/` | Created by the photo script for real kitchen photos. |
| `optimize_kitchen_photos.py` | Converts raw photos to WebP (1600px q82 + 800px q75, EXIF/GPS removed) and writes gallery tiles. |
| `make_staging.py` | Writes the staging copy next to this folder (tracking off, noindex, form sends nothing). |
| `CNAME`, `robots.txt` | Production only. |

## How the page works

- **Hero starter:** three tap options ("Where are you with your kitchen?"). A tap records the answer and jumps
  straight to step 2 of the enquiry form.
- **Enquiry form:** three steps (project stage, preferred start, contact details). It posts to the same Zapier
  hook as the bathroom page with `project_type=Kitchen Renovation` and
  `lead_source=Google Ads Kitchen Landing Page`. The stage and start answers are sent as `project_stage` and
  `start_timeline`, and also written at the top of `message`, so they reach the CRM even if the Zap only maps
  the original fields.
- **Conversion:** the Ads form conversion fires only on a confirmed 2xx from Zapier. On failure the visitor
  sees a "call us" message and nothing is counted.
- **Extra GA4 events** for funnel analysis: `form_step` (step 1 and 2 answers), `contract_toggle` (the
  comparison switch), `included_select` and `included_tour` (the kitchen tour), `gallery_open`, `cta_click`.
- **Extra GA4 event:** `extra_tap` (which addition was tapped).
- **Interactive pieces:** the trades comparison switches itself to the A&G view once when it scrolls into view;
  the kitchen drawing draws itself in once, then plays through the seven parts like stories (pausable, with
  arrows, and tap-to-advance on mobile); the process line fills as you scroll. All of it stays still for
  visitors who have reduced motion switched on.
- **What's included:** the kitchen drawing is original line art (no photo), so it works permanently.
- **The drawing line:** one fine line runs down the page margins and draws itself as the visitor scrolls (green on
  light sections, brass on dark ones), with small kitchen sketches blooming from it on wide screens. On phones it
  is a thin progress line down the left edge. It is built by a script from the section positions, so it adapts
  when sections change; give any new section an `id` and add it to the `sides` list in the thread script to choose
  which margin it runs down.
- **Popular additions:** its own section, with four illustrations that act out each addition once when seen
  (tap a card to replay) and a 3D kitchen that assembles itself beside the free design offer.
- **Hero:** the photo reveals itself in an arched frame on load, with the award seal and Kimberly's quote.

## Before the first launch

1. **No placeholders left.** In PowerShell: `(Select-String -Path index.html -Pattern "PLACEHOLDER").Count`
   must return `0`. The only placeholders left are the 6 gallery tiles.
2. **Confirmed with Andrius (Nov 2026):** kitchen fitters are in-house; the 10-15% matching-service line applies
   to kitchens; no response-time promise anywhere on the page; no standard duration in the timeline FAQ. The
   included scope and the four popular additions follow the October brand catalogue.
3. **Review figures checked live that day**: the page shows Google 5.0 from 60 and Trustpilot 4.7 from 48, in the
   hero proof row and the reviews section.
4. **Client photo permission** confirmed for Kimberly Dennis (hero photo and review card), Stevie Downard and
   Helen, E14.
5. **Hidden review card (Mindaugas K.)** stays hidden unless it's confirmed the reviewer is a client and not the
   former A&G coordinator. To show it, delete the word `hidden` on that `<article>` in the reviews section.
6. **Areas are area-level only** on gallery captions and alt text, never a street.
7. **Test the live form once before the kitchen campaign starts**, with "TEST" in the message, and confirm it
   reaches the CRM labelled as a kitchen enquiry.

## Reviews on the page

Review text is quoted word for word from Google. Where "…" appears, a passage was left out: staff names other than
Andrius, and Helen's mention of the platform she booked through. Keep to that rule when adding reviews.

## Adding photos and reviews

1. Create `photos-raw/` in this folder (git-ignored), one folder per project: `photos-raw/Project-01/` ...
   Review-card photos go in `photos-raw/testimonials/<client name>/`.
2. `pip install pillow` (plus `pillow-heif` for iPhone .heic), then `python optimize_kitchen_photos.py`.
3. Open `gallery-tiles.html`, replace `AREA`, and paste the tiles over the six PLACEHOLDER tiles in the
   gallery. Put the strongest project first: it becomes the large feature tile.
4. Hero: already set (`images/kitchen/hero/`). To change it, replace both files: a 1600x1200 landscape for
   phones and tablets and a 1200x1600 portrait crop for desktop.
5. Review cards: set `data-images` (full-size paths, comma separated) and `data-caption` on the photo button,
   the `img` src (low version), the quote, the name and the platform. Delete any card you can't fill; the
   first card is the large one.
6. Delete `images/placeholders/`.

## Every deploy (staging, then live)

1. Edit `index.html` (and `css/kitchen.css` if needed) in this folder.
2. `python make_staging.py`, then commit and push the staging repo. Review at
   `https://a-g-renovations-ltd.github.io/kitchen-landing-page-staging/` on desktop and phone.
3. In this folder: `git remote -v` must show `A-G-Renovations-Ltd/kitchen-landing-page`.
4. `git status`, then `git log --oneline -3` and note the top hash as your rollback point.
5. Checks before pushing: `hooks.zapier.com` appears exactly once; `AG_STAGING = false`; no `noindex`;
   `CNAME` reads `kitchen.ag-renovations.co.uk`; `robots.txt` says `Allow: /`; PLACEHOLDER count is 0 (for launch).
6. Commit, push, wait about 3 minutes, check in a private window.

## Domain safety

Do not verify `ag-renovations.co.uk` at organisation level while any A&G page lives outside the
A-G-Renovations-Ltd organisation: it takes those pages offline. Launch-day DNS is one new record only
(`kitchen` CNAME to `a-g-renovations-ltd.github.io`); no existing record changes.
