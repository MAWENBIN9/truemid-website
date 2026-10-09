# -*- coding: utf-8 -*-
"""Generate cases.html, case detail pages, blog.html, blog articles for TrueMid site."""
import io, os

ROOT = r"C:\Users\马文彬\WorkBuddy\Claw\Claw\website"
SITE = "https://www.truemidmanufacturing.com"

def header(depth, active):
    """depth 0 = site root, 1 = subdirectory (cases/, blog/)"""
    p = "../" * depth
    nav_items = [
        ("Services", p + "index.html#services", "services"),
        ("Case Studies", p + "cases.html", "cases"),
        ("Blog", p + "blog.html", "blog"),
        ("How It Works", p + "index.html#how", "how"),
        ("FAQ", p + "index.html#faq", "faq"),
        ("About", p + "index.html#about", "about"),
    ]
    nav = "\n".join(
        '    <a href="%s"%s>%s</a>' % (href, ' class="active"' if key == active else "", label)
        for label, href, key in nav_items
    )
    return f'''<a href="{p}index.html" class="logo">
    <span class="logo-icon">TM</span>
    TrueMid Manufacturing
  </a>
  <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
  <nav id="nav">
{nav}
    <a href="{p}index.html#contact" class="btn btn-primary">Get a Quote</a>
  </nav>'''

def footer(depth):
    p = "../" * depth
    return f'''<footer>
<div class="container">
  <div class="footer-grid" style="grid-template-columns:2fr 1fr 1fr 1fr">
    <div>
      <div class="logo"><span class="logo-icon">TM</span> TrueMid Manufacturing</div>
      <p style="color:rgba(255,255,255,.5)">Precision prototypes &amp; low-volume parts, delivered worldwide in 5&ndash;14 days. A US-registered company (New Mexico).</p>
    </div>
    <div>
      <h4>Services</h4>
      <a href="{p}index.html#services">3D Printing</a><br>
      <a href="{p}index.html#services">CNC Machining</a><br>
      <a href="{p}index.html#services">Vacuum Casting</a><br>
      <a href="{p}index.html#services">Injection Molding</a><br>
      <a href="{p}index.html#services">All Services &rarr;</a>
    </div>
    <div>
      <h4>Company</h4>
      <a href="{p}cases.html">Case Studies</a><br>
      <a href="{p}blog.html">Blog</a><br>
      <a href="{p}index.html#about">About Us</a><br>
      <a href="{p}index.html#how">How It Works</a><br>
      <a href="{p}index.html#contact">Request Quote</a>
    </div>
    <div>
      <h4>Contact</h4>
      <a href="mailto:bruce@truemidmanufacturing.com">Email Us</a><br>
      <a href="https://wa.me/8615291861855?text=Hello%2C%20I%20need%20a%20quote%20for%20manufacturing%20services" target="_blank" rel="noopener">WhatsApp</a><br>
      <a href="{p}index.html#contact">Get a Quote</a>
    </div>
  </div>
  <div class="footer-bottom">
    &copy; 2026 TrueMid Manufacturing LLC. All rights reserved. | US-Registered LLC (New Mexico) &middot; Global Manufacturing &amp; Delivery
    <div class="footer-legal">
      <a href="{p}privacy.html">Privacy Policy</a>
      <a href="{p}terms.html">Terms of Service</a>
    </div>
  </div>
</div>
</footer>'''

def page(depth, title, desc, canonical, active, body, schema_extra=""):
    p = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔧</text></svg>">
