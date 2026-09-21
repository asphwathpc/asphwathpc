#!/usr/bin/env python3
"""Build the Ashwath FM art for the profile README into assets/.

GitHub shows README images without loading outside CSS or fonts, so each
panel is HTML/CSS inside an SVG <foreignObject>, with the site's fonts
(Shrikhand, Bricolage Grotesque, Space Mono) subset from Google Fonts to just
the letters that panel uses and inlined as base64. Colours and shapes follow
the funk preset in Resume/funk/src/funk.css.

Edit the copy below, then run:  python3 build.py
"""

import base64
import html
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path(__file__).parent / "assets"
FONTS = (
    "family=Shrikhand"
    "&family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800"
    "&family=Space+Mono:wght@400;700"
)
# Google Fonts only serves woff2 to browsers it recognises.
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"

GRAIN = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E"
    "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E"
    "%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.2 0'/%3E%3C/filter%3E"
    "%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E\")"
)

BASE = """
.v{--paper:#fff3dc;--paper-2:#ffe4b8;--ink:#2a0e3d;--ink-soft:#5b3a6e;--line:#2a0e3d;
--c1:#ff4fa3;--c2:#ff7b1c;--c3:#ffc93c;--c4:#00bfa6;--c5:#a98bff;
--display:'Shrikhand',Georgia,serif;--sans:'Bricolage Grotesque',system-ui,sans-serif;--mono:'Space Mono',ui-monospace,monospace;
position:relative;overflow:hidden;box-sizing:border-box;color:var(--ink);font:400 16px/1.5 var(--sans);-webkit-font-smoothing:antialiased}
.v *{box-sizing:border-box;margin:0;padding:0}
.p{width:840px;background:var(--paper);border:3px solid var(--line);border-radius:28px}
.p::after{content:'';position:absolute;inset:0;z-index:50;pointer-events:none;opacity:.13;background-image:""" + GRAIN + """}
.dots{background:var(--paper-2) radial-gradient(circle,rgba(42,14,61,.16) 1.3px,transparent 1.8px) 0 0/22px 22px}
.head{position:relative;padding:36px 40px 0}
.eyebrow{font:700 13px var(--mono);text-transform:uppercase;letter-spacing:.12em;color:var(--ink-soft)}
.display{margin-top:8px;font:800 54px/.98 var(--sans);font-stretch:78%;letter-spacing:-.02em}
.display mark{font-family:var(--display);font-weight:400;font-stretch:normal;letter-spacing:0;color:var(--c1);background:none;
-webkit-text-stroke:.025em var(--line);paint-order:stroke fill;text-shadow:.05em .05em 0 var(--line)}
.lede{margin-top:14px;max-width:700px;font-size:17px;line-height:1.45;color:var(--ink-soft)}
@keyframes spin{to{transform:rotate(1turn)}}
@keyframes marquee{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.v *{animation:none!important}}
"""


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
        return r.read()


def font_css(text):
    chars = "".join(sorted(set(text + text.upper()) - set("\n\t")))
    css = fetch(f"https://fonts.googleapis.com/css2?{FONTS}&text={urllib.parse.quote(chars)}&display=block").decode()
    return re.sub(
        r"url\((https://[^)]+)\)",
        lambda m: "url(data:font/woff2;base64," + base64.b64encode(fetch(m.group(1))).decode() + ")",
        css,
    )


def svg(w, h, cls, css, body):
    text = html.unescape(re.sub(r"<[^>]+>", "", body))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f"<style><![CDATA[{font_css(text)}{BASE}{css}]]></style>\n"
        f'<foreignObject width="{w}" height="{h}">\n'
        f'<div xmlns="http://www.w3.org/1999/xhtml" class="v {cls}" style="width:{w}px;height:{h}px">{body}</div>\n'
        "</foreignObject>\n</svg>\n"
    )


def head(eyebrow, display, lede=""):
    return f'<div class="head"><p class="eyebrow">{eyebrow}</p><h2 class="display">{display}</h2>' + (
        f'<p class="lede">{lede}</p>' if lede else ""
    ) + "</div>"


def icon(paths):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{paths}</svg>'


# ---------------------------------------------------------------- hero

