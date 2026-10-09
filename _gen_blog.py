# -*- coding: utf-8 -*-
"""Generate blog.html + 2 SEO seed articles."""
import io, os

ROOT = r"C:\Users\马文彬\WorkBuddy\Claw\Claw\website"
SITE = "https://www.truemidmanufacturing.com"

def header(depth, active):
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
                          "dateModified": date,
                          "author": {"@type": "Organization", "name": "TrueMid Manufacturing LLC"},
                          "publisher": {"@type": "Organization", "name": "TrueMid Manufacturing LLC"},
                          "mainEntityOfPage": url, "image": img}, ensure_ascii=False, indent=2)
            + '\n</script>')

ARTICLES = [
 dict(slug="sla-vs-fdm-vs-sls", tag="3D Printing", date="2026-10-09", date_label="Oct 9, 2026", read="8 min read",
   title="SLA vs FDM vs SLS: Which 3D Printing Process Fits Your Project?",
   excerpt="Surface finish, strength, cost, and lead time differ sharply between the three most common 3D printing processes. Here's a practical decision guide with real specs and trade-offs.",
   meta_desc="SLA vs FDM vs SLS 3D printing compared: surface finish, strength, tolerances, cost, and lead time. A practical guide to choosing the right process for prototypes and end-use parts.",
   body="""
<p>You have a part to make. The CAD file is done. Then the quoting form asks: <em>which process?</em> SLA, FDM, or SLS &mdash; and the wrong choice can double your cost or produce a part that fails in your hands. This guide breaks down the three most common 3D printing processes the way an engineer actually decides: by what the part needs to <em>do</em>.</p>

<h2>The 30-Second Answer</h2>
<table>
<tr><th></th><th>SLA (Resin)</th><th>FDM (Filament)</th><th>SLS (Nylon Powder)</th></tr>
<tr><td><strong>Best for</strong></td><td>Visual prototypes, fine detail, smooth finish</td><td>cheap functional parts, jigs, large simple parts</td><td>functional parts, complex geometry, snap fits</td></tr>
<tr><td><strong>Surface</strong></td><td>Excellent (needs light sanding at most)</td><td>Visible layer lines</td><td>Matte, sandy texture</td></tr>
<tr><td><strong>Strength</strong></td><td>Brittle-ish, UV-sensitive</td><td>Anisotropic (weak between layers)</td><td>Isotropic-ish, tough, durable</td></tr>
<tr><td><strong>Tolerance</strong></td><td>&plusmn;0.1mm</td><td>&plusmn;0.2&ndash;0.3mm</td><td>&plusmn;0.2mm</td></tr>
<tr><td><strong>Detail level</strong></td><td>0.05mm features</td><td>~0.4mm nozzle limits</td><td>0.6&ndash;0.8mm features</td></tr>
<tr><td><strong>Relative cost</strong></td><td>Medium</td><td>Lowest</td><td>Medium-high</td></tr>
<tr><td><strong>Typical lead time</strong></td><td>5&ndash;9 days</td><td>5&ndash;9 days</td><td>7&ndash;12 days</td></tr>
</table>

<h2>Choose SLA When Looks Matter</h2>
<p>SLA (stereolithography) cures liquid resin with a laser, producing the smoothest surface of any 3D printing process and details down to 0.05mm. It's the right call for:</p>
<ul>
<li><strong>Investor demos and marketing samples</strong> &mdash; parts that get painted and photographed</li>
<li><strong>Fit-checking enclosures</strong> where cosmetic surfaces meet tight gaps</li>
<li><strong>Master patterns</strong> for <a href="../cases/electronics-housing.html">vacuum casting</a>, where surface quality transfers directly to the mold</li>
<li><strong>Dental, jewelry, and medical models</strong> requiring fine feature resolution</li>
</ul>
<p>The trade-offs: SLA parts are more brittle than SLS nylon, degrade under prolonged UV exposure, and generally shouldn't be used for load-bearing functional parts. Our <a href="../cases/medical-device-enclosure.html">medical device enclosure case study</a> is a typical SLA project &mdash; presentation-grade finish, zero structural duty.</p>

<h2>Choose FDM When Cost Matters</h2>
<p>FDM (fused deposition modeling) extrudes thermoplastic filament layer by layer. It's the cheapest process and works in familiar engineering plastics: PLA, ABS, PETG, Nylon, TPU, and even carbon-filled variants.</p>
<ul>
<li><strong>Jigs, fixtures, and shop tooling</strong> &mdash; nobody cares about layer lines on a drill guide</li>
<li><strong>Large, simple parts</strong> &mdash; FDM build volumes are the biggest</li>
<li><strong>Early concept iterations</strong> where you'll print five versions before lunch</li>
<li><strong>TPU flexible parts</strong> &mdash; gaskets, bumpers, living hinges</li>
</ul>
<p>The catch: FDM parts are anisotropic &mdash; significantly weaker between layers than along them. A bracket printed flat will be strong; the same bracket printed vertically may snap along a layer line under load. Design load paths accordingly.</p>

<h2>Choose SLS When Geometry Gets Serious</h2>
<p>SLS (selective laser sintering) fuses nylon powder with a laser. Because un-sintered powder supports the part, <strong>no support structures are needed at all</strong> &mdash; which changes what's possible:</p>
<ul>
<li><strong>Internal lattices and channels</strong> impossible to print any other way (see our <a href="../cases/drone-frame-component.html">drone frame lattice case</a>)</li>
<li><strong>Snap fits and living hinges</strong> &mdash; PA12's ductility survives real assembly</li>
<li><strong>Batches of small parts</strong> &mdash; the whole build volume nests parts, so 50 pieces cost far less per part than 1</li>
<li><strong>Functional prototypes</strong> that survive drop tests and repeated handling</li>
</ul>
<p>Trade-offs: the as-printed surface is matte and slightly grainy (bead-blasting and dyeing fix this), and fine features below ~0.6mm don't survive. Tolerances run around &plusmn;0.2mm.</p>

<h2>The Decision, in Four Questions</h2>
<ol>
<li><strong>Will anyone judge this part by how it looks?</strong> Yes &rarr; SLA.</li>
<li><strong>Does it carry load, snap, or flex?</strong> Yes &rarr; SLS (or skip printing: consider <a href="../index.html#services">CNC machining</a> for metals).</li>
<li><strong>Is it a jig, a bracket, or a concept draft?</strong> Yes &rarr; FDM, save the budget.</li>
<li><strong>Do you need 20&ndash;200 units that look and feel production-grade?</strong> &rarr; Not 3D printing at all &mdash; <a href="../cases/electronics-housing.html">vacuum casting</a> from a printed or machined master.</li>
</ol>

<h2>What About Metal Parts?</h2>
<p>Metal 3D printing (DMLS/SLM) exists for geometries that machining can't reach &mdash; conformal cooling channels, internal passages, topology-optimized brackets. But for most metal parts, CNC machining is faster, cheaper, and more precise. We do both, and we'll tell you honestly which one your part needs. Our <a href="../cases/heat-exchanger-core.html">DMLS heat exchanger case</a> shows when metal additive is genuinely worth it.</p>

<h2>Still Not Sure?</h2>
<p>Send us the file. Process selection is free with every quote &mdash; we review your geometry and recommend the cheapest process that meets your requirements, not the most expensive one that fits. Typical quote turnaround: 24 hours.</p>"""),
 dict(slug="reduce-cnc-machining-costs", tag="CNC Machining", date="2026-10-09", date_label="Oct 9, 2026", read="7 min read",
   title="How to Cut CNC Machining Costs: 7 Design Tips That Actually Work",
   excerpt="CNC quotes that shock you usually trace back to design decisions, not shop rates. Seven practical design-for-manufacturing changes that reliably lower machining quotes.",
   meta_desc="7 practical ways to reduce CNC machining costs: material choice, tolerance strategy, setup reduction, corner radii, deep pockets, and quantity economics. DFM guide with real numbers.",
   body="""
<p>When a CNC machining quote comes back twice what you expected, the machine shop's hourly rate is rarely the reason. Machining cost is mostly <em>time on the machine</em> &mdash; and your design decisions control that time. These seven changes are the ones we recommend most often when reviewing customer files.</p>

<h2>1. Design Around Stock Sizes</h2>
<p>If your part is 52mm thick but plate stock comes in 50mm, you've just bought 100mm stock and paid to machine half of it away. Check standard plate and bar sizes for your material before finalizing outer dimensions. In aluminum, common plate steps are 6, 10, 12, 20, 25, 50mm. An 8mm dimension change at design time can cut material cost 40%.</p>

<h2>2. Relax Tolerances Everywhere Except Where It Matters</h2>
<p>Tolerance is not a global setting. A &plusmn;0.05mm bore on a bearing seat is engineering; the same tolerance on the outer profile of a bracket is charity to the inspection department. Every tight tolerance adds setups, slower feeds, and measurement time.</p>
<ul>
<li>Non-critical features: &plusmn;0.2mm or leave them at ISO 2768-m default</li>
<li>Fits and bores: call out &plusmn;0.05mm only on the actual fit diameter</li>
<li>Put critical dimensions in a table on the drawing &mdash; make the default obviously loose</li>
</ul>

<h2>3. Reduce Setups: Machine From One Side</h2>
<p>Every time a part flips over in the vise, you pay for re-fixturing, re-indicating, and a fresh program. A part machined complete in one setup can cost 30&ndash;50% less than the same part needing three. Design cues:</p>
<ul>
<li>Keep all machined features accessible from one direction where possible</li>
<li>Put the datum face and all critical features on the same side</li>
<li>If two sides are unavoidable, keep features grouped so it's one flip, not three</li>
</ul>
<p>Our <a href="../cases/aerospace-bracket.html">aerospace bracket case study</a> is a good example &mdash; two setups, datum-referenced, no third flip.</p>

<h2>4. Respect the Tool's Corner Radius</h2>
<p>A square internal corner requires a smaller tool, slower feeds, and more passes &mdash; or EDM. An end mill is round, so internal corners are round. Design internal corner radii at least <strong>1/3 to 1/2 the depth of the pocket</strong>, and use a single generous radius where space allows. Bonus: it makes the part lighter and looks intentional.</p>

<h2>5. Avoid Deep Pockets and Thin Walls</h2>
<p>Deep pockets need long tools that chatter, forcing conservative cuts and multi-pass roughing. Keep pocket depth under 3&ndash;4&times; tool diameter where possible. Thin walls (below ~1.5mm in aluminum) flex under cutting forces, requiring light passes and sometimes custom fixturing &mdash; both billed to you. Add ribs or increase wall thickness instead.</p>

<h2>6. Rethink Threads and Undercuts</h2>
<ul>
<li><strong>Blind tapped holes:</strong> drill depth costs time; through-holes tap faster and clean better</li>
<li><strong>Undercuts:</strong> every undercut means special tooling or a fixture change &mdash; if a feature can be reached straight in, redesign it that way</li>
<li><strong>Standard thread sizes:</strong> M3/M4/M5 and #4-#40/#10-32 tools live in every shop; exotic pitches don't</li>
</ul>

<h2>7. Use Quantity Economics Intentionally</h2>
<p>The first part absorbs programming and setup cost alone. The tenth part costs barely more than material and cycle time. Real numbers from a typical aluminum bracket:</p>
<table>
<tr><th>Quantity</th><th>Unit price index</th><th>What you're paying for</th></tr>
<tr><td>1</td><td>100%</td><td>Setup + programming dominate</td></tr>
<tr><td>5</td><td>~45%</td><td>Setup amortized across 5</td></tr>
<tr><td>25</td><td>~28%</td><td>Batch fixturing, continuous runs</td></tr>
<tr><td>100</td><td>~20%</td><td>Consider whether <a href="../cases/consumer-electronics-housing.html">injection molding</a> is now cheaper per part</td></tr>
</table>
<p>If your demand justifies it, the crossover from machining to molding usually lands somewhere between a few hundred and a few thousand units &mdash; worth calculating before every production run.</p>

<h2>The Free Version of This Advice</h2>
<p>We run DFM review on every file before quoting &mdash; no charge, no obligation. Half the time the quote drops just from fixing two or three items above. Send your STEP file and see what changes.</p>"""),
]

