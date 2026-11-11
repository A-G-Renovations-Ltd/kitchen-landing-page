"""
Prepare kitchen project photos for the landing page.

Put the original photos (iPhone RAW .DNG, .HEIC, .JPG or .PNG) in photos-raw/<project-slug>/, e.g.
photos-raw/kensal/. Name the folder after the area. Then run from the repo root:

    pip install pillow rawpy pillow-heif
    python optimize_kitchen_photos.py kensal "Kitchen in Kensal"

For every photo it writes AVIF and WebP at 480, 800, 1200 and 1600px wide to images/kitchens/<slug>/, with all
metadata removed (including GPS), plus a tiny blurred preview. AVIF is about half the size of JPEG at the same
visible quality; WebP is the fallback. Browsers pick the right size for the screen, so phones on a weak signal
download small files. It also writes project-<slug>.html: a ready project tile to paste into the gallery grid.
Photos are used in name order; rename them (01-..., 02-...) so the cover photo sorts first. Leave out near-duplicates.
"""
import base64, io, os, sys
from PIL import Image, ImageOps

try:
    import pillow_heif; pillow_heif.register_heif_opener()
except ImportError:
    pass

WIDTHS = [480, 800, 1200, 1600]


def load(path):
    if path.lower().endswith('.dng'):
        import rawpy
        with rawpy.imread(path) as raw:
            flip = raw.sizes.flip; t = raw.extract_thumb()
            im = Image.open(io.BytesIO(t.data)) if t.format == rawpy.ThumbFormat.JPEG else Image.fromarray(t.data)
        im = ImageOps.exif_transpose(im)
        if flip in (5, 6) and im.width > im.height: im = im.rotate(90 if flip == 5 else -90, expand=True)
        if flip == 3: im = im.rotate(180)
    else:
        im = ImageOps.exif_transpose(Image.open(path))
    px = Image.new('RGB', im.size); px.paste(im.convert('RGB'))   # pixels only: no EXIF or GPS
    return px


def main():
    if len(sys.argv) < 3:
        raise SystemExit('Usage: python optimize_kitchen_photos.py <slug> "<caption>"')
    slug, caption = sys.argv[1], sys.argv[2]
    src_dir = os.path.join('photos-raw', slug); out = os.path.join('images', 'kitchens', slug)
    os.makedirs(out, exist_ok=True)
    files = sorted(f for f in os.listdir(src_dir) if f.lower().endswith(('.dng', '.heic', '.jpg', '.jpeg', '.png', '.webp')))
    meta = []
    for i, f in enumerate(files, 1):
        im = load(os.path.join(src_dir, f))
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        name = f'{slug}-{i:02d}'; sizes = []
        for w in WIDTHS:
            h = round(im.height * w / im.width); r = im if w == 1600 else im.resize((w, h), Image.LANCZOS)
            r.save(os.path.join(out, f'{name}-{w}.avif'), 'AVIF', quality=62, speed=6)
            r.save(os.path.join(out, f'{name}-{w}.webp'), 'WEBP', quality=80, method=4)
            sizes.append((w, h))
        t = im.resize((24, round(im.height * 24 / im.width))); b = io.BytesIO(); t.save(b, 'WEBP', quality=40)
        meta.append((name, sizes, 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()))
        print(f'  {f} -> {out}/{name}-*.avif/.webp')
    bases = ','.join(f'images/kitchens/{slug}/{n}' for n, _, _ in meta)
    n0, sizes, lqip = meta[0]; b = f'images/kitchens/{slug}/{n0}'; w, h = sizes[-1]
    sz = '(max-width: 860px) 82vw, 380px'
    av = ', '.join(f'{b}-{x}.avif {x}w' for x, _ in sizes); wb = ', '.join(f'{b}-{x}.webp {x}w' for x, _ in sizes)
    block = f'''          <!-- PROJECT TILE: {slug} -->
          <button type="button" class="ptile" data-base="{bases}" data-start="0" data-caption="{caption}" aria-label="View {caption}, {len(meta)} photos">
            <picture style="background-image:url('{lqip}')"><source type="image/avif" sizes="{sz}" srcset="{av}"><source type="image/webp" sizes="{sz}" srcset="{wb}"><img src="{b}-800.webp" alt="WRITE A SHORT FACTUAL DESCRIPTION OF THE COVER PHOTO" width="{w}" height="{h}" loading="lazy" decoding="async"></picture>
            <span class="ptile-count">{len(meta)} photos</span>
            <span class="ptile-meta"><span class="ptile-title">{caption}</span><span class="ptile-sub">WRITE ONE SHORT LINE ABOUT THE KITCHEN</span><span class="ptile-view">View project</span></span>
          </button>
'''
    open(f'project-{slug}.html', 'w', encoding='utf-8').write(block)
    print(f'\nWrote project-{slug}.html. Paste it inside <div class="ptiles"> in the gallery, then fill in the alt text and the short line.')


if __name__ == '__main__':
    main()
