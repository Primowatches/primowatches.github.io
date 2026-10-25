"""Primowatches site: every page is generated from faces.json.

  python build.py

A new watch face: add an entry to faces.json and its images to
watchfaces/<slug>/ (square, transparent outside the dial, about 600 px).
Its page is watchfaces/<slug>/, a URL that never changes once it is in a Play
listing. status: "coming" (no Play link yet) or "live".

A Garmin app is an entry under "garmin" with its images in garmin/<slug>/;
status "live" needs its Connect IQ Store link in "store". Its user guide is
a function below, registered in GUIDES.
"""
from pathlib import Path
from html import escape
import json

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / 'faces.json').read_text(encoding='utf-8'))
BRAND, EMAIL = DATA['brand'], DATA['email']
UPDATED = '26 October 2026'  # the privacy policy's date: change it when its text changes


def menus():
    """One drop-down per platform; <details> opens on tap without a script."""
    wear = ''.join(f'<a href="{{up}}watchfaces/{f["slug"]}/">{escape(f["name"])}</a>' for f in DATA['faces'])
    garmin = ''.join(f'<a href="{{up}}garmin/{a["slug"]}/">{escape(a["name"])}</a>'
                     f'<a href="{{up}}garmin/{a["slug"]}/#guide">{escape(a["name"])} user guide</a>' for a in DATA['garmin'])
    return (f'<details class="menu"><summary>Wear OS</summary><div><a href="{{home}}#watchfaces">All watch faces</a>{wear}'
            f'<a href="{{up}}install.html">Install a watch face</a></div></details>'
            f'<details class="menu"><summary>Garmin</summary><div>{garmin}</div></details>')


def page(path, title, description, body):
    """One page; `path` is relative to the site root, links are made relative to it."""
    up = '../' * path.count('/')
    nav = menus().replace('{home}', up or './').replace('{up}', up)
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
  <nav>{nav}<a href="{up}privacy.html">Privacy</a><a href="{up or './'}#contact">Contact</a></nav>
</header>
<script>document.addEventListener('click', e => document.querySelectorAll('nav details[open]').forEach(d => {{ if (!d.contains(e.target)) d.open = false; }}));</script>
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


def card(f, folder='watchfaces'):
    img, alt = f['images'][0]
    return f'''  <a class="card" href="{{up}}{folder}/{f["slug"]}/">
    <img src="{{up}}{folder}/{f["slug"]}/{img}" alt="{escape(alt)}" width="600" height="600" loading="lazy">
    <strong>{escape(f["name"])}</strong>
    <span>{escape(f["tagline"])}</span>
    {"" if f["status"] == "live" else '<em>Coming soon</em>'}
  </a>'''