# blog.html listing
posts = "\n".join(f'''
    <a class="post-card fade-in" href="blog/{a['slug']}.html">
      <span class="tag">{a['tag']}</span>
      <h3>{a['title']}</h3>
      <p>{a['excerpt']}</p>
      <span class="read">{a['date_label']} &middot; {a['read']}</span>
    </a>''' for a in ARTICLES)

blog_body = f'''<!-- ===== PAGE HERO ===== -->
<section class="page-hero">
<div class="container">
  <div class="breadcrumb"><a href="index.html">Home</a><span>/</span>Blog</div>
  <h1>Manufacturing Knowledge, No Fluff</h1>
  <p>Practical guides on 3D printing, CNC machining, and low-volume production &mdash; written by the people who run the machines. New articles regularly.</p>
</div>
</section>

<!-- ===== POST LIST ===== -->
<section>
<div class="container">
  <div class="post-list">{posts}
  </div>
</div>
</section>

<!-- ===== CTA ===== -->
<section class="cta">
<div class="container fade-in">
  <h2>Have a Project in Mind?</h2>
  <p>Get a free DFM review and quote within 24 hours &mdash; process recommendation included.</p>
  <a href="index.html#contact" class="btn btn-orange">Request a Quote &rarr;</a>
</div>
</section>'''