<link rel="stylesheet" href="{p}assets/style.css">
{schema_extra}</head>
<body>
<a href="https://wa.me/8615291861855?text=Hello%2C%20I%20need%20a%20quote%20for%20manufacturing%20services" class="wa-float" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <span class="wa-icon">&#128172;</span> WhatsApp
</a>
<header id="header">
<div class="header-inner">
{header(depth, active)}
</div>
</header>
{body}
{footer(depth)}
<script>
function toggleMenu(){{document.getElementById('nav').classList.toggle('open')}}
document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>document.getElementById('nav').classList.remove('open')));
window.addEventListener('scroll',()=>document.getElementById('header').classList.toggle('scrolled',window.scrollY>10));
const observer=new IntersectionObserver((e)=>{{e.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('visible');observer.unobserve(e.target)}}}})}},{{threshold:0.15}});
document.querySelectorAll('.fade-in').forEach(el=>observer.observe(el));
</script>
</body>
</html>'''

def breadcrumb_json(items):
    import json
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                          "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                               "name": n, "item": u} for i, (n, u) in enumerate(items)]},
                          ensure_ascii=False, indent=2)
            + '\n</script>')

def article_json(headline, desc, date, url, img):
    import json
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@type": "Article",
                          "headline": headline, "description": desc, "datePublished": date,
                          "dateModified": date, "author": {"@type": "Organization", "name": "TrueMid Manufacturing LLC"},
                          "publisher": {"@type": "Organization", "name": "TrueMid Manufacturing LLC"},
                          "mainEntityOfPage": url, "image": img}, ensure_ascii=False, indent=2)
            + '\n</script>')

# ================= CASES DATA =================
CASES = [
 dict(slug="medical-device-enclosure", tag="SLA 3D Printing", img="case-sla.jpg",
   title="Medical Device Enclosure — SLA Clear Resin Prototype",
   short="Medical Device Enclosure",
   specs=["Clear Resin","±0.1mm","Polished + Painted","12 units","7 days"],
   specline="Material: Clear Resin · Tolerance: ±0.1mm · Finish: Polished + Painted · Delivered in 7 days · 12 units",
   meta_desc="SLA clear resin medical device enclosure prototype: 12 units, ±0.1mm tolerance, polished and painted, delivered worldwide in 7 days. TrueMid Manufacturing case study.",
   body="""
<p>A US medical device startup needed presentation-grade enclosures for an investor demo and preliminary fitting tests of internal PCB assemblies. The parts required light-transmissive windows, tight fits around snap features, and a surface finish suitable for painting in the client's brand color.</p>
<h2>The Challenge</h2>
<ul>
<li>Optically clear windows blended into a matte body &mdash; two finishes on one part</li>
<li>Snap-fit features that had to survive repeated assembly without visible wear</li>
<li>Hard deadline: investor demo in under two weeks, including international shipping</li>
</ul>
<h2>Our Solution</h2>
<p>We printed the enclosures in high-resolution clear resin, masking the window zones before priming and painting the body sections. After curing, the window areas were polished to optical clarity, and snap features were printed at 0.05mm-adjusted offsets based on a single test coupon &mdash; avoiding a wasted iteration.</p>
<h2>Process &amp; Specs</h2>
<table>
<tr><th>Item</th><th>Detail</th></tr>
<tr><td>Process</td><td>SLA (stereolithography), 50&micro;m layers</td></tr>
<tr><td>Material</td><td>Clear resin (ABS-like)</td></tr>
<tr><td>Tolerance</td><td>&plusmn;0.1mm on critical fits</td></tr>
<tr><td>Finish</td><td>Masked, primed, painted, windows polished</td></tr>
<tr><td>Quantity</td><td>12 units</td></tr>
<tr><td>Lead time</td><td>7 days door-to-door (DHL)</td></tr>
</table>
<h2>Outcome</h2>
<p>All 12 enclosures arrived 5 days before the demo. The client used the same files, unchanged, for a second batch &mdash; proof that the first iteration was right. The snap fits survived 50+ assembly cycles during testing.</p>"""),
 dict(slug="aerospace-bracket", tag="CNC Machining", img="case-cnc.jpg",
   title="Aerospace Bracket Assembly — CNC 6061-T6 Aluminum",
   short="Aerospace Bracket Assembly",
   specs=["6061-T6 Aluminum","±0.05mm","Anodized Black","25 units","12 days"],
   specline="Material: 6061-T6 Aluminum · Tolerance: ±0.05mm · Finish: Anodized Black · Delivered in 12 days · 25 units",
   meta_desc="CNC machined 6061-T6 aerospace brackets: ±0.05mm tolerance, black anodized, 25 units delivered in 12 days. Precision CNC machining case study by TrueMid Manufacturing.",
   body="""
<p>A European aerospace subsystem supplier needed a small batch of mounting brackets for a test rig. The parts combined a thin-wall pocketed web with precision bores for bearing dowels &mdash; classic 3+2 axis CNC work, but with a tolerance stack that left no room for error.</p>
<h2>The Challenge</h2>
<ul>
<li>&plusmn;0.05mm positional tolerance on dowel bores, referenced to a common datum</li>
<li>Wall sections down to 1.2mm &mdash; machining distortion had to be controlled</li>
<li>Type II black anodize with masked threaded holes</li>
</ul>
<h2>Our Solution</h2>
<p>We roughed the parts leaving 0.3mm stock, stress-relieved them, then finished in a second setup to keep distortion out of the final geometry. Bores were finish-bored in one setup referenced to the datum face. Threaded holes were masked before anodizing to guarantee bolt fit.</p>
<h2>Process &amp; Specs</h2>
<table>
<tr><th>Item</th><th>Detail</th></tr>
<tr><td>Process</td><td>3-axis CNC milling, 2 setups + stress relief</td></tr>
<tr><td>Material</td><td>6061-T6 aluminum</td></tr>
<tr><td>Tolerance</td><td>&plusmn;0.05mm on datum bores</td></tr>
<tr><td>Finish</td><td>Type II black anodize, masked threads</td></tr>
<tr><td>Quantity</td><td>25 units</td></tr>
<tr><td>Lead time</td><td>12 days door-to-door (DHL)</td></tr>
</table>
<h2>Outcome</h2>
<p>All 25 brackets passed the client's incoming inspection, including a CMM spot-check on the datum bores. The rig was assembled on schedule with zero rework requests.</p>"""),
 dict(slug="electronics-housing", tag="Vacuum Casting", img="case-vacuum.jpg",
   title="Electronics Housing — Vacuum Cast ABS-like PU, Color Matched",
   short="Electronics Housing",
   specs=["PU Resin (ABS-like)","Color Matched","30 units","10 days"],
   specline="Material: PU Resin (ABS-like) · Color-matched · 30 units · Delivered in 10 days",
   meta_desc="Vacuum casting case study: 30 color-matched ABS-like electronics housings from silicone tooling in 10 days. Low-volume production without injection mold cost.",
   body="""
<p>A consumer electronics company needed 30 housings for a pilot user study &mdash; injection molding tooling was not justified, but 3D printed parts would not survive the drop tests or look right next to the final product. Vacuum casting was the natural bridge.</p>
<h2>The Challenge</h2>
<ul>
<li>Exact brand color match (RAL reference) with matte texture</li>
<li>Parts had to survive a 1-meter drop test onto concrete</li>
<li>10-day total deadline including overseas shipping</li>
</ul>
<h2>Our Solution</h2>
<p>We machined the master pattern for best surface quality, then cast in ABS-like PU with pigment matched to the client's RAL reference. The first article was photographed and approved before the batch ran. Two silicone molds ran in parallel to hit the schedule.</p>
<h2>Process &amp; Specs</h2>
<table>
<tr><th>Item</th><th>Detail</th></tr>
<tr><td>Process</td><td>Vacuum casting from CNC master pattern</td></tr>
<tr><td>Material</td><td>PU resin, ABS-like, 78 Shore D</td></tr>
<tr><td>Color</td><td>Pigment-matched to client RAL reference, matte</td></tr>
<tr><td>Quantity</td><td>30 units</td></tr>
<tr><td>Lead time</td><td>10 days door-to-door (DHL)</td></tr>
</table>
<h2>Outcome</h2>
<p>All 30 housings passed the drop test at pilot assembly. The client later returned for a 150-unit bridge batch while their production tooling was being cut &mdash; same molds, zero retooling cost.</p>"""),
 dict(slug="drone-frame-component", tag="SLS Printing", img="case-sls.jpg",
   title="Drone Frame Component — SLS PA12 with Internal Lattice",
   short="Drone Frame Component",
   specs=["PA12 Nylon","Internal Lattice","Dyed Black","8 units","9 days"],
   specline="Material: PA12 Nylon · Complex internal lattice · Dyed black · Delivered in 9 days · 8 units",
   meta_desc="SLS 3D printed PA12 drone frame arms with internal lattice structure: 42% lighter than solid, 8 units in 9 days. Design-for-additive case study.",
   body="""
<p>A drone startup wanted to shave weight from a frame arm without sacrificing stiffness. Solid PA12 was too heavy; hollow shells printed on other processes lacked crush resistance. The answer was an internal lattice only SLS can produce &mdash; no support removal needed.</p>
<h2>The Challenge</h2>
<ul>
<li>Reduce mass by 40%+ while keeping torsional stiffness</li>
<li>Geometry impossible to mold or machine</li>
<li>Matte black finish that didn't scream &ldquo;prototype&rdquo;</li>
</ul>
<h2>Our Solution</h2>
<p>Working from the client's outer envelope, we generated a gyroid lattice infill with denser zones at the mounting bosses. After SLS printing in PA12, the parts were bead-blasted and dyed black for a uniform, production-like surface.</p>
<h2>Process &amp; Specs</h2>
<table>
<tr><th>Item</th><th>Detail</th></tr>
<tr><td>Process</td><td>SLS (selective laser sintering)</td></tr>
<tr><td>Material</td><td>PA12 nylon</td></tr>
<tr><td>Structure</td><td>Gyroid lattice, graded density at bosses</td></tr>
<tr><td>Finish</td><td>Bead-blasted, dyed black</td></tr>
<tr><td>Weight saving</td><td>42% vs solid equivalent</td></tr>
<tr><td>Quantity</td><td>8 units</td></tr>
<tr><td>Lead time</td><td>9 days door-to-door (DHL)</td></tr>
</table>
<h2>Outcome</h2>
<p>Flight testing confirmed stiffness targets were met at 42% lower mass. The dyed finish was good enough that the client photographed these exact arms for their marketing material.</p>"""),
 dict(slug="heat-exchanger-core", tag="Metal 3D Printing", img="case-metal.jpg",
   title="Heat Exchanger Core — DMLS 316L with Conformal Channels",
   short="Heat Exchanger Core",
   specs=["316L Stainless","Conformal Channels","Post-machined Threads","3 units","14 days"],
   specline="Material: 316L Stainless · Conformal channels · Post-machined threads · Delivered in 14 days · 3 units",
   meta_desc="DMLS metal 3D printed 316L heat exchanger core with conformal cooling channels and post-machined NPT threads: 3 units in 14 days. Metal additive manufacturing case study.",
   body="""
<p>An energy systems engineering firm needed compact heat exchanger cores with conformal channels that followed the contour of the hot face &mdash; geometry that cannot be drilled or brazed. Traditional manufacturing would have meant a welded assembly of 9 parts with leak risk at every joint.</p>
<h2>The Challenge</h2>
<ul>
<li>Conformal internal channels, 3mm bore, smooth enough for fluid flow</li>
<li>NPT threads had to seal against fittings at 10 bar</li>
<li>Pressure-test-worthy parts &mdash; not display models</li>
</ul>
<h2>Our Solution</h2>
<p>We printed the cores as single DMLS parts in 316L stainless, orienting the channels to minimize powder traps and stair-stepping inside the bore. Ports were left with 1mm stock, then finish-machined and NPT-tapped for guaranteed thread sealing. Each core was pressure tested before shipment.</p>
<h2>Process &amp; Specs</h2>
<table>
<tr><th>Item</th><th>Detail</th></tr>
<tr><td>Process</td><td>DMLS metal 3D printing + CNC post-machining</td></tr>
<tr><td>Material</td><td>316L stainless steel</td></tr>
<tr><td>Internal features</td><td>Conformal channels, 3mm bore</td></tr>
<tr><td>Post-processing</td><td>Finish-machined ports, NPT threads, pressure test</td></tr>
<tr><td>Quantity</td><td>3 units</td></tr>
<tr><td>Lead time</td><td>14 days door-to-door (DHL)</td></tr>
</table>
<h2>Outcome</h2>
<p>All three cores held 10 bar without weeping. Thermal testing showed a 23% improvement over the client's previous brazed design &mdash; the geometry advantage was real, and it only exists because of additive manufacturing.</p>"""),
 dict(slug="consumer-electronics-housing", tag="Injection Molding", img="case-injection.jpg",
   title="Consumer Electronics Housing — ABS+PC Injection Molding",
   short="Consumer Electronics Housing",
   specs=["ABS+PC","Steel Tooling","SPI-B1 Texture","2,000 units","25 days"],
   specline="Material: ABS+PC · Steel tooling · Texture SPI-B1 · Delivered in 25 days · 2,000 units",
   meta_desc="Injection molded ABS+PC consumer electronics housings: steel tooling, SPI-B1 texture, 2,000 units in 25 days. Low-volume injection molding case study.",
   body="""
<p>A hardware startup moving from prototype to first production run needed 2,000 housings &mdash; too many for casting, too few to justify domestic tooling quotes. We cut steel tooling in China and ran the full batch in under four weeks, including shipping.</p>
<h2>The Challenge</h2>
<ul>
<li>Class A cosmetic surface with SPI-B1 matte texture</li>
<li>Tight warp control on a long, thin boss line</li>
<li>Startup cash flow &mdash; tooling cost had to stay lean without quality risk</li>
</ul>
<h2>Our Solution</h2>
<p>We ran moldflow analysis on the gate locations, added two flow leaders to correct predicted warp, and cut a single-cavity steel tool with a texture-ready A-side surface. T1 samples were approved with zero dimensional changes; only texture depth was fine-tuned between T1 and production.</p>
<h2>Process &amp; Specs</h2>
<table>
<tr><th>Item</th><th>Detail</th></tr>
<tr><td>Process</td><td>Injection molding, single-cavity steel tool</td></tr>
<tr><td>Material</td><td>ABS+PC blend (flame retardant grade)</td></tr>
<tr><td>Surface</td><td>SPI-B1 matte texture, A-side cosmetic</td></tr>
<tr><td>Analysis</td><td>Moldflow simulation, warp-corrected gates</td></tr>
<tr><td>Quantity</td><td>2,000 units</td></tr>
<tr><td>Lead time</td><td>25 days tool-to-parts door-to-door (DHL)</td></tr>
</table>
<h2>Outcome</h2>
<p>First-article approval on T1 with no dimensional revisions. The 2,000-unit batch shipped complete with AQL sampling inspection reports, and the tool remains in our facility for the client's next reorder &mdash; lead time drops to 12 days on repeat runs.</p>"""),
]

# ================= CASES LISTING PAGE =================
cards = "\n".join(f'''
    <a class="case-card fade-in" href="{c['slug']}.html">
      <div class="case-img">
        <img src="../images/{c['img']}" alt="{c['short']}" loading="lazy" width="600" height="400">
      </div>
      <div class="case-body">
        <span class="tag">{c['tag']}</span>
        <h3>{c['short']}</h3>
        <p class="specs">{c['specline']}</p>
      </div>
    </a>''' for c in CASES)

cases_body = f'''<!-- ===== PAGE HERO ===== -->
<section class="page-hero">
<div class="container">
  <div class="breadcrumb"><a href="../index.html">Home</a><span>/</span>Case Studies</div>
  <h1>Manufacturing Case Studies</h1>
  <p>Real projects, real specs, real deadlines &mdash; from single SLA prototypes to 2,000-unit injection molded production runs. Every case below shipped door-to-door worldwide.</p>
