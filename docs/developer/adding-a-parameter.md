---
sidebar_position: 3
slug: /developer/adding-a-parameter
title: Adding an input parameter
description: The places an input parameter touches in the source, and how to document it.
---

# Adding an input parameter

An input parameter appears in four places in the source and one in this
manual.

1. **`parameters.hpp`.** Add the member to the struct of its section
   (`Sim`, `Mesh`, `Control`, `BC`, `IC`, `Mat`, `Monitor`, ...).
2. **`input.cxx`, `declare_parameters`.** Register `section.name` with its
   type, default and help text. The help text is what users see with `-h`
   and what the [parameter reference](../reference/parameters.md) is
   generated from, so state the meaning, the unit and the valid values.
   Per-material lists are declared as text and read with `get_numbers`.
3. **`input.cxx`, `validate_parameters`.** Reject invalid values and
   incompatible combinations with `die(EXIT_CONFIG_VALUE, "...")`, naming the
   parameter in the message.
4. **`examples/defaults.cfg`.** Add a commented line with the default, in its
   section.

Record new, changed and removed parameters in `CHANGELOG.md`.

Then document it:

- add it to the parameter table of the User guide or Theory page for its
  feature;
- regenerate the [parameter reference](../reference/parameters.md) from
  executables built at that revision (see
  [maintaining this manual](./documentation.md)).

Parameter names come from `examples/defaults.cfg` or `-h`; never guess one in
documentation or examples.
