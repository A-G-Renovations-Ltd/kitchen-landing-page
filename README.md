# kitchen.ag-renovations.co.uk

Google Ads landing page for complete kitchen renovations. Built from the live bathroom page
(`landingpage-ag`, September rebuild): same layout, styles, scripts, form and tracking, rewritten for kitchens.

## What's in this repo

| Path | What it is |
|---|---|
| `index.html` | The page. This is the master copy: edit here only. |
| `src/input.css` → `dist/output.css` | Tailwind v4 build (`npm install` once, then `npm run build`). `dist/output.css` is committed so GitHub Pages can serve it. |
| `images/optimized/` | Shared brand assets copied from the bathroom repo: accreditation logos, award certificate, Andrius's photo, client logos. |
| `images/placeholders/` | Marked placeholder images. Delete this folder once every placeholder is replaced. |
| `images/kitchen/`, `images/kitchen-testimonials/` | Where the optimised kitchen photos go (written by the photo script). |
| `optimize_kitchen_photos.py` | Converts raw photos to WebP (1600px q82 + 800px q75, EXIF/GPS removed) and writes gallery tiles. |
| `make_staging.py` | Writes the staging copy (tracking off, noindex, form sends nothing). |
| `CNAME`, `robots.txt` | Production only. Never copy the staging `robots.txt` here. |

Form: posts to the same Zapier hook as the bathroom page with `project_type=Kitchen Renovation` and
`lead_source=Google Ads Kitchen Landing Page`. The Ads conversion fires only on a confirmed 2xx from Zapier.

## Before the first launch

1. **No placeholders left.** In PowerShell: `(Select-String -Path index.html -Pattern "PLACEHOLDER").Count` must return `0`.
   Placeholders are in the hero photo and thumbnail, the 9 gallery tiles, the 5 review cards and the process photo.
2. **Andrius has signed off** the kitchen-specific claims:
   - Kitchen fitters are employed by A&G (Why A&G card 01 and the subcontractor FAQ).
   - "Around 3 to 5 weeks on site" (timeline FAQ).
   - "Direct quotes typically 10-15% lower than through a matching service" also holds for kitchens (card 04, mid-page CTA, FAQ).
   - The What's Included scope list and the Popular Upgrades list.
   - "We seek trade discounts wherever possible" (supply FAQ).
3. **Review figures checked live that day**: Google 5.0 from 51 (hero, ratings box, final CTA) and Trustpilot 4.7 from 41 (ratings box).
4. **Every review card** is a real kitchen review, word for word, with the client's permission to use their photos.
5. **Areas are area-level only** (e.g. "Fulham"), never a street, on gallery tiles and alt text. Once you have them,
   add a few recent kitchen areas to the "What areas of London do you cover?" FAQ in both the visible FAQ and the FAQPage schema.
6. **Test the live form once before the kitchen campaign starts**: submit one enquiry with "TEST" in the message and confirm it arrives
   through Zapier with `project_type` = Kitchen Renovation. Doing it before any ad points at the page means no ad click is attached,
   so it isn't counted as an Ads conversion.

## Adding photos and reviews

1. Create `photos-raw/` in the repo root (it is git-ignored). One folder per project: `photos-raw/Project-01/`, `photos-raw/Project-02/` ...
   Review-card photos go in `photos-raw/testimonials/<client name>/`.
2. `pip install pillow` (and `pip install pillow-heif` if any photos are iPhone .heic), then `python optimize_kitchen_photos.py`.
3. Open `gallery-tiles.html`, replace `AREA` in each tile, and paste the tiles over the PLACEHOLDER tiles in the gallery grid in `index.html`.
4. Hero: point the hero `<img>` at a landscape photo in `images/kitchen/full/` and write a factual alt. Do the same for the small hero
   thumbnail (use the `low/` version) and the process photo and its caption.
5. Review cards: set `data-client`, `data-images` (full-size paths, comma-separated), the `img` src (low version), the quote, the name and
   the platform. Add `<div class="tsm-count">1 / N</div>` under the image when a card has more than one photo, as on the bathroom page.
   Delete any card you can't fill.
6. Delete `images/placeholders/`.

## GitHub setup

1. Signed in as the marketing@ag-renovations.co.uk account, create a **free organisation** (e.g. `ag-renovations`) and add your
   personal account and Andrius's as owners. The company then owns the repos rather than a personal account.
2. Create two **public** repos in it (free-plan Pages only serves public repos; a private one 404s silently):
   `kitchen-landing-page` (this folder) and `kitchen-landing-page-staging` (the folder `make_staging.py` writes).
3. In each repo: Settings > Pages > Deploy from a branch > `main` / root.
4. Verify the domain once for the organisation: organisation Settings > Pages > add `ag-renovations.co.uk` and add the TXT record GitHub
   gives you at one.com. This prevents the "domain already taken" error you hit on the bathroom page.
5. At one.com add a CNAME record: host `kitchen`, value `<organisation-name>.github.io`. This does not touch the MX/email records.
6. In the production repo: Settings > Pages > Custom domain `kitchen.ag-renovations.co.uk`, then tick **Enforce HTTPS** once the
   certificate is issued.

**Moving the bathroom repo into the organisation** (repo Settings > General > Danger Zone > Transfer ownership): after the transfer,
change the one.com CNAME for `bathroom` from the old `<account>.github.io` to `<organisation-name>.github.io`, then re-check the
custom domain and Enforce HTTPS in the repo's Pages settings. Do it at a quiet time and check the page in a private window straight after,
because the bathroom ads keep sending traffic while the DNS change propagates.

## Every deploy (staging, then live)

1. Edit `index.html` in this repo. Run `npm run build`; if any CSS changed, bump `dist/output.css?v=` in the same commit.
2. `python make_staging.py`, then commit and push the staging repo. Review at
   `https://<organisation-name>.github.io/kitchen-landing-page-staging/` on desktop and phone.
3. Back in this repo: `git remote -v` must show `<organisation-name>/kitchen-landing-page`.
4. `git status`, then `git log --oneline -3` and note the top hash as your rollback point.
5. Checks before pushing:
   - `hooks.zapier.com` appears exactly once
   - `AG_STAGING = false`
   - no `noindex` anywhere in `index.html`
   - `CNAME` reads `kitchen.ag-renovations.co.uk`; `robots.txt` says `Allow: /`
   - PLACEHOLDER count is 0
6. Commit, push, wait about 3 minutes, check in a private window.

## Optional

- **Separate Ads conversion action.** The form uses the bathroom page's form conversion for now. To report kitchen leads under their own
  action (useful if you later give kitchen leads a higher value), create a new conversion action in Google Ads and paste its `send_to`
  value into `AG_ADS_FORM_CONVERSION` near the bottom of `index.html`.
- **Clarity.** Uses the same Clarity project as the bathroom page (filter recordings by URL). To keep them apart, create a kitchen project
  under marketing@ and swap the ID in the Clarity block in `<head>`.
- **Zap.** Check the Zap's later steps use `project_type` and `lead_source` from the hook, not a fixed "Bathroom" value, so kitchen leads
  arrive labelled.
