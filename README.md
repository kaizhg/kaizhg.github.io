# kaizhg.github.io

Kai Zhang's portfolio, built with [Astro](https://astro.build) and deployed to GitHub Pages
by `.github/workflows/deploy.yml` on every push to `main`.

## Develop

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs to dist/
```

Projects live in `src/data/projects.ts`; each one gets a page at `/work/<slug>/`.

## Case studies

Each project page renders `src/data/case-studies/<slug>.json` — an ordered list of blocks
(`text`, `image`, `loop`, `video`, `youtube`, `gallery`, `row`). Images live in
`src/assets/work/<slug>/` (Astro generates responsive WebP), videos and GIF loops in
`public/media/<slug>/`.

The Selected case studies were imported from the old Adobe Portfolio site with
`scripts/import-legacy.py`, which pulls originals from `../asset` where available.
