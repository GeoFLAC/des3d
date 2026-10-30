---
sidebar_position: 1
---

# What is DES3D?

**DES3D** or **DynEarthSol3D** (Dynamic Earth Solver in 3D) is a finite
element code that solves the momentum balance and the heat transfer for 
elasto-visco-plastic materials in the Lagrangian form using unstructured 
meshes. It can be used for studying long-term deformations of the Earth\'s 
lithosphere but certainly not limited to it.

# How to cite

Please cite the DES3D v2.0 paper (preprint):

> Shyu, C. J., Lee, S., Ding, X., Keum, J., Tan, E., Lavier, L. L., & Choi, E. (2026). DynEarthSol v2.0: An efficient explicit Lagrangian solver for geodynamics, surface processes, and earthquake-cycle dynamics. *EGUsphere* [preprint, in review for *Solid Earth*]. DOI:[10.5194/egusphere-2026-2922](https://doi.org/10.5194/egusphere-2026-2922)

and the original method paper:

> Choi, E., Tan, E., Lavier, L. L., & Calo, V. M. (2013). DynEarthSol2D: An efficient unstructured finite element method to study long-term tectonic deformation. *Journal of Geophysical Research: Solid Earth*, 118(5), 2429–2444. DOI:[10.1002/jgrb.50148](https://doi.org/10.1002/jgrb.50148)

To cite the software itself, use DOI:[10.5281/zenodo.20293557](https://doi.org/10.5281/zenodo.20293557).
This DOI covers every archived release, both the software (`v2.x.x`) and the
benchmark datasets (`benchmarks-v2.x.x`), and it opens the list of all
versions. To cite the exact version you used, pick the matching software
release from that list, or take its DOI from the
[releases page](https://github.com/GeoFLAC/DynEarthSol/releases) or from the
`CITATION.cff` file shipped with that release.

:::tip Using an AI assistant to get oriented
If you're new to DES3D, one effective way to get started is working through
model setup with an AI coding assistant. Point it at this documentation site
and any background papers relevant to your problem, then describe the
tectonic scenario you want to model in plain language, geometry, timing,
boundary conditions, the processes involved, and iterate on the resulting
`.cfg` file together. Treat its output as a draft to check against this
manual and your own understanding of the parameters, not a substitute for
either.
:::

<!-- Check out the `usage`{.interpreted-text role="doc"} section for further
information, including `installation`{.interpreted-text role="ref"}. -->

<!-- DES3D has its documentation hosted on Read the Docs. -->

<!-- ::: note
::: title
Note
:::

This project is under active development.
::: -->

<!-- # Contents

::: toctree
usage api flowchart
::: -->
<!-- 
# Tutorial Intro

Let's discover **Docusaurus in less than 5 minutes**.

## Getting Started

Get started by **creating a new site**.

Or **try Docusaurus immediately** with **[docusaurus.new](https://docusaurus.new)**.

### What you'll need

- [Node.js](https://nodejs.org/en/download/) version 18.0 or above:
  - When installing Node.js, you are recommended to check all checkboxes related to dependencies.

## Generate a new site

Generate a new Docusaurus site using the **classic template**.

The classic template will automatically be added to your project after you run the command:

```bash
npm init docusaurus@latest my-website classic
```

You can type this command into Command Prompt, Powershell, Terminal, or any other integrated terminal of your code editor.

The command also installs all necessary dependencies you need to run Docusaurus.

## Start your site

Run the development server:

```bash
cd my-website
npm run start
```

The `cd` command changes the directory you're working with. In order to work with your newly created Docusaurus site, you'll need to navigate the terminal there.

The `npm run start` command builds your website locally and serves it through a development server, ready for you to view at http://localhost:3000/.

Open `docs/intro.md` (this page) and edit some lines: the site **reloads automatically** and displays your changes. -->