HERO_CSS = """
.hero{text-align:center}
.sun{position:absolute;left:50%;top:44%;width:1500px;height:1500px;margin:-750px 0 0 -750px;
background:repeating-conic-gradient(from 0deg,rgba(255,201,60,.6) 0 5deg,transparent 5deg 10deg);
-webkit-mask:radial-gradient(closest-side,#000 15%,transparent 72%);mask:radial-gradient(closest-side,#000 15%,transparent 72%);
animation:spin 120s linear infinite}
.rainbow{position:absolute;left:50%;bottom:-250px;width:1200px;height:600px;margin-left:-600px;
background:radial-gradient(circle farthest-side at 50% 100%,transparent 0 42%,var(--line) 42% 42.6%,var(--c4) 42.6% 52%,var(--line) 52% 52.6%,
var(--c3) 52.6% 62%,var(--line) 62% 62.6%,var(--c2) 62.6% 72%,var(--line) 72% 72.6%,var(--c1) 72.6% 82%,var(--line) 82% 82.6%,transparent 82.6%)}
.inner{position:relative;z-index:3;padding-top:40px}
.chip{display:inline-flex;align-items:center;gap:9px;padding:6px 15px;background:var(--paper);border:2.5px solid var(--line);
border-radius:999px;box-shadow:3px 3px 0 var(--line);font:700 12.5px var(--mono);text-transform:uppercase;letter-spacing:.08em}
.dot{width:10px;height:10px;border-radius:50%;background:#ff2d2d;animation:onair 1.6s ease-out infinite}
@keyframes onair{from{box-shadow:0 0 0 0 rgba(255,45,45,.5)}to{box-shadow:0 0 0 10px rgba(255,45,45,0)}}
.name{margin-top:14px;font:400 108px/.92 var(--display)}
.w{display:block;white-space:nowrap}
.w+.w{transform:translateX(.4em)}
.w span{display:inline-block;color:var(--c1);-webkit-text-stroke:.032em var(--line);paint-order:stroke fill;
text-shadow:.045em .045em 0 var(--c3),.09em .09em 0 var(--line);animation:wave 3.2s ease-in-out infinite}
.w+.w span{color:var(--c4);text-shadow:.045em .045em 0 var(--c2),.09em .09em 0 var(--line)}
@keyframes wave{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-.07em) rotate(3deg)}}
.role,.hlede{text-shadow:0 0 6px var(--paper),0 0 14px var(--paper),0 0 2px var(--paper)}
.role{margin-top:26px;font:700 13px var(--mono);text-transform:uppercase;letter-spacing:.08em}
.role span{color:var(--c1)}
.hlede{margin-top:6px;font-size:22px;font-weight:600;line-height:1.35}
.radio{display:flex;width:680px;margin:24px auto 0;padding:12px;color:#f5ead6;background:linear-gradient(#3b2352,#1c0c27);
border:3px solid var(--line);border-radius:22px;box-shadow:7px 7px 0 var(--line),inset 0 2px 0 rgba(255,255,255,.15);text-align:left}
.face{flex:1;min-width:0}
.disp{position:relative;display:flex;align-items:center;height:50px;overflow:hidden;background:#0b1712;border:2px solid #000;
border-radius:10px;box-shadow:inset 0 0 22px rgba(0,0,0,.8)}
.scroll{display:flex;width:max-content;white-space:nowrap;font:700 19px var(--mono);color:var(--c3);text-shadow:0 0 10px var(--c3);
animation:marquee 30s linear infinite}
.eq{position:absolute;right:0;top:0;bottom:0;display:flex;align-items:flex-end;gap:3px;padding:10px 12px 10px 30px;
background:linear-gradient(to left,#0b1712 65%,rgba(11,23,18,0))}
.eq i{width:5px;height:18%;background:var(--c1);box-shadow:0 0 6px var(--c1);animation:eq .58s ease-in-out infinite alternate}
@keyframes eq{from{height:15%}to{height:100%}}
.dial{position:relative;display:flex;justify-content:space-between;height:30px;margin-top:10px;padding:2px 8px 0;
font:700 11px var(--mono);color:#d9c6a5;background:repeating-linear-gradient(90deg,#d9c6a5 0 1px,transparent 1px 7px) bottom/100% 8px no-repeat}
.needle{position:absolute;top:-2px;bottom:0;left:5%;width:3px;background:var(--c2);box-shadow:0 0 10px var(--c2)}
.presets{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:12px}
.pre{padding:6px 4px 8px;text-align:center;font:800 13px var(--sans);text-transform:uppercase;letter-spacing:.05em;color:#24122f;
background:linear-gradient(#f7eedd,#cdb994);border:2px solid #000;border-radius:9px;box-shadow:0 5px 0 #000}
.pre small{display:block;font:700 10.5px var(--mono);opacity:.7}
.pre.on{background:var(--c1);transform:translateY(3px);box-shadow:0 2px 0 #000}
.play{display:flex;flex:0 0 140px;flex-direction:column;align-items:center;justify-content:center;gap:10px;margin-left:12px;
font:700 11.5px var(--mono);text-transform:uppercase;letter-spacing:.06em}
.knob{position:relative;width:92px;height:92px;border-radius:50%;border:3px solid #000;box-shadow:0 6px 0 #000,inset 0 -6px 12px rgba(0,0,0,.25);
background:radial-gradient(circle,var(--c2) 0 40%,#000 40.5% 43%,transparent 43.5%),repeating-conic-gradient(#bfae90 0 3deg,#d8ccb4 3deg 10deg)}
.knob::after{content:'';position:absolute;left:50%;top:50%;margin:-11px 0 0 -6px;border-left:18px solid var(--ink);
border-top:11px solid transparent;border-bottom:11px solid transparent}
.st{position:absolute;z-index:4;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 14px;
font:800 14.5px/1.05 var(--sans);text-align:center;border:3px solid var(--line);box-shadow:4px 4px 0 var(--line);
transform:rotate(var(--r));animation:float 7s ease-in-out infinite}
.st b{display:block;font:400 36px/.9 var(--display)}
.flower b{font-size:28px}
@keyframes float{0%,100%{transform:rotate(var(--r))}50%{transform:rotate(calc(var(--r) + 7deg))}}
.star{--r:-9deg;left:30px;top:118px;width:120px;height:120px;background:var(--c3);border-radius:58% 42% 55% 45% / 45% 58% 42% 55%}
.flower{--r:-8deg;right:38px;top:104px;width:116px;height:116px;background:var(--c1);border-radius:50%;
outline:3px dashed var(--line);outline-offset:5px;font-size:13px}
.pill{--r:-7deg;left:30px;top:610px;background:var(--c4);border-radius:999px;animation-delay:-2s}
.tag{--r:5deg;right:30px;top:604px;width:150px;padding-left:22px;background:var(--c5);border-radius:10px 22px 22px 10px;animation-delay:-4s}
.tapes{position:absolute;z-index:2;left:0;right:0;bottom:92px;height:0}
.tape{position:absolute;left:-5%;width:110%;overflow:hidden;padding:3px 0;font:400 24px var(--display);white-space:nowrap;
border-top:3px solid var(--line);border-bottom:3px solid var(--line)}
.tape.a{top:0;background:var(--c3);transform:rotate(-3deg)}
.tape.b{top:12px;background:var(--c1);transform:rotate(2.2deg)}
.run{display:flex;width:max-content;animation:marquee 34s linear infinite}
.tape.b .run{animation-direction:reverse}
.run em{font-style:normal;margin:0 .4ch}
"""


