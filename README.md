# KSC.JUSNREM — Intelligent Constitution Engine

**Live at: [jusnrem.digital](https://jusnrem.digital)**

The constitutional history of Pakistan as a living, version-controlled body of law — from the first Government of India Act (1858) and its Company-era precursors, through every framework that governed these territories, to the 1973 Constitution tracked article-by-article through all 24 enacted amendments (1974–2025), plus a section-by-section library of the great codes.

## What the engine does

**Constitutional lineage (1773–1973)** — structured dossiers for every framework that preceded the 1973 Constitution, grouped into six eras:

1. *Company rule precursors (1773–1853)* — Regulating Act 1773, Pitt's India Act 1784, Charter Acts 1813/1833/1853
2. *Crown rule (1858–1947)* — Government of India Act 1858, Indian Councils Acts 1861/1892/1909 (Morley–Minto separate electorates), Government of India Act 1919 (dyarchy), Government of India Act 1935, Lahore Resolution 1940
3. *Dominion interim framework (1947–1956)* — Indian Independence Act 1947, Pakistan (Provisional Constitution) Order 1947, Objectives Resolution 1949, dissolution of the first Constituent Assembly, the Tamizuddin litigation and the doctrine of necessity, One Unit 1955
4. *1956 Constitution → first martial law (1956–1962)* — the first Islamic Republic constitution, the 1958 abrogation, Laws (Continuance in Force) Order, State v. Dosso
5. *1962 Constitution → second martial law (1962–1969)* — Ayub's presidential constitution and Basic Democracies, the 1969 abrogation
6. *Transition (1969–1973)* — PCO 1969, Legal Framework Order 1970, the 1971 crisis and secession of East Pakistan, Asma Jilani v. Government of Punjab, Interim Constitution 1972 — ending where the engine's version-controlled history begins: 14 August 1973

**Time machine** — read the entire 1973 constitution exactly as it stood after any amendment. Articles not yet enacted at the selected era are dimmed; omitted articles are marked.

**Amendment timeline** — all 24 enacted amendments with date of assent, signing President, a plain-English summary, and a clickable list of every article each one added, amended, or omitted. (The 9th, 11th, and 15th were proposed but never passed.)

**Statute Library** — the Pakistan Penal Code, 1860 (314 sections) and the Code of Criminal Procedure, 1898 (260 sections), browsable section by section with filtering. Texts come from automated extraction of official PDF compilations; every page carries a provenance notice pointing to the Pakistan Code (pakistancode.gov.pk) for the authoritative text.

**Compare versions** — word-level diff between any two versions of any constitutional article.

**Full-text search** — across constitutional text (at the selected era), amendment summaries, pre-1973 frameworks, and statute sections.

## Files

| File | Purpose |
|---|---|
| `index.html` | The complete interface — single file, zero dependencies, no build step |
| `data.js` | The 1973-onward dataset (314 articles, 580 text versions, 25 commits) as a JS global |
| `lineage.js` | Pre-1973 constitutional lineage: 30 framework dossiers across 6 eras, 1773–1973 |
| `statutes.js` | Statute Library: PPC 1860 + CrPC 1898, 574 sections with provenance metadata |
| `data.json` | The 1973-onward dataset as raw JSON, for programmatic / AI use |
| `extract_history.py` | Regenerates `data.json` from the source git repository |
| `DEPLOY.md` | How to publish on jusnrem.digital |
| `source-data/` | Full clone of the source repo, `legalize-pk-full-history.bundle` (complete git history), and `statutes/` (raw PPC/CrPC extraction JSON) |

## Regenerating the data

When a new amendment is enacted and committed to the source repository:

```bash
git clone https://github.com/ksc-jusnrem/legalize-pk
python3 extract_history.py ./legalize-pk data.json
printf 'window.CONSTITUTION_DATA=' > data.js && cat data.json >> data.js && printf ';' >> data.js
```

The pre-1973 lineage (`lineage.js`) is hand-curated and edited directly. The statute library (`statutes.js`) is generated from the raw extraction JSON in `source-data/statutes/`.

## Data and provenance

1973-onward constitutional texts: [github.com/ksc-jusnrem/legalize-pk](https://github.com/ksc-jusnrem/legalize-pk) — one article per file, one amendment per backdated commit. Original dataset concept by Umer Butt, inspired by legalize-es. Statute texts (PPC, CrPC): automated extraction of official PDF compilations, from the Pakistani-law-RAG dataset; sections may have imperfect boundaries — consult the Pakistan Code for the authoritative text. Pre-1973 dossiers compiled from the public record of the statutes, orders and judgments described.

The legislative texts are in the public domain. Engine, interface, structure and format under the MIT License.

---
KSC.JUSNREM — Intelligent Constitution Engine · jusnrem.digital
