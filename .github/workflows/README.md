# Workflows

## `deploy.yml`
Builds the Docusaurus site and deploys it to GitHub Pages on every push to `main`.

## `test-deploy.yml`
Runs the same production build on pull requests targeting `main`, without deploying, so a broken build is caught before merge.

## `dynearthsol-pr-notify.yml`
Triages merged [DynEarthSol](https://github.com/GeoFLAC/DynEarthSol) PRs for doc relevance.

It's the receiving half of a two-repo pipeline: DynEarthSol's `notify-des3d.yml` workflow fires on every PR merged to its `master`/`main`, and sends a `repository_dispatch` event (`dynearthsol-pr-merged`) here carrying the PR number. Both sides authenticate via the org's `notify-des-inputgen` GitHub App rather than a personal token/secret in this repo.

On receipt, this workflow fetches the PR's changed files from the DynEarthSol API and:
- **skips it** if every changed file is under `.github/` (CI-only — checked by file path, not the PR title, since a `ci:`-titled PR can still touch non-workflow files)
- **otherwise opens a triage issue** in this repo, titled `Review DynEarthSol #<N> for doc updates: <title>`, linking the PR and listing its changed files

See [`CLAUDE.md`](../../CLAUDE.md) for the doc-sync procedure a triage issue is meant to kick off, and for the `workflow_dispatch` testing gotcha (a workflow must be merged to the default branch before it can be dispatched manually, on either side of the pipeline).

Can be run manually for testing: `gh workflow run dynearthsol-pr-notify.yml --repo GeoFLAC/des3d -f number=<PR>`.

## `dependabot-auto-merge.yml`
Auto-approves and enables auto-merge for Dependabot PRs that are patch or minor version bumps (major bumps are left for manual review, since they're more likely to need judgment). Uses `dependabot/fetch-metadata` to read the update type, then `gh pr merge --auto`.

This only *enables* auto-merge — the actual merge is still gated by branch protection on `main`, which requires the `Test deployment` check (the same build `test-deploy.yml` runs) to pass first. A dependency bump that breaks the build (e.g. the js-yaml/gray-matter conflict documented in the `Patch nanoid, undici, and js-yaml security advisories` commit) just sits open instead of merging.

Depends on repo settings that aren't in this file: Dependabot security updates enabled, "Allow auto-merge" enabled, and a branch protection ruleset on `main` requiring the `Test deployment` check (only that — not "require a pull request before merging", so direct pushes to `main` still work).
