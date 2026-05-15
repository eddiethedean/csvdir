---
description: csvdir — read every CSV in a directory with one iterator. Install, guides, and API reference.
---

# csvdir

**Read every CSV in a directory as one stream of rows.** Treat a folder of CSV files as one dataset — discovery, headers, chunking, and optional [pandas](https://pandas.pydata.org/) integration with zero runtime dependencies.

!!! warning "Beta software"

    APIs may evolve between releases. Pin versions in production and read **[Changelog](CHANGELOG.md)** when upgrading.

<div class="grid cards" markdown>

- :material-rocket-launch:{ .lg .middle } __Get started__

    ---

    Install, mental model, and next steps in **[Getting started](getting-started.md)**.

- :material-book-open-variant:{ .lg .middle } __Guides__

    ---

    Iteration, headers, chunking, columns, discovery, encodings, and pandas in the **[Guides overview](guides/index.md)**.

- :material-tune:{ .lg .middle } __Configuration__

    ---

    Every `read_dir` and `CsvDirFile` parameter in **[Configuration reference](reference/options.md)**.

- :material-api:{ .lg .middle } __API reference__

    ---

    Factories, readers, iterators, and utilities in **[API reference](reference/api.md)**.

- :material-hammer-wrench:{ .lg .middle } __Development__

    ---

    Local setup, tests, linting, and doc builds in **[Development](development.md)**.

</div>

## Install (quick)

```bash
pip install csvdir
```

Optional extras (`[dev]`, `[docs]`) are described in **[Getting started](getting-started.md)**.

## Canonical README

The root **[README on GitHub](https://github.com/eddiethedean/csvdir/blob/main/README.md)** remains the single source for PyPI: feature list, usage snippets, badges, and links to this site.
