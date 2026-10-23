# DES3D User Documentation

This is the [Docusaurus](https://docusaurus.io) site for
[GeoFLAC/DynEarthSol](https://github.com/GeoFLAC/DynEarthSol) (DES3D),
deployed to **https://geoflac.github.io/des3d/**.

It documents how to build, configure and run DES3D, it is not the
simulation code itself, that lives in the
[DynEarthSol](https://github.com/GeoFLAC/DynEarthSol) repository.

## Quick start

Requires Node.js ≥ 20 (Docusaurus 3.x hard-checks this at build time) and
Yarn.

```console
yarn install
yarn start      # dev server at http://localhost:3000/des3d/, hot-reloads on save
```

Before opening a PR, confirm the production build also succeeds (the dev
server is more forgiving about some things than the real build):

```console
yarn build
yarn clear       # clean .docusaurus/ and build/ when something looks stale
```

`yarn typecheck` runs `tsc` against `docusaurus.config.ts` and `sidebars.ts`.

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | The current ("Latest") documentation content, organized into `usage/`, `tutorial/`, and `theory/` categories. |
| `sidebars.ts` | Sidebar structure for `docs/`. |
| `versioned_docs/version-X.Y.Z/`, `versioned_sidebars/`, `versions.json` | Frozen snapshots of the docs matching already-tagged DynEarthSol releases (currently v2.0.0 and v2.0.2). Independent copies, not derived from `docs/`, see [CLAUDE.md](./CLAUDE.md) before editing one. |
| `static/` | Images and other files served as-is. |
| `src/css/custom.css` | Site-wide style overrides. |
| `docusaurus.config.ts` | Site config: navbar, footer, the announcement bar (tracks which DynEarthSol PR the docs are synced through), KaTeX/search plugins. |

## Keeping the docs in sync with DynEarthSol

Most of the day-to-day work on this repo isn't writing new docs from
scratch, it's catching up with upstream DynEarthSol changes:

- A GitHub Actions pipeline (`.github/workflows/dynearthsol-pr-notify.yml`,
  documented in [`.github/workflows/README.md`](./.github/workflows/README.md))
  automatically opens an issue here whenever a DynEarthSol PR merges with
  doc-relevant changes.
- **[`CLAUDE.md`](./CLAUDE.md) is the source of truth for that procedure**:
  which page a given kind of change belongs on, how to verify a change
  actually rendered, when something needs backporting into an older
  version's snapshot, and the announcement-bar/version-dropdown mechanics.
  Read it before making a non-trivial change, whether you're a human
  contributor or an AI assistant.

## Deployment and checks

- `deploy.yml` builds and deploys to GitHub Pages on every push to `main`.
- `test-deploy.yml` runs the same production build on every PR targeting
  `main`, without deploying; branch protection on `main` requires this
  check to pass before merging.
- `dependabot-auto-merge.yml` auto-merges patch/minor Dependabot PRs once
  that check passes (see
  [`.github/workflows/README.md`](./.github/workflows/README.md) for the
  cases it doesn't catch, e.g. transitive dependencies needing two
  coexisting major versions).

## Contributing

- Branch from `main`, open a PR, let `test-deploy.yml` verify the build.
  Direct pushes to `main` are technically allowed by branch protection but
  normal changes should go through a PR.
- See [CLAUDE.md](./CLAUDE.md) for the full doc-sync procedure, the
  versioned-docs workflow, and known gotchas (Node version, dependency
  resolution overrides, etc.).
