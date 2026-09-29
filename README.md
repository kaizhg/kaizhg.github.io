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
