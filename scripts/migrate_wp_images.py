"""One-off: copy images referenced by migrated posts from the WordPress.com CDN into public/images/wp/."""
import pathlib, re, urllib.parse, urllib.request

POSTS = pathlib.Path("src/content/blog")
OUT = pathlib.Path("public/images/wp")
URL_RE = re.compile(r"https?://mohamedsahbicom\.files\.wordpress\.com/[^\s)\"']+")
OLD_SITE_RE = re.compile(r"https?://mohamedsahbicom\.wordpress\.com(/\d{4}/\d{2}/\d{2}/[^\s)\"']+)")

failed = []
for post in sorted(POSTS.glob("*.md")):
    text = post.read_text()
    new = OLD_SITE_RE.sub(r"\1", text)
    for url in sorted(set(URL_RE.findall(text))):
        path = urllib.parse.urlsplit(url).path.lstrip("/")  # e.g. 2019/12/octocat.png (drops ?w=800)
        dest = OUT / urllib.parse.unquote(path)
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                req = urllib.request.Request(url.split("?")[0], headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    dest.write_bytes(r.read())
                print("ok  ", url)
            except Exception as e:
                failed.append(url)
                print("FAIL", url, e)
                continue
        new = new.replace(url, "/images/wp/" + path)
    if new != text:
        post.write_text(new)

print(f"failed: {len(failed)}")
