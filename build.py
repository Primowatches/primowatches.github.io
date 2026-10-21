"""Primowatches site: every page is generated from faces.json.

  python build.py

A new watch face: add an entry to faces.json and its images to
watchfaces/<slug>/ (square, transparent outside the dial, about 600 px).
Its page is watchfaces/<slug>/, a URL that never changes once it is in a Play
listing. status: "coming" (no Play link yet) or "live".
"""
from pathlib import Path
from html import escape
import json

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / 'faces.json').read_text(encoding='utf-8'))
BRAND, EMAIL = DATA['brand'], DATA['email']
UPDATED = '18 October 2026'  # the privacy policy's date: change it when its text changes


def page(path, title, description, body):
    """One page; `path` is relative to the site root, links are made relative to it."""
    up = '../' * path.count('/')
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="google-site-verification" content="F2sSLz3GuPwt_C3BkwWSnTi81Ip2itNgBJjz8FT71gg">
<meta name="google-site-verification" content="0I45dqfzrLrNNodKksoEg44V1YR8bqElhHY7i-KYdTE">
<link rel="icon" href="{up}assets/icon.png">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header>
  <a class="brand" href="{up or './'}">{BRAND}</a>
  <nav><a href="{up or './'}#watchfaces">Watch faces</a><a href="{up}install.html">Install</a><a href="{up}privacy.html">Privacy</a><a href="{up or './'}#contact">Contact</a></nav>
</header>
<main>
{body.replace('{up}', up)}
</main>
<footer>© 2026 {BRAND} · <a href="{up}privacy.html">Privacy policy</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></footer>
</body>
</html>
'''
    out = HERE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8', newline='\n')
    print(path)


def store_button(f):
    if f['status'] == 'live':
        return f'<a class="button" href="{escape(f["play"])}">Get it on Google Play</a>'
    return '<span class="badge">Coming soon to Google Play</span>'


def card(f):
    img, alt = f['images'][0]
    return f'''  <a class="card" href="{{up}}watchfaces/{f["slug"]}/">
    <img src="{{up}}watchfaces/{f["slug"]}/{img}" alt="{escape(alt)}" width="600" height="600" loading="lazy">
    <strong>{escape(f["name"])}</strong>
    <span>{escape(f["tagline"])}</span>
    {"" if f["status"] == "live" else '<em>Coming soon</em>'}
  </a>'''


def home():
    cards = '\n'.join(card(f) for f in DATA['faces'])
    page('index.html', f'{BRAND}: watch faces for Wear OS', DATA['tagline'], f'''<h1>{BRAND}</h1>
<div class="rule"></div>
<p class="lead">{escape(DATA["tagline"])}</p>

<h2 id="watchfaces">Watch faces</h2>
<div class="grid">
{cards}
</div>

<h2 id="contact">Contact</h2>
<p>Questions, support or feedback: <a href="mailto:{EMAIL}">{EMAIL}</a></p>''')


def face(f):
    imgs = '\n'.join(f'  <img src="{i}" alt="{escape(a)}" width="600" height="600" loading="lazy">' for i, a in f['images'])
    feats = '\n'.join(f'  <li>{escape(x)}</li>' for x in f['features'])
    page(f'watchfaces/{f["slug"]}/index.html', f'{f["name"]} watch face for Wear OS', f'{f["name"]}: {f["intro"]}', f'''<p class="crumb"><a href="{{up}}#watchfaces">Watch faces</a> /</p>
<h1>{escape(f["name"])}</h1>
<div class="rule"></div>
<p class="lead">{escape(f["intro"])}</p>
<p>{store_button(f)}</p>

<div class="dials">
{imgs}
</div>

<h2>Features</h2>
<ul>
{feats}
</ul>

<h2>Requirements</h2>
<p>{escape(f["requires"])}: Samsung Galaxy Watch4 and later, Google Pixel Watch, OnePlus Watch 2 and later, and other Wear OS watches with a round screen.</p>

<h2>Install and customise</h2>
<p>Can't find {escape(f["name"])} on your watch after buying it? See <a href="{{up}}install.html">how to install and set a watch face</a>.</p>

