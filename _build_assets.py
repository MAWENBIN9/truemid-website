import re, io, os

root = r"C:\Users\马文彬\WorkBuddy\Claw\Claw\website"
idx = os.path.join(root, "index.html")
html = io.open(idx, encoding="utf-8").read()

m = re.search(r"<style>(.*?)</style>", html, re.S)
css = m.group(1)

extra = """
/* ===== Shared: inner pages ===== */
.page-hero{background:linear-gradient(135deg, var(--blue-dark) 0%, #004C85 40%, var(--blue) 100%);color:var(--white);padding:4rem 0 3rem;position:relative;overflow:hidden}
.page-hero h1{font-size:clamp(1.7rem,3.5vw,2.5rem);margin-bottom:.8rem}
.page-hero p{color:rgba(255,255,255,.85);font-size:1.05rem;max-width:640px}
.breadcrumb{font-size:.82rem;color:var(--gray-500);margin-bottom:1.2rem}
.breadcrumb a{color:var(--gray-500)}
.breadcrumb a:hover{color:var(--blue)}
.breadcrumb span{margin:0 .4rem;color:var(--gray-300)}

/* Article / case detail layout */
.detail-wrap{max-width:820px;margin:0 auto}
.detail-hero-img{border-radius:var(--radius-lg);overflow:hidden;margin:2rem 0;box-shadow:var(--shadow)}
.detail-meta{display:flex;flex-wrap:wrap;gap:.6rem;margin:0 0 2rem;padding:0;list-style:none}
.detail-meta li{font-size:.8rem;background:var(--blue-pale);color:var(--blue);padding:.25rem .7rem;border-radius:4px;font-weight:600}
.detail-body h2{font-size:1.5rem;margin:2.2rem 0 .8rem}
.detail-body h3{font-size:1.15rem;margin:1.5rem 0 .5rem}
.detail-body p{font-size:1.02rem;color:#333;margin-bottom:1.1rem}
.detail-body ul,.detail-body ol{margin:0 0 1.2rem 1.4rem;color:#333}
.detail-body li{margin-bottom:.5rem}
.detail-body table{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:.92rem}
.detail-body th{background:var(--gray-50);text-align:left;padding:.7rem .9rem;border:1px solid var(--gray-100);font-weight:700}
.detail-body td{padding:.7rem .9rem;border:1px solid var(--gray-100)}
.detail-cta{background:linear-gradient(135deg,var(--blue-dark),var(--blue));color:var(--white);border-radius:var(--radius-lg);padding:2.2rem;text-align:center;margin:3rem 0}
.detail-cta h2{color:var(--white);margin-bottom:.6rem}
.detail-cta p{color:rgba(255,255,255,.85);margin-bottom:1.4rem}
.article-date{font-size:.85rem;color:var(--gray-500);margin-bottom:2rem}

/* Blog list */
.post-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem}
.post-card{background:var(--white);border:1px solid var(--gray-100);border-radius:var(--radius-lg);padding:1.6rem;transition:all .3s;display:block;color:inherit;text-decoration:none}
.post-card:hover{box-shadow:var(--shadow-lg);transform:translateY(-2px);color:inherit}
.post-card .tag{display:inline-block;font-size:.75rem;background:var(--blue-pale);color:var(--blue);padding:.2rem .6rem;border-radius:4px;margin-bottom:.6rem;font-weight:600}
.post-card h3{font-size:1.1rem;margin-bottom:.5rem}
.post-card p{font-size:.9rem;color:var(--gray-500);margin-bottom:.8rem}
.post-card .read{font-size:.8rem;color:var(--gray-500)}

@media(max-width:768px){
  .post-list{grid-template-columns:1fr}
}
"""

os.makedirs(os.path.join(root, "assets"), exist_ok=True)
io.open(os.path.join(root, "assets", "style.css"), "w", encoding="utf-8", newline="\n").write(css + extra)

html = html.replace(m.group(0), '<link rel="stylesheet" href="assets/style.css">', 1)
io.open(idx, "w", encoding="utf-8", newline="\n").write(html)
print("CSS extracted:", len(css), "chars; extras:", len(extra))
