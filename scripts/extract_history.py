#!/usr/bin/env python3
"""
KSC.JUSNREM - Constitutional Intelligence Engine
Data extractor: walks the full git history of the version-controlled
Constitution of Pakistan and emits a single JSON dataset that powers
the static web interface on jusnrem.digital.

Output schema (data.json):
{
  "meta":    { name, generated, source, commitCount, articleCount },
  "commits": [ { i, hash, date, president, title, summary,
                 changes: [{file, status}] } ],            # chronological
  "articles": { "article-001": {
                  "num": "1", "title": "...",
                  "versions": [ { "commit": <index>, "text": "..." } ] },
                "preamble": {...} }
}
"""
import json, re, subprocess, sys, datetime

import os
REPO = sys.argv[1] if len(sys.argv) > 1 else "/tmp/legalize-pk"
OUT  = sys.argv[2] if len(sys.argv) > 2 else os.path.join("data", "constitution", "data.json")

def git(*args):
    return subprocess.run(["git", "-C", REPO, *args],
                          capture_output=True, encoding="utf-8", check=True).stdout

# ---- 1. commits, oldest first -------------------------------------------
rows = git("log", "--reverse", "--format=%H|%ad|%an|%s", "--date=short").strip().splitlines()
commits = []
for i, row in enumerate(rows):
    h, date, author, subject = row.split("|", 3)
    # subject looks like "Eighteenth Amendment 2010-04-19 Asif Ali Zardari"
    title = re.sub(r"\s+\d{4}-\d{2}-\d{2}.*$", "", subject).strip()
    commits.append({"i": i, "hash": h, "date": date,
                    "president": author, "title": title,
                    "summary": "", "changes": []})

# ---- 2. per-commit file changes + amendment summaries --------------------
for c in commits:
    status = git("show", "--name-status", "--format=", c["hash"]).strip().splitlines()
    for line in status:
        if not line.strip():
            continue
        parts = line.split("\t")
        st, path = parts[0][0], parts[-1]
        if path.startswith("federal-constitution/"):
            c["changes"].append({"file": path.split("/")[-1].replace(".md", ""),
                                 "status": st})
        elif path.startswith("federal-ammendment-summaries/") and st in "AM":
            c["summary"] = git("show", f'{c["hash"]}:{path}').strip()

# ---- 3. article version histories ----------------------------------------
META_TABLE = re.compile(r"^\s*\|.*\|\s*$")

def parse_article(raw):
    """Split the leading markdown metadata table from the body text."""
    title = None
    body_lines, in_table, table_done = [], False, False
    for ln in raw.splitlines():
        if not table_done and META_TABLE.match(ln):
            in_table = True
            m = re.match(r"\|\s*Title\s*\|\s*(.+?)\s*\|", ln)
            if m:
                title = m.group(1).strip()
            continue
        if in_table and not META_TABLE.match(ln):
            table_done = True
        body_lines.append(ln)
    return title, "\n".join(body_lines).strip()

articles = {}
files = sorted({ch["file"] for c in commits for ch in c["changes"]})
for f in files:
    path = f"federal-constitution/{f}.md"
    m = re.match(r"article-0*(\d+[A-Za-z]*)", f)
    num = m.group(1) if m else ("Preamble" if f == "preamble" else f)
    versions, latest_title = [], None
    for c in commits:
        touched = next((ch for ch in c["changes"] if ch["file"] == f), None)
        if not touched:
            continue
        if touched["status"] == "D":
            versions.append({"commit": c["i"], "text": "[Omitted]"})
            continue
        raw = git("show", f'{c["hash"]}:{path}')
        title, body = parse_article(raw)
        if title:
            latest_title = title
        versions.append({"commit": c["i"], "text": body})
    articles[f] = {"num": num, "title": latest_title or f, "versions": versions}

# ---- 4. write -------------------------------------------------------------
data = {
    "meta": {
        "name": "KSC.JUSNREM - Constitutional Intelligence Engine",
        "domain": "jusnrem.digital",
        "generated": datetime.date.today().isoformat(),
        "source": "https://github.com/ksc-jusnrem/legalize-pk",
        "commitCount": len(commits),
        "articleCount": len(articles),
    },
    "commits": commits,
    "articles": articles,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fp:
    json.dump(data, fp, ensure_ascii=False, separators=(",", ":"))

out_js = OUT.replace(".json", ".js")
with open(out_js, "w", encoding="utf-8") as fp:
    fp.write("/* Auto-generated from git history. Do not edit manually. */\n")
    fp.write("window.CONSTITUTION_DATA = ")
    json.dump(data, fp, ensure_ascii=False, separators=(",", ":"))
    fp.write(";\n")

n_versions = sum(len(a["versions"]) for a in articles.values())
print(f"commits={len(commits)} articles={len(articles)} versions={n_versions}")
print(f"wrote {OUT}")
print(f"wrote {out_js}")
