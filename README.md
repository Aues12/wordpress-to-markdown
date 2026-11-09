# WordPress to Markdown

A modular Python library for converting WordPress content into structured, Markdown (including Obsidian-compatible notes) files.

---

## Overview

This project provides a clean and extensible pipeline to transform content from WordPress into local files suitable for knowledge management systems like Obsidian.

Core pipeline:

```
WordPress API → JSON → Process → Assemble → Write
```

---

## Features

* Fetch posts from WordPress REST API
* Normalize and process content
* Convert posts into structured objects
* Export as Markdown files
* Build output in `per_post` or `book` mode
* Optional YAML frontmatter generation
* Modular architecture (easy to extend)

---

## Project Structure

```text
wordpress-to-markdown/
├── src/wordpress_to_markdown/
│   ├── cli.py
│   ├── commanding.py
│   ├── config/
│   ├── core/
│   ├── importer/
│   ├── processors/
│   ├── sources/
│   ├── assembler.py
│   └── writer.py
├── tests/
├── config.json
└── pyproject.toml
```

---

## Installation

Requires Python 3.10 or newer.

### Install from PyPI (after the first release)

```bash
pip install wordpress-to-markdown
```

### Install from GitHub (available now)

```bash
pip install git+https://github.com/Aues12/wordpress-to-markdown.git
```

### Clone the repository

```bash
git clone https://github.com/Aues12/wordpress-to-markdown.git
cd wordpress-to-markdown
```

### Quickstart

(Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

### Development installation

With pip:

```bash
python -m pip install -e '.[dev]'
```

With uv (using `uv.lock`):

```bash
uv sync --locked --extra dev
uv run wordpress-to-markdown --help
```

Dependencies:

* requests
* PyYAML
* markdownify

For running tests:

* pytest

---

## Usage

### 1. Fetch data from WordPress

```python
from wordpress_to_markdown.importer.wordpress_api import export_posts_to_json

export_posts_to_json(
    base_url="https://your-site.com",
    output_file="data/imported.json"
)
```

Use this manual fetch step when you want to generate or refresh `data/imported.json`
outside the CLI workflow. In normal usage, `wordpress-to-markdown` already checks for the
JSON file and fetches it automatically when needed, or when you pass `--refresh`.

---

### 2. Configure the CLI

Use `--config /path/to/config.json` to select a configuration file. Relative `json_file` and `output_dir` paths are resolved from the configuration file's directory, not the shell's working directory.

Create/edit the `config.json` file in the project root:

```json
{
  "wordpress": {
    "base_url": "https://your-site.com"
  },
  "paths": {
    "json_file": "data/imported.json",
    "output_dir": "output"
  },
  "frontmatter": {
    "include_frontmatter": false,
    "fields": [
      "title",
      "date",
      "modified",
      "slug",
      "category_names"
    ]
  }
}
```

---

### 3. Run the pipeline

```bash
wordpress-to-markdown
```

This will:

* Load `config.json`
* Reuse existing JSON or fetch fresh data from WordPress
* Load JSON
* Process posts
* Assemble output
* Write Markdown files to the configured output directory

Available CLI options:

* `--refresh` fetches fresh data from WordPress before building
* `--order {newest,oldest}` controls post selection order before limiting
* `--write_order {newest,oldest}` controls ordering inside the written output
* `--limit N` limits the number of posts to build
* `--mode {per_post,book}` switches between one-file-per-post and combined book output
* `--frontmatter` includes YAML frontmatter in the assembled output
* `--excerpt` includes each WordPress excerpt before the post content (disabled by default)
* `--content-format {markdown,html}` converts post and excerpt HTML to Markdown (default), or preserves the imported HTML inside the `.md` output

Cached exports created before excerpt support do not contain this field. Use
`--refresh --excerpt` once to fetch excerpts from WordPress and rebuild them.

Examples:

```bash
# Build the 10 newest posts as individual markdown files
wordpress-to-markdown --order newest --limit 10 --mode per_post

# Build a single combined book in oldest-to-newest order
wordpress-to-markdown --order newest --limit 20 --write_order oldest --mode book

# Build individual files with WordPress excerpts below each title
wordpress-to-markdown --mode per_post --excerpt

# Preserve imported HTML in Markdown files
wordpress-to-markdown --content-format html --excerpt
```

---

## Testing and packaging

GitHub Actions runs the test suite with pip and uv on Python 3.10–3.13, then builds and checks both distributions. It also tests the installed wheel outside the repository.

```bash
pip install -e '.[dev]'
python -m pytest
python -m build
python -m twine check dist/*
```

The implementation lives in `src/wordpress_to_markdown/`; import modules through `wordpress_to_markdown`. For example, `from wordpress_to_markdown.config.loader import load_config`. Use `wordpress-to-markdown --config /absolute/path/to/config.json` from any working directory; paths inside the config are relative to that file.

## Testing

Run the test suite with:

```bash
python -m pytest
```

If `pytest` is not installed yet, install it with:

```bash
pip install pytest
```

---

## Core Concepts

### Post

Represents content during processing.

### DocumentUnit

Represents write-ready output.

### Pipeline

A sequence of transformations applied to each post.

### Assembler

Defines how posts are grouped (e.g., per_post, corpus).

### Writer

Handles output format (e.g., markdown, docx).

---

## Current Capabilities

* per_post assembly
* Book assembly
* Markdown export
* Turkish-aware slug generation
* Basic metadata normalization
* HTML to Markdown conversion
* Optional YAML frontmatter
* Config-driven output directory

---

## Future Roadmap

### Processing

* Markdown cleaning
* Link conversion (URL → wikilinks)

### Assembly

* Corpus mode

### Writer

* Additional output formats

---

## Design Principles

* Modular architecture
* Clear separation of concerns
* Stateless processing
* Extensibility over complexity

---

## Example Output

```
output/
├─ post-1.md
├─ post-2.md
└─ post-3.md
```

---

## License

MIT

---

## Final Note

This project is designed as a foundation for building flexible content pipelines and personal knowledge systems.
