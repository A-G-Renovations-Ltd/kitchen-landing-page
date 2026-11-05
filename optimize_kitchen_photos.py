"""
Optimise kitchen photos for the landing page.

Put the original photos in photos-raw/ (ignored by git), one folder per project:

    photos-raw/Project-01/   any .jpg .jpeg .png .webp (.heic needs: pip install pillow-heif)
    photos-raw/Project-02/
    photos-raw/testimonials/<client-name>/   photos for a client review card

Run from the repo root:   python optimize_kitchen_photos.py

Output (same settings as the bathroom page: full 1600px WebP q82, low 800px WebP q75,
EXIF and GPS removed, phone rotation applied first):

    images/kitchen/full/Project-01-image-01.webp     images/kitchen/low/...
    images/kitchen-testimonials/full/<client>-01.webp   .../low/...

It also writes gallery-tiles.html: one ready gallery tile per project folder, to paste into
the gallery grid in index.html (replacing the PLACEHOLDER tiles). The first six get the layout
classes the grid expects (feature, tall, two small, two wide). Replace AREA in each tile.
"""
import os
import re
from PIL import Image, ImageOps

try:
    import pillow_heif  # optional, for iPhone .heic files
    pillow_heif.register_heif_opener()
except ImportError:
    pass

RAW = 'photos-raw'
EXT = ('.jpg', '.jpeg', '.png', '.webp', '.heic')


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def save(src, dst, max_px, quality):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)  # apply rotation, then drop all metadata
        im = im.convert('RGB')
        im.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
        im.save(dst, 'WEBP', quality=quality, method=6)  # no exif passed, so none is written


def process(folder, out_dir, prefix):
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(EXT))
    made = []
    for i, f in enumerate(files, 1):
        name = f'{prefix}-{i:02d}.webp'
        for sub, px, q in (('full', 1600, 82), ('low', 800, 75)):
            os.makedirs(f'{out_dir}/{sub}', exist_ok=True)
            save(os.path.join(folder, f), f'{out_dir}/{sub}/{name}', px, q)
        made.append(name)
        print(f'  {f} -> {out_dir}/full/{name}')
    return made


def main():
    if not os.path.isdir(RAW):
        raise SystemExit(f'No {RAW}/ folder found. Create it and add one folder per project.')
    tiles = []
    for d in sorted(os.listdir(RAW)):
        path = os.path.join(RAW, d)
        if not os.path.isdir(path):
            continue
        if d.lower() == 'testimonials':
            for c in sorted(os.listdir(path)):
                if os.path.isdir(os.path.join(path, c)):
                    print(f'Testimonial: {c}')
                    process(os.path.join(path, c), 'images/kitchen-testimonials', slug(c))
            continue
        print(f'Project: {d}')
        prefix = re.sub(r'[^A-Za-z0-9]+', '-', d).strip('-') + '-image'   # Project-01 -> Project-01-image
        made = process(path, 'images/kitchen', prefix)
        if not made:
            continue
        full = ','.join(f'images/kitchen/full/{m}' for m in made)
        cls = ['tile-feature', 'tile-tall', '', '', 'tile-wide', 'tile-wide'][len(tiles)] if len(tiles) < 6 else ''
        count = f'\n          <span class="tile-count">{len(made)} photos</span>' if len(made) > 1 else ''
        tiles.append(f'''        <!-- {d}: replace AREA with the area only (e.g. Fulham), never a street -->
        <button type="button" class="tile {cls}" data-images="{full}" data-caption="Kitchen in AREA">
          <img src="images/kitchen/low/{made[0]}" alt="Kitchen renovation by A&amp;G Renovations in AREA, London" loading="lazy" decoding="async" width="800" height="600">
          <span class="tile-cap">Kitchen in AREA</span>{count}
        </button>
''')
    if tiles:
        with open('gallery-tiles.html', 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(tiles))
        print(f'\nWrote gallery-tiles.html with {len(tiles)} tile(s).')


if __name__ == '__main__':
    main()