schema0 = breadcrumb_json([("Home", SITE + "/"), ("Blog", SITE + "/blog.html")])
io.open(os.path.join(ROOT, "blog.html"), "w", encoding="utf-8", newline="\n").write(
    page(0, "Blog — 3D Printing, CNC Machining & Manufacturing Guides | TrueMid",
         "Practical manufacturing guides from TrueMid Manufacturing: choosing 3D printing processes, reducing CNC machining costs, vacuum casting, and low-volume production.",
         SITE + "/blog.html", "blog", blog_body, schema0))
print("blog.html written")

# article pages
os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
for a in ARTICLES:
    body = f'''<!-- ===== PAGE HERO ===== -->
<section class="page-hero">
<div class="container">
  <div class="breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../blog.html">Blog</a><span>/</span>{a['tag']}</div>
  <h1>{a['title']}</h1>
</div>
</section>

<!-- ===== ARTICLE BODY ===== -->
<section>
<div class="container">
  <div class="detail-wrap fade-in">
    <p class="article-date">{a['date_label']} &middot; {a['read']} &middot; by TrueMid Manufacturing</p>
    <div class="detail-body">
{a['body']}
    </div>
    <div class="detail-cta">
      <h2>Want a Quote on Your Part?</h2>
      <p>Free DFM review, process recommendation, and detailed quote within 24 hours.</p>
      <a href="../index.html#contact" class="btn btn-orange">Request a Quote &rarr;</a>
    </div>
  </div>
</div>
</section>'''
    schema = breadcrumb_json([("Home", SITE + "/"), ("Blog", SITE + "/blog.html"), (a["title"], SITE + "/blog/" + a["slug"] + ".html")]) + "\n" + article_json(
        a["title"], a["meta_desc"], a["date"], SITE + "/blog/" + a["slug"] + ".html", SITE + "/images/factory.jpg")
    io.open(os.path.join(ROOT, "blog", a["slug"] + ".html"), "w", encoding="utf-8", newline="\n").write(
        page(1, a["title"] + " | TrueMid Manufacturing", a["meta_desc"],
             SITE + "/blog/" + a["slug"] + ".html", "blog", body, schema))
    print("article:", a["slug"])

print("DONE part 2")