def wavy(word, offset=0):
    return "".join(f'<span style="animation-delay:{-(i + offset) * 0.2:.1f}s">{ch}</span>' for i, ch in enumerate(word))


def hero():
    led = ("ASHWATH FM 88.1 ✺ PRESET 1 · FUNK ✺ ♪ NOW PLAYING ✺ NINE YEARS MAKING CAR SOFTWARE PROVE ITSELF. "
           "✺ 10 → 136 TEST BENCHES ✺ LIVE FROM BENGALURU, INDIA ✺ ")
    words = "".join(f"<span>{w} <em>✺</em> </span>" for w in ["Test", "Automate", "Flash", "Triage", "Ship", "Repeat"] * 2)
    tape = f'<div class="run"><span>{words}</span><span>{words}</span></div>'
    presets = "".join(
        f'<div class="pre{" on" if i == 1 else ""}"><small>{i}</small>{p}</div>'
        for i, p in enumerate(["Funk", "Disco", "Soul", "Boogie"], 1)
    )
    eq = "".join(f'<i style="animation-delay:{-i * 0.13:.2f}s"></i>' for i in range(7))
    dial = "".join(f"<span>{f}</span>" for f in [88, 92, 96, 100, 104, 108])
    return f"""
<div class="sun"></div><div class="rainbow"></div>
<div class="inner">
  <p class="chip"><span class="dot"></span>On air · Bengaluru, India</p>
  <h1 class="name"><span class="w">{wavy("Ashwath")}</span><span class="w">{wavy("Chandra", 7)}</span></h1>
  <p class="role">Senior Software Engineer <span>✺</span> Automotive infotainment · Test infrastructure</p>
  <p class="hlede">Nine years making car software prove itself.</p>
  <div class="radio">
    <div class="face">
      <div class="disp"><div class="scroll"><span>{led}</span><span>{led}</span></div><div class="eq">{eq}</div></div>
      <div class="dial">{dial}<i class="needle"></i></div>
      <div class="presets">{presets}</div>
    </div>
    <div class="play"><span class="knob"></span><span>Drop the beat</span></div>
  </div>
</div>
<div class="st star"><b>9</b>years in car software</div>
<div class="st flower"><b>~80%</b>blockers auto-caught</div>
<div class="st pill">10 → 136 test benches</div>
<div class="st tag">Mutton biryani specialist</div>
<div class="tapes"><div class="tape a">{tape}</div><div class="tape b">{tape}</div></div>
"""


# ---------------------------------------------------------------- chart toppers

HITS_CSS = """
.hits{padding:32px 30px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:22px}
.hit{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;height:196px;padding:18px 14px;text-align:center;
background:var(--c);border:3px solid var(--line);border-radius:48% 52% 44% 56% / 55% 42% 58% 45%;box-shadow:6px 6px 0 var(--line);
transform:rotate(var(--rot));animation:morph 9s ease-in-out infinite alternate}
.hit b{font:400 52px/1 var(--display)}
.hit span{max-width:150px;font-size:14px;font-weight:700;line-height:1.22}
@keyframes morph{to{border-radius:58% 42% 60% 40% / 42% 60% 40% 58%}}
"""

STATS = [
    ("9", "years in automotive infotainment"),
    ("136", "test benches in the farm I lead"),
    ("60%", "peak speed-up in log processing after the pipeline rebuild"),
    ("100+", "overnight test scenarios made hands-off end to end"),
]


def hits():
    blobs = "".join(
        f'<div class="hit" style="--c:var(--c{i + 1});--rot:{(i - 1.5) * 2.5}deg;animation-delay:{-i * 2.2:.1f}s"><b>{v}</b><span>{label}</span></div>'
        for i, (v, label) in enumerate(STATS)
    )
    return f'<p class="eyebrow">Chart toppers</p><div class="grid">{blobs}</div>'


# ---------------------------------------------------------------- side A: the discography

