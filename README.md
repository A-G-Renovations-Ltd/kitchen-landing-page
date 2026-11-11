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
  weaves inside the page's edge padding and sweeps across between sections, never under text. It is built by a script from the section positions, so it adapts
  when sections change; give any new section an `id` and add it to the `sides` list in the thread script to choose
  which margin it runs down.
- **Popular additions:** its own section, with four illustrations that act out each addition once when seen
  (tap a card to replay) and a 3D kitchen that assembles itself beside the free design offer.
- **Hero:** the photo reveals itself in an arched frame on load, with the award seal and Kimberly's quote.

## Before the first launch

1. **Placeholders:** none left. `(Select-String -Path index.html -Pattern "PLACEHOLDER").Count` returns `0`.
2. **Confirmed with Andrius (Nov 2026):** kitchen fitters are in-house; the 10-15% matching-service line applies
   to kitchens; no response-time promise anywhere; no standard duration in the timeline FAQ. The included scope
   and the four popular additions follow the October brand catalogue. Homes are the main market.
3. **Review figures checked live that day**: Google 5.0 from 60 and Trustpilot 4.7 from 48 (hero trust row and
   reviews section).
4. **Photo rights and permission:** the reviewers (Kimberly Dennis, Stevie Downard, Helen) have agreed to their
   photos being used; A&G has the right to use the professionally shot Ealing, Islington and FAQ photos (the FAQ
   photo has a `CONFIRM` comment in the code).
5. **Hidden review card (Mindaugas K.)** stays hidden unless it's confirmed the reviewer is a client and not the
   former A&G coordinator. To show it, delete the word `hidden` on that `<article>`.
6. **Review links:** each review currently opens the Google reviews list; swap in each review's own share link
   under its `REVIEW LINK` comment if you want them to open the exact review.
7. **Partner statuses current:** Magnet Approved Installer, B&Q Approved Installer, Howdens and Kutchenhaus supply
   partners and Easy Bathrooms Simply Install, all taken from the October 2026 catalogue.
8. **Cookie consent:** the page loads Google Tag Manager, Google Analytics, Google Ads and Clarity with no consent
   banner (the bathroom page is the same). Decide with Andrius whether to add one with Google Consent Mode.
9. **Test the live form once before the kitchen campaign starts**, with "TEST" in the message, and confirm it
   reaches the CRM labelled as a kitchen enquiry.

## Reviews on the page

Review text is quoted word for word from Google. Where "…" appears, a passage was left out: staff names other than
Andrius, and Helen's mention of the platform she booked through. Keep to that rule when adding reviews.

Tapping a review's text opens it on Google; tapping its photos opens the photo viewer. Every review link currently
opens the Google reviews list. To send each one to its exact review: on Google Maps, open the review, tap Share,
copy the link, and paste it into the `href` under the matching `REVIEW LINK` comment in `index.html` (the hero quote
card and each review card have one).

## Booking links

Every "Book a free site visit" button, the header button, the mobile booking bar and the hero options all go to
`#book`, the form card itself, so on phones visitors land on the form rather than the intro text above it.

## Sharing and browser tab

`favicon-32.png` and `apple-touch-icon.png` give the page its tab and home-screen icon (the crest).
`images/og-image.jpg` (1200 x 630) is the preview image shown when the link is shared on WhatsApp, LinkedIn, etc.

## Adding kitchen projects

The gallery shows one tile per project, as on the bathroom page: the cover photo, the project name, a short line
and the photo count. Tapping a tile opens that project's photos only. Current projects, in gallery order: Ealing (7 photos), Kensal (9),
Islington (2), Croydon (6), Little Venice (5) and a grey herringbone kitchen (2; area unknown, so it is titled by
style). Areas only, never streets or postcodes. The Installation step in "How your kitchen comes together" also shows an
on-site photo of one of our fitters (`images/kitchens/on-site/`), which opens full size when tapped.

Photos are served as AVIF (about half the size of JPEG at the same visible quality) with WebP as the fallback,
each at 480, 800, 1200 and 1600px wide. Browsers download only the size the screen needs, and a tiny blurred
preview shows instantly while the sharp photo loads. All metadata, including GPS, is removed. Pick 5 to 9 photos
per project with no near-duplicates, so the site stays light.

1. Put the chosen photos in `photos-raw/<area>/` (git-ignored), e.g. `photos-raw/fulham/`, renamed so the cover
   photo sorts first. iPhone RAW (.DNG) is fine.
2. `pip install pillow rawpy pillow-heif`, then `python optimize_kitchen_photos.py fulham "Kitchen in Fulham"`.
3. Paste the generated `project-fulham.html` inside `<div class="ptiles">` in the gallery, write the cover alt text
   and the short line, then deploy as usual.

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