<h2>Support</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>. {escape(f["name"])} collects no data: see the <a href="{{up}}privacy.html">privacy policy</a>.</p>''')


def privacy():
    names = ', '.join(f['name'] for f in DATA['faces'])
    page('privacy.html', f'Privacy policy · {BRAND}', f'Privacy policy for {BRAND} watch faces.', f'''<h1>Privacy policy</h1>
<div class="rule"></div>
<p class="lead">Applies to every {BRAND} watch face on Google Play ({escape(names)}). Last updated {UPDATED}.</p>

<h2>Summary</h2>
<p>Our watch faces do not collect, store, share or sell any personal data. They contain no code, no analytics, no advertising and no network access.</p>

<h2>What a watch face shows</h2>
<p>Our watch faces display information your watch already has, such as time, date, battery level, steps, heart rate and weather. It is provided by Wear OS and by the apps you choose for each complication slot, and drawn on your watch only. It never leaves your watch through the watch face, and we never receive it.</p>

<h2>Permissions</h2>
<p>Our watch faces request no Android permissions. Access to data shown in complications is controlled by Wear OS and by the app that provides each complication, under that app's own privacy policy.</p>

<h2>Settings</h2>
<p>Your choices, such as colours and surfaces, are stored by Wear OS on your watch. We have no access to them.</p>

<h2>Google Play</h2>
<p>Google Play handles downloads, purchases and reviews, under the <a href="https://policies.google.com/privacy">Google Privacy Policy</a>. We receive only anonymous, aggregated statistics from Google Play Console, such as the number of installs.</p>

<h2>Children</h2>
<p>Our watch faces collect no data from anyone, including children.</p>

<h2>Changes</h2>
<p>If this policy changes, the new version is published on this page with a new date.</p>

<h2>Contact</h2>
<p>{BRAND}. Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')


def install():
    page('install.html', f'Install a watch face · {BRAND}', f'How to install, set and customise a {BRAND} watch face on Wear OS.', f'''<h1>Install a watch face</h1>
<div class="rule"></div>
<p class="lead">Our watch faces run on the watch itself. Installing one does not switch your watch face: you choose it on the watch afterwards.</p>

<h2>1. Install</h2>
<ul>
  <li><strong>From your phone:</strong> open the watch face in Google Play, tap the arrow next to Install (or Buy) and make sure your watch is ticked.</li>
  <li><strong>From your watch:</strong> open Play Store on the watch, search for the watch face and install it.</li>
</ul>
<p>It can take a few minutes before the watch face reaches the watch. The phone app may say it is installed before the watch has it.</p>

<h2>2. Set it as your watch face</h2>
<ul>
  <li><strong>On the watch:</strong> touch and hold the current watch face, swipe to the end and tap <em>Add</em> (+), then choose the watch face.</li>
  <li><strong>Samsung Galaxy Watch:</strong> or open the Galaxy Wearable app on your phone, tap <em>Watch faces</em> and choose it.</li>
  <li><strong>Google Pixel Watch:</strong> or open the Pixel Watch app on your phone, tap <em>Watch faces</em> and add it.</li>
</ul>

<h2>3. Customise</h2>
<p>Touch and hold the watch face and tap <em>Customise</em> (or the pencil). Swipe between colours, surfaces and the other options. On the data page, tap a field to choose what it shows: any app on your watch can provide data. Galaxy Wearable and the Pixel Watch app can customise it from your phone too.</p>

<h2>Always-on display</h2>
<p>The always-on look appears only when <em>Always-on display</em> is turned on in your watch's display settings. The style and brightness are chosen in the watch face's own options.</p>

<h2>Troubleshooting</h2>
<ul>
  <li><strong>Not offered for my watch:</strong> our watch faces need Wear OS 5 or newer and a round screen. Check under Settings › System › About › Versions.</li>
  <li><strong>Installed, but not in the list:</strong> wait a few minutes, or restart the watch. Then try Play Store on the watch itself.</li>
  <li><strong>Empty fields or dashes:</strong> the app providing the data may need permission (heart rate, location for weather), or has no data yet. Open that app on the watch once.</li>
  <li><strong>Weather missing:</strong> weather comes from your watch's weather app, which needs a connection to your phone or the internet.</li>
</ul>
<p>Still stuck? Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your watch model.</p>''')


if __name__ == '__main__':
    home()
    for f in DATA['faces']:
        face(f)
    install()
    privacy()
