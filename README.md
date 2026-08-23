# Coding utilities

A practical, growing collection of resources for people who build software: literature reviews, decision frameworks, small tools, and reusable working notes.

This repository is intentionally lightweight. Each collection should be useful on its own, easy to browse, and explicit about its scope and provenance.

## Contents

| Collection | What it contains |
| --- | --- |
| [Multi-agent software engineering literature review (2026)](multi-agent-software-engineering-literature-2026/) | An evidence-led review of when multi-agent coding workflows help, where they fail, and how to operate them safely. |

## Featured resource: multi-agent software engineering

The [2026 multi-agent software engineering literature review](multi-agent-software-engineering-literature-2026/) brings together foundations, empirical evidence, feature-delivery practices, platform capabilities, limitations, and a decision framework.

If you only need the practical takeaway, start with the [synthesis and decision framework](multi-agent-software-engineering-literature-2026/08-synthesis-decision-framework.md). Its central recommendation is simple: add agents only when work can be independently executed and verified behind stable boundaries; otherwise, one capable agent is usually the better default.

## Navigating the repository

- Each top-level directory is a self-contained collection and should include its own `README.md`.
- Numbered Markdown files are intended to be read in order where a collection describes a research process or report.
- Links in collection READMEs are the preferred entry points; they explain context, assumptions, and limitations better than a bare file listing.

## Adding something useful

Contributions are welcome when they are practical, attributable, and maintainable. A new collection should:

1. Live in a clearly named top-level directory.
2. Include a concise `README.md` explaining its purpose, intended audience, and how to use it.
3. Cite sources and state any relevant date, version, or evidence limitations.
4. Avoid committing generated files, credentials, or machine-specific configuration.
5. Add an entry to the contents table above.

For a small standalone utility, include the command to run it, its dependencies, an example, and any expected input or output.

## Scope

This is a curated personal knowledge base and toolbox, not a packaged application. Material may range from carefully sourced research notes to focused scripts and templates; each collection should make its own level of validation clear.
