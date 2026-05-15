---
description: csvdir — read every CSV in a directory with one iterator. Install, guides, and API reference.
---

# csvdir

**Read every CSV in a directory as one stream of rows.** Treat a folder of CSV files as one dataset — discovery, headers, chunking, and optional [pandas](https://pandas.pydata.org/) integration with zero runtime dependencies.

```{admonition} Beta software
:class: warning

APIs may evolve between releases. Pin versions in production and read [Changelog](CHANGELOG) when upgrading.
```

- **Get started**

---

Install, mental model, and next steps in [Getting started](getting-started.md).

- **User guide**

---

Iteration, headers, chunking, columns, discovery, encodings, and pandas in the [Guides overview](guides/index.md).

- **Configuration**

---

Every `read_dir` and `CsvDirFile` parameter in [Configuration reference](reference/options.md).

- **API reference**

---

Autodoc for factories, readers, iterators, and utilities — see **API reference** in the sidebar.

- **Development**

---

Local setup, tests, linting, and doc builds in [Development](development.md).

## Install (quick)

```bash
pip install csvdir
```

Optional dev/docs extras (`[dev]`, `[docs]`) are described in [Getting started](getting-started.md).

## Canonical README

The root [README on GitHub](https://github.com/eddiethedean/csvdir/blob/main/README.md) remains the single source for PyPI: feature list, usage snippets, badges, and links to this site.

```{toctree}
:hidden:
:maxdepth: 1

getting-started
CHANGELOG
guides/index
guide/iteration
guide/headers
guide/chunking
guide/columns
guide/discovery
guide/pandas
guide/encodings
reference/index
reference/options
development
```