TRACKS_CSS = """
.tracks{display:grid;gap:30px;padding:30px 40px 40px}
.track{display:flex;gap:24px;align-items:flex-start}
.album{position:relative;flex:0 0 200px;height:160px}
.sleeve{position:absolute;z-index:1;left:0;top:4px;width:150px;height:150px;overflow:hidden;border:3px solid var(--line);border-radius:6px;
box-shadow:6px 6px 0 var(--line);transform:rotate(-2.5deg)}
.disc{position:absolute;left:52px;top:9px;width:140px;height:140px;display:flex;align-items:center;justify-content:center;
border:3px solid var(--line);border-radius:50%;animation:spin 3.2s linear infinite;
background:radial-gradient(circle,var(--c) 0 17%,#111 17.5% 18.5%,transparent 19%),repeating-radial-gradient(circle,#151515 0 2px,#2c2c2c 2px 4px)}
.disc span{margin-top:-22px;font:700 6.5px var(--mono);letter-spacing:.08em;color:var(--ink)}
.txt{flex:1;min-width:0}
.kick{font:700 11.5px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.who{margin-top:4px;font:700 11px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.txt h3{margin-top:6px;font:800 28px/1.05 var(--sans);font-stretch:80%;letter-spacing:-.01em}
.body{margin-top:6px;font-size:15px;line-height:1.42;color:var(--ink-soft)}
.tags{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
.tags i{padding:2px 9px;font:700 11px var(--mono);font-style:normal;background:var(--c);border:2px solid var(--line);border-radius:999px;
box-shadow:2px 2px 0 var(--line)}
.lbl{position:absolute;z-index:2;left:8px;bottom:8px;padding:1px 6px;font:700 7px var(--mono);letter-spacing:.06em;
background:var(--paper);border:2px solid var(--line);border-radius:999px}
.farm{display:flex;flex-direction:column;justify-content:center;gap:6px;padding:8px;background:#1c0c27}
.farm h4{font:400 22px/1 var(--display);color:var(--c3);text-shadow:2px 2px 0 var(--c1)}
.farm h4 small{margin-left:4px;font:700 8px var(--mono);letter-spacing:.08em;color:#f5ead6;text-shadow:none}
.bench{display:grid;grid-template-columns:repeat(17,1fr);gap:2px;padding:4px;background:#0e0616;border-radius:5px}
.bench i{height:5px;border-radius:1px;background:var(--c);box-shadow:0 0 4px var(--c)}
.bench i.soon{background:repeating-linear-gradient(45deg,rgba(245,234,214,.3) 0 1px,transparent 1px 3px);box-shadow:none;
outline:1px dashed rgba(245,234,214,.5);outline-offset:-1px;animation:blink 2.4s ease-in-out infinite}
@keyframes blink{50%{opacity:.35}}
.farm p{font:700 7.5px var(--mono);letter-spacing:.06em;color:#f5ead6}
.gate{background:repeating-conic-gradient(var(--c1) 0 25%,var(--paper) 0 50%) 0 0/36px 36px}
.post{position:absolute;left:20px;bottom:28px;width:14px;height:58px;background:var(--c2);border:2.5px solid var(--line);border-radius:3px}
.arm{position:absolute;left:24px;bottom:78px;width:118px;height:13px;border:2.5px solid var(--line);border-radius:6px;transform-origin:6px 50%;
background:repeating-linear-gradient(90deg,var(--c3) 0 12px,var(--ink) 12px 24px);animation:lift 4s ease-in-out infinite}
@keyframes lift{0%,20%{transform:rotate(-6deg)}45%,75%{transform:rotate(-58deg)}100%{transform:rotate(-6deg)}}
.sign{position:absolute;right:10px;top:14px;padding:3px 8px;font:400 12px/1.05 var(--display);text-align:center;background:var(--c4);
border:2.5px solid var(--line);border-radius:8px;transform:rotate(6deg)}
.eye{background:#1c0c27}
.rings{position:absolute;inset:-20px;background:repeating-radial-gradient(circle at 50% 50%,transparent 0 9px,var(--c4) 9px 11px);
opacity:.75;animation:pulse 2.6s ease-in-out infinite alternate}
@keyframes pulse{to{transform:scale(1.18);opacity:.45}}
.iris{position:absolute;left:50%;top:50%;width:44px;height:44px;margin:-26px 0 0 -22px;border:3px solid var(--line);border-radius:50%;
background:radial-gradient(circle,var(--ink) 0 30%,var(--c3) 32%)}
.bus{position:absolute;z-index:2;padding:1px 5px;font:700 8px var(--mono);border:2px solid var(--line);border-radius:4px}
.lava{background:linear-gradient(160deg,var(--c5),var(--c1))}
.glass{position:absolute;left:50%;top:26px;width:56px;height:84px;margin-left:-28px;overflow:hidden;background:rgba(255,243,220,.35);
border:3px solid var(--line);border-radius:40% 40% 18% 18% / 30% 30% 12% 12%}
.blob{position:absolute;left:14px;bottom:-6px;width:24px;height:24px;border-radius:50%;background:var(--c3);animation:lava 4.5s ease-in-out infinite alternate}
@keyframes lava{to{transform:translateY(-62px) scale(1.25,.85)}}
.base{position:absolute;left:50%;top:108px;width:66px;height:22px;margin-left:-33px;background:var(--ink);clip-path:polygon(14% 0,86% 0,100% 100%,0 100%)}
.lava .lbl{top:8px;bottom:auto}
"""

