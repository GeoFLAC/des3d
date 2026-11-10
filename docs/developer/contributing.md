---
sidebar_position: 4
slug: /developer/contributing
title: Contributing
description: Commits, issues, pull requests and releases for DynEarthSol.
---

# Contributing

DynEarthSol is developed on GitHub at
[GeoFLAC/DynEarthSol](https://github.com/GeoFLAC/DynEarthSol). The
repository's
[`CONTRIBUTING.md`](https://github.com/GeoFLAC/DynEarthSol/blob/master/CONTRIBUTING.md)
is the authority for everything on this page; this is a summary.

## Commits

A commit message records what the code cannot: what was wrong before, why
this change and not another, and what it was measured to do.

```text
type: imperative summary, 72 characters or fewer, no period

The problem and its user-visible effect. The approach, where the diff does
not make it obvious, and alternatives rejected. Numbers for every claim.

Co-Authored-By: Name <email>
```

`type` is one of `fix`, `feat`, `refactor`, `test`, `docs`, `ci`, `build` or
`cleanup`. Refer to earlier work by its subject or pull-request number, not
by hash alone, since branches are rebased.

## Issues and pull requests

Templates under `.github/` fill in when you open an issue or a pull request.

- **Bug reports:** one issue per symptom, with the version, the exact build
  and run commands, the smallest failing input and the output as text.
- **Enhancements:** the problem, a concrete proposal, alternatives rejected,
  and what closes the issue.
- **Pull requests:** one topic each, commits that each build and pass
  `tests/regression`, and a title that stands alone in `git log`. Report
  whether the change altered results (see [Testing a change](./testing.md)).
  Open as a draft until CI passes, then ask at least one other developer to
  review.

## AI-assisted contributions

They are welcome. You are responsible for the output of the tools you use and
should be able to explain every line. Disclose the tools in the pull
request, name them in `Co-Authored-By` trailers, and reply to reviews
yourself. `AGENTS.md` in the repository root gives an assistant the rules it
cannot infer from the code.

## Releases

A release updates `CHANGELOG.md`, `CITATION.cff` and `.zenodo.json`, is
merged through a reviewed pull request, and is then tagged (`v2.x.y`). The
tag triggers a workflow that packages the source with its submodules for a
draft GitHub release and a Zenodo deposit. The steps are in
`CONTRIBUTING.md` under "Development and release workflow".
