"""
Build the staging copy from this (production) repo.

Run from this repo's root:   python make_staging.py
Default target: ../kitchen-landing-page-staging   (or pass a folder: python make_staging.py D:/path/to/staging)

The staging copy gets: tracking removed (GTM, Clarity, gtag), a noindex tag, no Zapier webhook,
AG_STAGING = true (the form shows success but sends nothing), robots.txt Disallow, and no CNAME.
Edit index.html HERE only; never edit the staging index.html by hand.
"""
import os
import re
import shutil
import sys

target = sys.argv[1] if len(sys.argv) > 1 else os.path.join('..', 'kitchen-landing-page-staging')
os.makedirs(target, exist_ok=True)

s = open('index.html', encoding='utf-8').read()
s = re.sub(r'[ \t]*<!-- TRACKING:START.*?<!-- TRACKING:END -->\n', '', s, flags=re.S)


def rep(old, new):
    global s
    if s.count(old) != 1:
        raise SystemExit(f'Stopped: expected exactly one "{old[:50]}" in index.html. Nothing was written.')
    s = s.replace(old, new)


rep('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '  <meta name="robots" content="noindex, nofollow">\n'
    '  <!-- STAGING COPY: tracking removed, form sends nothing. Never deploy this file to the live repo. -->')
rep("const AG_WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/27822859/4bkdgjs/';",
    "const AG_WEBHOOK_URL = ''; /* STAGING: no webhook */")
rep('const AG_STAGING = false;', 'const AG_STAGING = true;')

for bad in ('googletagmanager.com/gtm.js', 'clarity.ms/tag', 'gtag/js?id=', 'hooks.zapier.com'):
    if bad in s:
        raise SystemExit(f'Stopped: "{bad}" still present after conversion. Nothing was written.')

with open(os.path.join(target, 'index.html'), 'w', encoding='utf-8') as fh:
    fh.write(s)
for d in ('dist', 'images', 'src'):
    shutil.copytree(d, os.path.join(target, d), dirs_exist_ok=True)
for f in ('logo.jpeg', 'package.json', 'package-lock.json', '.gitignore'):
    shutil.copy2(f, os.path.join(target, f))
with open(os.path.join(target, 'robots.txt'), 'w') as fh:
    fh.write('User-agent: *\nDisallow: /\n')
if os.path.exists(os.path.join(target, 'CNAME')):
    os.remove(os.path.join(target, 'CNAME'))
print(f'Staging copy written to {os.path.abspath(target)}')