ROLES = [
    dict(
        c=1, kick="Track 01 · The headliner · 2023 — Present",
        who="Senior Software Engineer · Mercedes-Benz Research &amp; Development India",
        title="Grew a test-bench farm from 10 to 136.",
        body="Project MTTF turns physical automotive test benches into something engineers book on demand. I am the lead and "
             "product owner for its Infotainment &amp; Telematics ECU vertical in India — the process, the automation, and the "
             "counterpart role to the engineering team in Germany.",
        tags=["90% availability", "80% utilization", "Lead 3 engineers", "On site in Germany"],
    ),
    dict(
        c=4, kick="Track 02 · 2021 — 2023", who="Software Engineer · Wipro Ltd.",
        title="The gate every feature had to clear.",
        body="Parking &amp; Towing infotainment HMI features were validated before merge — I was the check that decided whether "
             "a feature reached the stable branch.",
        tags=["Parking &amp; Towing HMI", "System · EOL · Regression", "Process automation"],
    ),
    dict(
        c=5, kick="Track 03 · 2019 — 2021", who="Software Engineer · Altran Technologies · Deployed at Bosch",
        title="Two camera projects, seen through the logs.",
        body="Diagnostic tester on MCSOR (for Jungheinrich) and unit tester on Front Video Gen3 — reading CAN and Ethernet "
             "traffic until the behavior was explainable.",
        tags=["CAPL + Python", "Google Test", "CAN · Ethernet · DLT · Wireshark"],
    ),
    dict(
        c=2, kick="Track 04 · 2017 — 2019", who="Software Test Engineer · LG Soft India · For JLR",
        title="Where the cabin’s feel got tested.",
        body="Manual infotainment testing on the JLR PIVI program, focused on Ambient Lighting and Seat Massage — the "
             "features people don’t name but always notice.",
        tags=["JLR PIVI", "Ambient Lighting", "Seat Massage", "DLT · Putty"],
    ),
]


def sleeve(i):
    if i == 0:
        cells = "".join(
            f'<i style="--c:var(--c{n % 5 + 1})"></i>' if n < 76 else f'<i class="soon" style="animation-delay:{-n * 37}ms"></i>'
            for n in range(136)
        )
        return (f'<div class="sleeve farm"><h4>136<small>BENCHES</small></h4><div class="bench">{cells}</div>'
                "<p>76 LIVE · 60 BEING BUILT</p></div>")
    if i == 1:
        return ('<div class="sleeve gate"><div class="arm"></div><div class="post"></div>'
                '<div class="sign">Stable<br/>branch</div><span class="lbl">PRE-INTEGRATION TESTING</span></div>')
    if i == 2:
        return ('<div class="sleeve eye"><div class="rings"></div><div class="iris"></div>'
                '<span class="bus" style="left:8px;top:8px;background:var(--c5)">CAN</span>'
                '<span class="bus" style="right:8px;top:8px;background:var(--c1)">ETH</span>'
                '<span class="bus" style="right:8px;bottom:8px;background:var(--c3)">DLT</span>'
                '<span class="lbl">CAMERA SYSTEMS</span></div>')
    blobs = "".join(
        f'<i class="blob" style="left:{x}px;width:{s}px;height:{s}px;background:var(--c{c});animation-delay:{d}s"></i>'
        for x, s, c, d in [(6, 22, 3, 0), (24, 18, 2, -1.6), (14, 14, 3, -3.1)]
    )
    return f'<div class="sleeve lava"><div class="glass">{blobs}</div><div class="base"></div><span class="lbl">FIRST STEPS</span></div>'


def tracks():
    rows = "".join(
        f"""<div class="track" style="--c:var(--c{r['c']})">
  <div class="album"><div class="disc"><span>ASHWATH FM</span></div>{sleeve(i)}</div>
  <div class="txt"><p class="kick">{r['kick']}</p><p class="who">{r['who']}</p><h3>{r['title']}</h3>
  <p class="body">{r['body']}</p><p class="tags">{''.join(f'<i>{t}</i>' for t in r['tags'])}</p></div>
</div>"""
        for i, r in enumerate(ROLES)
    )
    return head(
        "Side A · The discography", "Four gigs. <mark>One groove.</mark>",
        "I build the test infrastructure that lets infotainment teams ship with confidence — from hands-on validation on a "
        "JLR head unit to leading a 136-bench automated farm at Mercedes-Benz.",
    ) + f'<div class="tracks">{rows}</div>'


# ---------------------------------------------------------------- side B: the B-sides

