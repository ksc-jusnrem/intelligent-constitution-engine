# Deploying on constitution.codes

The engine is a static site: `index.html` + `data.js` (and optionally `data.json`). No server, no database, no build step. Any static host works.

## Option A — Cloudflare Pages (free, fast, recommended)

1. Push this folder to a GitHub repo (e.g. `ksc-jusnrem/constitution-engine`).
2. Cloudflare dashboard → Workers & Pages → Create → Pages → connect the repo.
   Build command: *(none)* · Output directory: `/`
3. Custom domains → add `constitution.codes` (and `www.constitution.codes`).
4. If the domain's DNS is already on Cloudflare, the records are added automatically; otherwise point the domain's nameservers at Cloudflare or add the CNAME it shows you.

## Option B — Netlify

1. Drag-and-drop this folder at app.netlify.com/drop — live in seconds.
2. Site settings → Domain management → add custom domain `constitution.codes`.
3. At your registrar, create:
   - `A` record `@` → `75.2.60.5` (Netlify load balancer), or use Netlify DNS
   - `CNAME` record `www` → `<yoursite>.netlify.app`
4. Netlify provisions HTTPS via Let's Encrypt automatically.

## Option C — GitHub Pages

1. Push to a repo, Settings → Pages → deploy from branch `main`, folder `/`.
2. Add `constitution.codes` as the custom domain (creates a `CNAME` file).
3. At your registrar: `A` records for `@` → 185.199.108.153 / .109. / .110. / .111.153, `CNAME` `www` → `<user>.github.io`.

## Option D — Any VPS / shared hosting

Upload the folder to the web root. That's it. Example nginx block:

```nginx
server {
  listen 443 ssl http2;
  server_name constitution.codes www.constitution.codes;
  root /var/www/jusnrem-engine;
  index index.html;
  gzip on; gzip_types application/javascript application/json text/html;
}
```

## Local preview

```bash
cd jusnrem-engine
python3 -m http.server 8080
# open http://localhost:8080
```

(Opening `index.html` directly by double-click also works, since the data ships as `data.js`, not a fetched JSON.)

## Performance note

`data.js` is ~770 KB raw and ~180 KB with gzip/brotli, which every host above applies automatically. First load is one round trip; everything after that is instant and offline-capable.