def home():
    cards = '\n'.join(card(f) for f in DATA['faces'])
    apps = '\n'.join(card(a, 'garmin') for a in DATA['garmin'])
    page('index.html', f'{BRAND}: watch faces for Wear OS and Garmin apps', DATA['tagline'], f'''<h1>{BRAND}</h1>
<div class="rule"></div>
<p class="lead">{escape(DATA["tagline"])}</p>

<h2 id="watchfaces">Wear OS watch faces</h2>
<div class="grid">
{cards}
</div>

<h2 id="garmin">Garmin apps</h2>
<div class="grid">
{apps}
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
    apps = ', '.join(a['name'] for a in DATA['garmin'])
    page('privacy.html', f'Privacy policy · {BRAND}', f'Privacy policy for {BRAND} watch faces and Garmin apps.', f'''<h1>Privacy policy</h1>
<div class="rule"></div>
<p class="lead">Applies to every {BRAND} watch face on Google Play ({escape(names)}) and every {BRAND} app for Garmin watches ({escape(apps)}). Last updated {UPDATED}.</p>

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

<h2>Garmin apps</h2>
<p>Our Garmin apps have no network access, no analytics and no advertising, and we receive nothing from them. Your workouts, programs and settings are stored on your watch. When you choose to save a workout to Garmin Connect, it becomes a Garmin activity that syncs through Garmin's own apps, under the <a href="https://www.garmin.com/privacy/connect/">Garmin Connect privacy policy</a>. Settings you change in Garmin Connect or the Connect IQ Store app are sent by Garmin to your watch only.</p>

<h2>Children</h2>
<p>Our watch faces and apps collect no data from anyone, including children.</p>

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


def ciq_button(a):
    if a['status'] == 'live':
        return f'<a class="button" href="{escape(a["store"])}">Get it in the Connect IQ Store</a>'
    return '<span class="badge">Coming soon to the Connect IQ Store</span>'


def strength_guide():
    return '''<h3 id="start">Getting started</h3>
<ol>
  <li>Install Strength from the Connect IQ Store, in the Connect IQ app or Garmin Connect on your phone, and sync your watch.</li>
  <li>On the watch, open your apps (or activities) list and choose <strong>Strength</strong>.</li>
  <li>The home screen has <strong>Start workout</strong>, <strong>Program</strong>, <strong>History</strong> and <strong>Settings</strong>.</li>
</ol>
<table>
  <tr><th>Button</th><th>What it does</th></tr>
  <tr><td><strong>START/OK</strong></td><td>Choose, and log a set during a workout</td></tr>
  <tr><td><strong>UP/DOWN</strong></td><td>Move in lists, and change the highlighted weight or reps</td></tr>
  <tr><td><strong>BACK/LAP</strong></td><td>Go back. In a workout it switches between KG and REPS</td></tr>
  <tr><td><strong>MENU</strong> (hold UP)</td><td>The workout menu, and edit or delete in lists</td></tr>
</table>
<p>On touchscreen watches you can tap rows and swipe up and down. Swipe right to go back, except during a workout, where swiping left or right switches between KG and REPS.</p>
<p><strong>Leaving the app:</strong> press BACK (or swipe right) until you are on the home screen, then once more. During a workout, finish it first with <strong>MENU › Finish workout</strong>.</p>

<h3 id="workout">A workout at the gym</h3>
<ol>
  <li>Choose <strong>Start workout</strong>. The first exercise shows last time's heaviest weight and the program's target reps. The line at the bottom shows every set from last time, for example <code>LAST 60x8 60x8 60x7</code>.</li>
  <li><strong>↑</strong> next to KG means you reached the target reps in every set last time, so the weight has gone up one step. Press DOWN to keep the old weight.</li>
  <li><strong>UP/DOWN</strong> change the highlighted value and <strong>BACK/LAP</strong> switches between KG and REPS. Press quickly several times in a row and the weight changes faster.</li>
  <li>Lift, then press <strong>START/OK</strong> once. The set is logged and the rest starts.</li>
  <li>During the rest, reps are highlighted: use <strong>UP/DOWN</strong> if you did more or fewer reps than planned. <strong>LAP</strong> switches to the weight. A new personal record vibrates and shows <strong>NEW PR</strong>.</li>
  <li>The watch gives a short alert 10 seconds before the rest ends, and a longer one (with sound if tones are on) when it is over. The screen lights up and shows the next set. An extra press right after logging never skips the rest.</li>
  <li>Hold <strong>MENU</strong> for the workout menu: <strong>Undo last set</strong>, <strong>+30 s rest</strong>, <strong>Do later</strong>, <strong>Skip exercise</strong>, <strong>Add/remove set</strong> and <strong>Finish workout</strong>.</li>
  <li>After the last set you can check and correct it before you press <strong>START/OK = Save</strong>.</li>
  <li>Choose <strong>Save + sync</strong> (the workout becomes an activity in Garmin Connect) or <strong>Watch only</strong> (nothing is sent to your phone). The summary shows time, sets, volume and new records.</li>
</ol>
<p>Exercises without weight are logged at 0 kg and get their own charts for max reps and total reps.</p>

<h3 id="programs">Programs</h3>
<p>Strength has four ready-made programs (Full body, Strength, Muscle gain and At home) and four slots for your own.</p>
<p><strong>Create a program on the watch</strong></p>
<ol>
  <li>Open <strong>Program</strong> and choose <strong>+ New program</strong> at the bottom of the list.</li>
  <li>Type a name with the watch's text picker, or skip it to keep "Program 1–4".</li>
  <li>Choose <strong>+ Add exercise</strong>, then a muscle group and an exercise, and set sets, reps, rest and start weight. Repeat for each exercise.</li>
</ol>
<p><strong>Change a program on the watch:</strong> highlight it in the Program list and <strong>hold MENU</strong>. You get <strong>Exercises</strong> (add, change, or hold MENU on an exercise to remove it), <strong>Rename</strong> and <strong>Delete program</strong> (press twice).</p>
<p><strong>On your phone:</strong> open Garmin Connect or the Connect IQ app, find Strength among your watch's apps and open <strong>Settings</strong>. Each program has a <strong>Program name</strong> field and a list of exercises with sets, reps, rest (seconds) and start weight (decimals such as 22.5 kg are allowed).</p>
<ul>
  <li>Each row has an <strong>Exercise name</strong>, such as "1. BENCH PRESS", filled in and overwritten by the watch: you can leave it alone. A row you have just added gets its name once the watch has received the settings: close and reopen the settings to see it.</li>
  <li><strong>Change the order:</strong> open an exercise, set <strong>Order</strong> to the position you want (1 for the top, 0 to leave it) and save. The watch moves it there and renumbers the rest. Garmin's settings list has no drag and drop.</li>
</ul>
<p>Phone settings are only available when Strength is installed from the Connect IQ Store.</p>

<h3 id="custom">Your own exercises</h3>
<p>There are 12 slots for exercises of your own, and each can be used in several programs.</p>
<p><strong>On the watch</strong></p>
<ol>
  <li>Open the program: <strong>Program › highlight it › hold MENU › Exercises</strong>.</li>
  <li>Choose <strong>+ Add exercise › My exercises › + New exercise</strong>.</li>
  <li>Type the name, choose a muscle group, then set sets, reps, rest and start weight, and choose <strong>Save</strong>.</li>
</ol>
<p><strong>On the phone</strong></p>
<ol>
  <li>In Strength's settings, open <strong>My exercises</strong>, add a row, choose a free <strong>Custom 1–12</strong> slot, type the name and choose a muscle group.</li>
  <li>Open <strong>Program 1–4</strong>, add a row and choose the same <strong>Custom</strong> slot as the exercise.</li>
  <li>Save, and sync your watch.</li>
</ol>
<p>The exercise picker on the phone shows "Custom 1–12" because Garmin's settings lists cannot show names you have typed. The watch, and the exercise name on each program row, show the real name.</p>

<h3 id="settings">Settings</h3>
<p>All settings are on the watch under <strong>Settings</strong>, and in the phone settings.</p>
<ul>
  <li><strong>Weight step:</strong> 0.5, 1, 1.25, 2, 2.5 (default), 5 or 10 kg.</li>
  <li><strong>Rest alert:</strong> vibration + sound (default), vibration, sound or off. Your watch's own vibration and tone settings still apply.</li>
  <li><strong>Pre-alert:</strong> a short alert 10 s (default) or 5 s before the rest ends, or none. Used for rests of 30 seconds or more. The rest length itself is set per exercise in the program.</li>
  <li><strong>Garmin Connect:</strong> <em>Ask</em> (default: choose Save + sync or Watch only after each workout), <em>Always</em> or <em>Never</em>.</li>
  <li><strong>Colour:</strong> lime, cyan, orange, red, blue, purple, pink or white. Two-colour Instinct watches are always black and white.</li>
</ul>

<h3 id="history">History and progress</h3>
<p><strong>Past workouts:</strong> open <strong>History › Workout history</strong>, choose a workout and scroll through every exercise and set with weight and reps.</p>
<p><strong>Progress charts:</strong> open <strong>History › Progress</strong> and choose an exercise.</p>
<ul>
  <li><strong>START/OK</strong> switches between max weight, estimated 1RM and volume.</li>
  <li>Hold <strong>MENU</strong> to switch between 4 weeks, 3 months, 1 year and all time. On touchscreens, tap the left or right side of the chart to change the period, and the middle to change what is measured.</li>
  <li><strong>UP/DOWN</strong> jump to the next exercise.</li>
</ul>
<p>The space between points matches the real time between workouts. Estimated 1RM uses the Epley formula, up to 12 reps.</p>
<p>Most watches keep the last 220 workouts, more than a year at four workouts a week. Watches with little app memory (Forerunner 55, Venu Sq and the Instinct family) keep 60. When the limit is reached, the oldest workout is removed from the watch.</p>

<h3 id="connect">The watch and Garmin Connect</h3>
<table>
  <tr><th></th><th>On the watch (History)</th><th>In Garmin Connect</th></tr>
  <tr><td>Which workouts</td><td>The last 220 (60 on small watches), whatever you chose to sync</td><td>Every workout saved with sync</td></tr>
  <tr><td>Each set (exercise, kg, reps)</td><td>Yes</td><td>Yes, as one lap per set*</td></tr>
  <tr><td>Time, heart rate, calories</td><td>No</td><td>Yes</td></tr>
  <tr><td>Progress charts and weight suggestions</td><td>Yes</td><td>No</td></tr>
  <tr><td>Without phone or internet</td><td>Yes</td><td>No</td></tr>
</table>
<p>* The exercise, weight and reps fields need Strength installed from the Connect IQ Store, and are not recorded on the Forerunner 55, Venu Sq and Instinct family. Find them under laps or Connect IQ data on the activity in Garmin Connect.</p>
<ul>
  <li>A workout saved as <strong>Watch only</strong> is gone for good once the watch removes it to make room.</li>
  <li>Deleting an activity in Garmin Connect does not change the history on the watch, and the other way round.</li>
</ul>

<h3 id="glance">Glance</h3>
<p>Add Strength to your watch's glances (usually: hold MENU, open <em>Glances</em> and choose <em>Add</em>). It shows the program for your next workout and how long ago you trained, with sets and volume. If a workout was interrupted, it shows <strong>Resume workout</strong>. Press START/OK or tap it to open Strength.</p>

<h3 id="interrupted">Interrupted workout</h3>
<p>If the app closes in the middle of a workout, you are offered <strong>Resume workout</strong>, <strong>Save workout</strong> or <strong>Discard workout</strong> the next time you open it. Resume and Save always give one single activity in Garmin Connect (or none, if you chose Watch only).</p>

<h3 id="troubleshooting">Troubleshooting</h3>
<ul>
  <li><strong>No settings on the phone:</strong> they appear only when Strength is installed from the Connect IQ Store, and your watch is connected to the phone.</li>
  <li><strong>A phone change does not show on the watch:</strong> sync the watch in Garmin Connect, then reopen Strength. A running workout is never changed: new settings apply from the next one.</li>
  <li><strong>No exercise names in the phone list:</strong> the watch fills them in after it has received the settings. Open Strength on the watch once, then reopen the settings on the phone.</li>
  <li><strong>Can't leave the app:</strong> press BACK (or swipe right) until you reach the home screen, then once more. During a workout, finish it from MENU first.</li>
</ul>'''


GUIDES = {'strength': strength_guide}


def garmin_app(a):
    imgs = '\n'.join(f'  <img src="{i}" alt="{escape(t)}" width="500" height="500" loading="lazy">' for i, t in a['images'])
    feats = '\n'.join(f'  <li>{escape(x)}</li>' for x in a['features'])
    guide = GUIDES[a['slug']]()
    page(f'garmin/{a["slug"]}/index.html', f'{a["name"]} for Garmin watches', f'{a["name"]}: {a["intro"]}', f'''<p class="crumb"><a href="{{up}}#garmin">Garmin apps</a> /</p>
<h1>{escape(a["name"])}</h1>
<div class="rule"></div>
<p class="lead">{escape(a["intro"])}</p>
<p>{ciq_button(a)} <a class="ghost" href="#guide">Read the user guide</a></p>

<div class="shots">
{imgs}
</div>

<h2>Features</h2>
<ul>
{feats}
</ul>

<h2>Requirements</h2>
<p>{escape(a["requires"])}. Settings on the phone need Garmin Connect or the Connect IQ app.</p>

<h2 id="guide">User guide</h2>
<div class="toc"><a href="#start">Getting started</a><a href="#workout">A workout</a><a href="#programs">Programs</a><a href="#custom">Your own exercises</a><a href="#settings">Settings</a><a href="#history">History and progress</a><a href="#connect">Garmin Connect</a><a href="#glance">Glance</a><a href="#interrupted">Interrupted workout</a><a href="#troubleshooting">Troubleshooting</a></div>
{guide}

<h2>Support</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your watch model. {escape(a["name"])} sends no data to us: see the <a href="{{up}}privacy.html">privacy policy</a>.</p>''')


if __name__ == '__main__':
    home()
    for f in DATA['faces']:
        face(f)
    for a in DATA['garmin']:
        garmin_app(a)
    install()
    privacy()
