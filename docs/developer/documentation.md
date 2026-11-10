---
sidebar_position: 5
slug: /developer/documentation
title: Maintaining this manual
description: How this site is organized, built, checked and kept in step with DynEarthSol.
---

# Maintaining this manual

This manual is a [Docusaurus](https://docusaurus.io) site in the
[GeoFLAC/des3d](https://github.com/GeoFLAC/des3d) repository, published at
https://geoflac.github.io/des3d/ when changes are merged to `main`.

## Structure

| Section | Folder | Contents |
| --- | --- | --- |
| Getting started | `docs/getting-started/` | overview, installation, quickstart, running, visualizing, troubleshooting |
| Theory | `docs/theory/` | formulation and numerical methods |
| User guide | `docs/user-guide/` | one feature per page: model setup, numerical controls, running and output |
| Tutorials | `docs/tutorial/` | reproducible worked examples that build a model for a geoscience problem, each opening with an *At a glance* box |
| Benchmarks | `docs/benchmarks/` | DES compared with analytical, theoretical or independent solutions, grouped by field and listed in the overview |
| Reference | `docs/reference/` | configuration file and the generated parameter list |
| Developer guide | `docs/developer/` | this section |

Moved pages keep their published URL through a `slug:` in their front
matter, and a renamed category page gets a redirect in
`docusaurus.config.ts`. Link to other pages by relative file path, such as
`../user-guide/running/restart.md`, so the build can check the link.

## Building and checking

Docusaurus needs Node 20 or later.

```console
yarn install
yarn build      # fails on any broken link, anchor or image
yarn start      # local preview at http://localhost:3000/des3d/
```

## The parameter reference

`docs/reference/parameters.md` is generated, never edited by hand. After any
change to DynEarthSol's options, build both executables at that revision and
run:

```console
python3 scripts/generate_parameter_reference.py \
    --exe2d /path/to/dynearthsol2d --exe3d /path/to/dynearthsol3d --source <revision>
```

`--check` with the same arguments reports whether the page is out of date.

## Versions

`docs/` is the "Latest" manual, following the current source. Each tagged
release has a frozen copy under `versioned_docs/`. A correction that also
applies to a release is made in its copy too; a page for a feature that a
release did not have is not added to it. When DynEarthSol tags a release,
`yarn docusaurus docs:version vX.Y.Z` freezes the current manual.

## Keeping up with DynEarthSol

When a pull request is merged into DynEarthSol, a workflow opens an issue in
this repository asking for a documentation review. User-visible changes (new
or changed parameters, build options, output formats, breaking changes) are
documented on the page for that feature; internal fixes are not. Tutorials
record the DynEarthSol revision they were checked with in their *At a
glance* box.