</div>
</section>

<!-- ===== CASE LIST ===== -->
<section>
<div class="container">
  <div class="cases-grid">{cards}
  </div>
</div>
</section>

<!-- ===== CTA ===== -->
<section class="cta">
<div class="container fade-in">
  <h2>Have a Part Like These?</h2>
  <p>Send your files and get a detailed quote within 24 hours &mdash; process recommendation included, free.</p>
  <a href="../index.html#contact" class="btn btn-orange">Request a Quote &rarr;</a>
</div>
</section>'''

# ================= CASE DETAIL PAGES =================
os.makedirs(os.path.join(ROOT, "cases"), exist_ok=True)
for c in CASES:
    chips = "".join(f"\n      <li>{s}</li>" for s in c["specs"])
    body = f'''<!-- ===== PAGE HERO ===== -->
<section class="page-hero">
<div class="container">
  <div class="breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../cases.html">Case Studies</a><span>/</span>{c['short']}</div>
  <h1>{c['title']}</h1>
</div>
</section>

<!-- ===== CASE BODY ===== -->
<section>
<div class="container">
  <div class="detail-wrap fade-in">
    <ul class="detail-meta">{chips}
    </ul>
    <div class="detail-hero-img">
      <img src="../images/{c['img']}" alt="{c['title']}" width="1200" height="800">
    </div>
    <div class="detail-body">
{c['body']}
    </div>
    <div class="detail-cta">
      <h2>Need a Part Like This?</h2>
      <p>Send your STEP/STL files &mdash; we'll recommend the best process and quote within 24 hours.</p>
      <a href="../index.html#contact" class="btn btn-orange">Request a Quote &rarr;</a>
    </div>
  </div>