BSIDES_CSS = """
.cards{display:grid;grid-template-columns:1fr 1fr;gap:24px 22px;padding:28px 40px 40px}
.card{padding:16px;background:var(--paper);border:3px solid var(--line);border-radius:18px;box-shadow:6px 6px 0 var(--line)}
.card:nth-child(odd){transform:rotate(-.8deg)}
.card:nth-child(even){transform:rotate(.8deg)}
.top{display:flex;gap:14px;align-items:center}
.cas{flex:0 0 164px;height:104px;padding:10px 11px 0;background:var(--c);border:3px solid var(--line);border-radius:10px;
box-shadow:inset 0 -12px 0 rgba(0,0,0,.18)}
.lab{display:flex;align-items:center;gap:5px;padding:3px 6px;border:2px solid var(--line);border-radius:5px;
background:#fff8ec repeating-linear-gradient(transparent 0 9px,rgba(42,14,61,.13) 9px 10px)}
.lab b{padding:1px 4px;font:700 9px var(--mono);color:#fff8ec;background:#2a0e3d;border-radius:3px}
.lab span{overflow:hidden;font:400 10.5px/1.15 var(--display);white-space:nowrap;text-overflow:ellipsis}
.win{display:flex;align-items:center;justify-content:space-between;width:76%;height:38px;margin:9px auto 0;padding:0 8px;
background:#2a1a12 linear-gradient(#6b4527,#6b4527) center/46% 34% no-repeat;border:2px solid var(--line);border-radius:999px}
.reel{width:27px;height:27px;border:2px solid #000;border-radius:50%;animation:spin 2.4s linear infinite;
background:radial-gradient(circle,#2a1a12 0 20%,transparent 21%),repeating-conic-gradient(#fff8ec 0 20deg,#8a6446 20deg 60deg)}
.card h3{font:800 23px/1.05 var(--sans);font-stretch:85%}
.res{display:inline-block;margin-top:8px;padding:3px 10px;font:700 11px var(--mono);background:var(--c);border:2px solid var(--line);
border-radius:999px;box-shadow:2px 2px 0 var(--line)}
.desc{margin-top:12px;font-size:14.5px;line-height:1.42;color:var(--ink-soft)}
"""

TOOLS = [
    (2, "B1", "Result Ease", "Zero dual-entry errors",
     "A GUI tool that pushes test results to Jira through its REST API and to Confluence by scraping it — no API existed — "
     "so nothing is entered twice."),
    (3, "B2", "Automated DLT KPI", "~80% blocker detection",
     "Reads DLT logs and flags blocker and minor issues automatically. Adopted and now maintained by the defect-triaging team."),
    (4, "B3", "Smart Flash", "Hands-off daily flashing",
     "Detects, downloads and flashes daily builds with checksum validation, ignition retries and Teams alerts — the "
     "lunch-hour release window no longer needs a human watching it."),
    (5, "B4", "Log pipeline rebuild", "3–4 hours → near real-time",
     "Parallelized file handling with Python multiprocessing and ran log, report and media pipelines side by side."),
]


def bsides():
    cards = "".join(
        f"""<div class="card" style="--c:var(--c{c})"><div class="top">
  <div class="cas"><div class="lab"><b>{side}</b><span>{name}</span></div>
  <div class="win"><i class="reel"></i><i class="reel" style="animation-delay:-.7s"></i></div></div>
  <div><h3>{name}</h3><p class="res">{res}</p></div></div><p class="desc">{desc}</p></div>"""
        for c, side, name, res, desc in TOOLS
    )
    return head("Side B · The B-sides", "Tools I built to <mark>skip the boring bits.</mark>") + f'<div class="cards">{cards}</div>'


# ---------------------------------------------------------------- selections: the jukebox

JUKEBOX_CSS = """
.jb{display:flex;gap:30px;padding:28px 40px 40px}
.arch{position:relative;flex:0 0 320px;height:430px;padding:14px;overflow:hidden;border:3px solid var(--line);
border-radius:170px 170px 24px 24px;box-shadow:8px 8px 0 var(--line)}
.tube{position:absolute;left:50%;top:40%;width:760px;height:760px;margin:-380px 0 0 -380px;
background:conic-gradient(var(--c1),var(--c2),var(--c3),var(--c4),var(--c5),var(--c1));animation:spin 8s linear infinite}
.screen{position:relative;height:100%;color:#f5ead6;text-align:center;border:3px solid var(--line);border-radius:150px 150px 12px 12px;
background:#1c0c27 radial-gradient(circle at 50% 0%,rgba(255,79,163,.45),rgba(255,79,163,0) 62%)}
.np{position:absolute;left:16px;right:16px;top:70px;opacity:0;animation:np 16s infinite}
.np .eyebrow{color:var(--c3)}
.np h3{margin:8px 0 16px;font:400 42px/1.05 var(--display);color:var(--c3);text-shadow:3px 3px 0 var(--c1)}
.np li{margin-top:10px;padding:9px 12px;list-style:none;text-align:left;font-size:14px;line-height:1.35;
background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.16);border-radius:12px}
.np li b{display:block;color:var(--c4)}
.np li span{display:block;margin-bottom:3px;font:700 10.5px var(--mono);opacity:.75}
.np:first-child{opacity:1}
@keyframes np{0%,22%{opacity:1}25%,97%{opacity:0}100%{opacity:1}}
.keys{flex:1;display:flex;flex-direction:column;gap:18px}
.row{display:flex;flex-wrap:wrap;gap:9px}
.row h4{width:100%;font:700 11.5px var(--mono);text-transform:uppercase;letter-spacing:.1em;color:var(--ink-soft)}
.key{display:inline-flex;align-items:center;gap:7px;padding:5px 12px 5px 5px;font-size:14px;font-weight:700;background:var(--paper);
border:2.5px solid var(--line);border-radius:999px;box-shadow:3px 3px 0 var(--line)}
.key b{padding:1px 6px;font:700 10.5px var(--mono);background:var(--c);border:2px solid var(--line);border-radius:999px}
.key.on{animation:press 16s infinite}
@keyframes press{0%,24%{background:var(--c);transform:translate(2px,2px);box-shadow:1px 1px 0 var(--line)}
25%,100%{background:var(--paper);transform:none;box-shadow:3px 3px 0 var(--line)}}
"""

