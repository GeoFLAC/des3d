# des3d — DynEarthSol user documentation site

Docusaurus site for [GeoFLAC/DynEarthSol](https://github.com/GeoFLAC/DynEarthSol) (DES3D), deployed to GitHub Pages at https://geoflac.github.io/des3d/.

## Recurring task: sync docs with upstream DynEarthSol PRs

When asked to catch up the docs with recent DynEarthSol changes ("what's new", "sync the docs", "catch up with recent PRs"), run this procedure without being walked through it step by step:

1. **Find the last sync point.** Check `themeConfig.announcementBar` in `docusaurus.config.ts` for the PR number/date it references, and/or `git log --oneline -- docs/` for the last "docs: update ..." commit date.
2. **List what's merged since then:**
   ```
   gh pr list --repo GeoFLAC/DynEarthSol --state merged --limit 100 \
     --json number,title,mergedAt --jq '.[] | select(.mergedAt > "<last-sync-date>") | "\(.mergedAt[:10])  #\(.number)  \(.title)"' | sort
   ```
3. **Drop CI/workflow-only PRs** (titles like `ci:`, GitHub Actions/token/workflow refactors) — no doc surface.
4. **For each remaining PR**, `gh pr view <N> --repo GeoFLAC/DynEarthSol --json title,body,files` and judge whether it's user-facing (new parameter, build flag, output format, breaking change) vs. an invisible internal fix. Only document the former.
5. **Map user-facing changes to the right page:**
   - build options / dependencies → `docs/usage/usage.md`
   - running / checkpointing / restart behavior → `docs/usage/run.md`
   - output / visualization format → `docs/usage/visualize.md`
   - meshing/remeshing behavior and parameters → `docs/theory/remeshing.md` (other `docs/theory/` pages as applicable)
   - workflow-level features (coupling, weak zones, MMG, etc.) → `docs/tutorial/`
6. **Use the DynEarthSol README as source of truth** for build/dependency wording — it's usually updated in the same PR:
   ```
   gh api repos/GeoFLAC/DynEarthSol/contents/README.md --jq '.content' | base64 -d
   ```
   Condense its language into the docs rather than re-deriving it from source.
7. **Update the announcement bar** (`docusaurus.config.ts` → `themeConfig.announcementBar`): bump the PR number/date in `content`, and bump the `id` (e.g. increment a numeric suffix) so visitors who already dismissed the old banner see the new one.
8. **Verify before committing:** `yarn build`, then grep the generated HTML under `build/` for the new content to confirm it rendered (not just that the build didn't crash). Clean up `build/` and `.docusaurus/` afterward — they're not committed.
9. **Commit** with a message naming which upstream PR numbers were covered. Ask before pushing.

### Node version note

Docusaurus 3.x requires Node ≥20. If the system Node is older (check `node --version`), fetch a portable Node 20 binary into the scratchpad directory rather than touching the system install:
```
curl -fsSL https://nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.xz -o node20.tar.xz
tar -xJf node20.tar.xz -C node20 --strip-components=1
export PATH="$(pwd)/node20/bin:$PATH"
```
`yarn --ignore-engines install` bypasses the `package.json` engines check for install, but the Docusaurus CLI itself hard-checks the Node version at build time regardless — the actual binary must be ≥20.

## Doc scope discipline

Only document changes with a visible parameter, flag, workflow, or breaking-change surface. Skip internal-only correctness/perf fixes, refactors, and CI changes that don't change what a user of the engine sees or configures.