</div>
</section>'''
    schema = breadcrumb_json([("Home", SITE + "/"), ("Case Studies", SITE + "/cases.html"),
                              (c["short"], SITE + "/cases/" + c["slug"] + ".html")])
    html = page(1, c["title"] + " | TrueMid Manufacturing", c["meta_desc"],
                SITE + "/cases/" + c["slug"] + ".html", "cases", body, schema)
    io.open(os.path.join(ROOT, "cases", c["slug"] + ".html"), "w", encoding="utf-8", newline="\n").write(html)
    print("case page:", c["slug"])

# write cases.html (at root, depth 0) - regenerate with depth 0
p = ""
cards0 = cards.replace('href="', 'href="cases/').replace('src="../images/', 'src="images/')
cases_body0 = cases_body.replace('../index.html', 'index.html').replace('src="../images/', 'src="images/')
# fix double replacement in cards (cases/ already added)
cases_body0 = cases_body0.replace('href="cases/cases/', 'href="cases/')
schema0 = breadcrumb_json([("Home", SITE + "/"), ("Case Studies", SITE + "/cases.html")])
html0 = page(0, "Manufacturing Case Studies — 3D Printing, CNC, Casting & Molding | TrueMid",
             "TrueMid Manufacturing case studies: SLA prototypes, CNC aluminum brackets, vacuum cast housings, SLS lattice parts, DMLS metal cores, and injection molded production runs delivered worldwide.",
             SITE + "/cases.html", "cases", cases_body0, schema0)
io.open(os.path.join(ROOT, "cases.html"), "w", encoding="utf-8", newline="\n").write(html0)
print("cases.html written")
print("DONE part 1")