SKILLS = [
    ("Languages &amp; scripting", 1, ["Python", "Shell", "CAPL"]),
    ("Automation &amp; infrastructure", 2, ["Docker", "Ansible", "Google Test", "JFrog Artifactory CLI", "BeautifulSoup"]),
    ("Test tooling &amp; analysis", 4, ["DLT", "Putty", "Wireshark", "CAN &amp; Ethernet log analysis"]),
    ("Ways of working", 5, ["Requirement analysis", "Test design", "Defect triage", "Jira", "Confluence",
                            "Cross-border stakeholder alignment"]),
]
MB = ("Mercedes-Benz R&amp;D India", "2023 — now")
BOSCH = ("Altran · at Bosch", "2019 — 2021")
# The screen cycles through these keys; where each was played comes from Resume/src/content/skills.ts.
NOW_PLAYING = [
    ("A1", "Python", [(MB, "Log-pipeline rebuild, Smart Flash, Result Ease, bench automation"), (BOSCH, "Automation test scripts")]),
    ("A3", "CAPL", [(BOSCH, "Automation test scripts for camera ECUs")]),
    ("B1", "Docker", [(MB, "Test-bench infrastructure for Project MTTF")]),
    ("B3", "Google Test", [(BOSCH, "Unit testing on Front Video Gen3")]),
]


def jukebox():
    delay = {code: f"{-(16 - 4 * k) % 16}s" for k, (code, _, _) in enumerate(NOW_PLAYING)}
    screens = "".join(
        f'<div class="np" style="animation-delay:{delay[code]}"><p class="eyebrow">Now playing · {code}</p><h3>{name}</h3><ul>'
        + "".join(f"<li><b>{who}</b><span>{years}</span>{what}</li>" for (who, years), what in gigs)
        + "</ul></div>"
        for code, name, gigs in NOW_PLAYING
    )
    rows = ""
    for (title, c, names), letter in zip(SKILLS, "ABCD"):
        keys = ""
        for n, name in enumerate(names, 1):
            code = f"{letter}{n}"
            on = f' on" style="animation-delay:{delay[code]}' if code in delay else ""
            keys += f'<span class="key{on}"><b>{code}</b>{name}</span>'
        rows += f'<div class="row" style="--c:var(--c{c})"><h4>{title}</h4>{keys}</div>'
    return head(
        "Selections", "The <mark>jukebox.</mark>",
        "Punch in a skill to hear where it actually got played. No star ratings, just the gigs.",
    ) + f'<div class="jb"><div class="arch"><div class="tube"></div><div class="screen">{screens}</div></div><div class="keys">{rows}</div></div>'


# ---------------------------------------------------------------- bonus tracks

BONUS_CSS = """
.quests{display:grid;grid-template-columns:repeat(4,1fr);gap:22px 18px;padding:28px 40px 40px}
.q{display:flex;flex-direction:column;align-items:flex-start;gap:3px;height:226px;padding:14px 13px 12px;background:var(--c);
border:3px solid var(--line);border-radius:18px;box-shadow:5px 5px 0 var(--line);transform:rotate(var(--t));
animation:sway 3.2s ease-in-out infinite alternate}
@keyframes sway{from{transform:rotate(calc(var(--t) - 1.5deg))}to{transform:rotate(calc(var(--t) + 1.5deg))}}
.ic{display:flex;align-items:center;justify-content:center;width:44px;height:44px;margin-bottom:7px;background:var(--paper);
border:2.5px solid var(--line);border-radius:50%}
.ic svg{width:22px;height:22px;fill:none;stroke:var(--ink);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.q h3{font:400 19px/1.05 var(--display)}
.q .k{font:700 9.5px var(--mono);text-transform:uppercase;letter-spacing:.08em}
.q .hook{margin-top:5px;font-size:12.5px;font-weight:600;line-height:1.3}
"""

HOBBIES = [
    ("Gaming", "PC · PS5", "Cyberpunk 2077, Hogwarts Legacy, Spider-Man — the ones I keep going back to.",
     '<rect x="2" y="7" width="20" height="11" rx="5"/><path d="M7 10.5v4M5 12.5h4"/><circle cx="15.5" cy="11.5" r=".8"/><circle cx="18" cy="14" r=".8"/>'),
    ("Vibe coding", "No ticket · No deadline", "Code with no acceptance criteria, written to find out whether an idea holds.",
     '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M7 10l3 2.5L7 15M12 15h5"/>'),
    ("Building PCs", "Spec · Budget · Airflow", "From a requirement and a budget to a machine that boots — and glows.",
     '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>'),
    ("Lego", "One bag at a time", "Hours with the manual open, every piece where the page says. Worth every minute.",
     '<rect x="3" y="10" width="18" height="10" rx="1.5"/><rect x="6" y="6" width="4" height="4" rx="1"/><rect x="14" y="6" width="4" height="4" rx="1"/>'),
    ("Chess", "Learnt as a kid", "The game that taught me how to concentrate.",
     '<circle cx="12" cy="6" r="2.5"/><path d="M9.5 10h5M10.5 10l-1 7h5l-1-7M7 20h10"/>'),
    ("Cooking", "Speciality · Mutton biryani", "Hard to do every day. A joy when I do. Best of all when it is for someone else.",
     '<path d="M3 11h18a9 9 0 0 1-18 0z"/><path d="M9 7.5c0-1.5 1.5-1.5 1.5-3M13.5 7.5c0-1.5 1.5-1.5 1.5-3"/>'),
    ("Anime", "Currently · One Piece", "I never understood it. Then I started One Piece.",
     '<path d="M12 3l2.4 5.6L20 11l-5.6 2.4L12 19l-2.4-5.6L4 11l5.6-2.4z"/>'),
    ("Collecting", "Model cars · Collectibles", "Model cars, and the collectibles that earn a place beside them.",
     '<path d="M3 15v-3l2.5-4.5h9L18 11l3 1v3z"/><circle cx="7" cy="16" r="2"/><circle cx="16.5" cy="16" r="2"/>'),
]


