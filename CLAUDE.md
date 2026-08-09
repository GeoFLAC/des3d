# des3d — DynEarthSol user documentation site

Docusaurus site for [GeoFLAC/DynEarthSol](https://github.com/GeoFLAC/DynEarthSol) (DES3D), deployed to GitHub Pages at https://geoflac.github.io/des3d/.

## Recurring task: sync docs with upstream DynEarthSol PRs

When asked to catch up the docs with recent DynEarthSol changes ("what's new", "sync the docs", "catch up with recent PRs"), run this procedure without being walked through it step by step:

1. **Find the last sync point.** Check `themeConfig.announcementBar` in `docusaurus.config.ts` for the PR number/date it references, and/or `git log --oneline -- docs/` for the last "docs: update ..." commit date. If you're here because an automated triage issue (see below) already named a specific PR, skip straight to step 4 with that PR number instead of re-scanning.
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

## Automated notification pipeline

Merges to DynEarthSol no longer require manually running the `gh pr list` scan above to notice them — a cross-repo GitHub Actions pipeline does it automatically:

1. **`GeoFLAC/DynEarthSol/.github/workflows/notify-des3d.yml`** (a different repo, not checked out here) fires on every PR merged to `master`/`main`. It mints a token from the org's `notify-des-inputgen` GitHub App (scoped via `repositories: des3d`; this app's installation was extended to include `des3d` alongside its original `des-inputgen` target) and sends a `repository_dispatch` event (`dynearthsol-pr-merged`) carrying the PR number.
2. **`.github/workflows/dynearthsol-pr-notify.yml`** (in this repo) receives it, fetches the PR's changed files from the DynEarthSol API, and skips it if every changed file is under `.github/` (CI-only, no doc surface) — note this checks files, not the title, so a `ci:`-titled PR that also touches non-workflow files (e.g. `docker/Dockerfile.cuda`) still gets flagged. Otherwise it opens a GitHub issue here titled `Review DynEarthSol #<N> for doc updates: <title>`.
3. When one of those issues shows up, that's the trigger to run the sync procedure above for that specific PR — start at step 4 with the PR number the issue already gives you.
4. Both workflows can also be run manually via `workflow_dispatch` (`gh workflow run <file> --repo <owner/repo> -f number=<N>` / `-f pr_number=<N>`) for testing. **Gotcha:** `workflow_dispatch` can't be fired on a workflow that exists only on a non-default branch — GitHub only indexes dispatchable workflows from the default branch, so a newly-added or newly-edited workflow must be merged before it can be triggered this way, even with `--ref <branch>` pointing at where the code actually lives.

## Dependency security updates

Dependabot alerts on this repo are handled by a mix of GitHub-native automation and manual fixes — see `.github/workflows/README.md` for the full picture. In short: Dependabot security updates + repo auto-merge + a branch protection rule requiring the `Test deployment` check are enabled, and `dependabot-auto-merge.yml` auto-merges patch/minor Dependabot PRs once that check passes. This covers most alerts with no intervention needed.

What it *won't* catch: alerts on deep transitive dependencies where different consumers in the tree genuinely need different major versions of the same package (a semver-invisible runtime conflict, not something Dependabot can resolve with a single-version bump). The `js-yaml`/`gray-matter` case is the concrete example — `gray-matter` calls the since-removed `yaml.safeLoad`, so it needs to stay on js-yaml 3.x while everything else uses 4.x. Fixing these requires scoped `resolutions` entries in `package.json` using anchored paths (e.g. `"@docusaurus/core/**/gray-matter/js-yaml": "3.15.1"`), not a single bare `"js-yaml"` override — a bare override collapses both tracks onto one version and silently breaks whichever side needed the other major version. If you add a bare resolution key for a package that also has an anchored one, the bare key seems to win over the more specific one in practice (contrary to what Yarn's docs imply about specificity) — don't mix the two for the same package. Alerts with no upstream fix at all (check via `npm view <pkg> versions` / the GHSA advisory's `first_patched_version`) are left open with a note; don't force a downgrade to dodge them without checking whether the vulnerable code path is even reachable here (e.g. `image-size`'s DoS parsers only run at build time against this repo's own trusted images, never untrusted input).