def bonus():
    tilts = [-1.5, 1.2, -1, 1.5, 1.2, -1.4, 1, -1.2]
    cards = "".join(
        f'<div class="q" style="--c:var(--c{i % 5 + 1});--t:{tilts[i]}deg;animation-delay:{-i * 0.8:.1f}s">'
        f'<span class="ic">{icon(paths)}</span><h3>{name}</h3><p class="k">{kicker}</p><p class="hook">{hook}</p></div>'
        for i, (name, kicker, hook, paths) in enumerate(HOBBIES)
    )
    return head("Bonus tracks", "Off the clock, <mark>still grooving.</mark>") + f'<div class="quests">{cards}</div>'


# ---------------------------------------------------------------- encore, buttons, footer

ENCORE_CSS = """
.encore{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:var(--c3)}
.burst{position:absolute;left:50%;top:50%;width:1400px;height:1400px;margin:-700px 0 0 -700px;
background:repeating-conic-gradient(rgba(255,123,28,.55) 0 5deg,transparent 5deg 10deg);
-webkit-mask:radial-gradient(closest-side,#000 10%,transparent 70%);mask:radial-gradient(closest-side,#000 10%,transparent 70%);
animation:spin 120s linear infinite}
.encore>p,.encore>h2{position:relative}
.encore .eyebrow{color:var(--ink)}
.encore .display{font-size:104px}
.encore .lede{margin-top:10px;color:var(--ink);font-weight:600}
"""

BUTTON_CSS = """
.btn{position:absolute;left:0;top:0;right:7px;bottom:7px;display:flex;align-items:center;justify-content:center;
font:800 22px var(--sans);background:var(--c);border:3px solid var(--line);border-radius:999px;box-shadow:6px 6px 0 var(--line)}
"""

FOOTER_CSS = """
.foot{padding:16px 0 22px;color:var(--paper);text-align:center;background:var(--ink)}
.foot::after{opacity:.08}
.big{display:flex;width:max-content;font:400 72px/1.15 var(--display);color:var(--c1);white-space:nowrap;animation:marquee 30s linear infinite}
.big span{padding-right:.5ch}
.foot p{margin-top:8px;font:700 11.5px var(--mono);text-transform:uppercase;letter-spacing:.06em}
"""


def footer():
    run = "<span>Ashwath FM ✺ signing off ✺ Ashwath FM ✺ signing off ✺ </span>"
    return (f'<div class="big">{run}{run}</div>'
            "<p>Bachelor of Computer Applications · Mangalore University · 2014 — 2017</p>"
            "<p>Ashwath Chandra · Broadcast from Bengaluru, India</p>")


PANELS = {
    "hero": (840, 770, "p hero", HERO_CSS, hero()),
    "hits": (840, 320, "p dots hits", HITS_CSS, hits()),
    "tracks": (840, 1140, "p", TRACKS_CSS, tracks()),
    "b-sides": (840, 760, "p dots", BSIDES_CSS, bsides()),
    "jukebox": (840, 690, "p", JUKEBOX_CSS, jukebox()),
    "bonus": (840, 716, "p dots", BONUS_CSS, bonus()),
    "encore": (840, 280, "p encore", ENCORE_CSS,
               '<div class="burst"></div><p class="eyebrow">Encore</p><h2 class="display">Let’s <mark>jam.</mark></h2>'
               '<p class="lede">Test infrastructure, bench farms, or a good biryani debate: the inbox is open.</p>'),
    "btn-email": (270, 70, "b", BUTTON_CSS, '<div class="btn" style="--c:var(--c1)">iam@ashwath.me</div>'),
    "btn-linkedin": (180, 70, "b", BUTTON_CSS, '<div class="btn" style="--c:var(--c2)">LinkedIn ↗</div>'),
    "btn-site": (190, 70, "b", BUTTON_CSS, '<div class="btn" style="--c:var(--c4)">Portfolio ↗</div>'),
    "footer": (840, 170, "p foot", FOOTER_CSS, footer()),
}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, (w, h, cls, css, body) in PANELS.items():
        doc = svg(w, h, cls, css, body)
        ET.fromstring(doc)  # a malformed SVG shows up on GitHub as a broken image, so fail here instead
        (OUT / f"{name}.svg").write_text(doc)
        print(f"assets/{name}.svg  {len(doc) // 1024} KB")
