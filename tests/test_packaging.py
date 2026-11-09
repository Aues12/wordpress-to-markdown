"""Smoke tests for the distributable package."""

from pathlib import Path

from wordpress_to_markdown.cli import parse_args
from wordpress_to_markdown.config.loader import load_config
from wordpress_to_markdown.core.models import Post
from wordpress_to_markdown.assembler import assemble


def test_package_cli_config_option():
    # The installed CLI accepts a custom configuration path.
    assert parse_args(["--config", "site.json"]).config == "site.json"


def test_package_config_relative_paths(tmp_path, monkeypatch):
    # Resolve paths from the configuration directory, not the working directory.
    project = tmp_path / "blog"
    project.mkdir()
    (project / "config.json").write_text(
        '{"paths": {"json_file": "data/posts.json", "output_dir": "notes"}}',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    settings = load_config(project / "config.json")
    assert Path(settings["paths"]["json_file"]) == project / "data" / "posts.json"
    assert Path(settings["paths"]["output_dir"]) == project / "notes"


def test_package_assembly():
    # Verify package imports and basic Markdown conversion.
    units = assemble([Post(title="Hello", slug="hello", content="<p>World</p>")])
    assert units[0].filename == "hello.md"
    assert "World" in units[0].content


def test_cli_runs_with_external_config_from_another_directory(tmp_path, monkeypatch):
    import json
    import sys
    from wordpress_to_markdown.cli import main

    project = tmp_path / "blog"
    project.mkdir()
    (project / "posts.json").write_text(json.dumps({"posts": [
        {"title": "Example", "slug": "example", "content": "<p>Hello</p>"}
    ]}), encoding="utf-8")
    config = project / "config.json"
    config.write_text(json.dumps({
        "wordpress": {"base_url": "https://your-site.com"},
        "paths": {"json_file": "posts.json", "output_dir": "notes"},
        "frontmatter": {"fields": ["title"], "include_frontmatter": False},
    }), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["wordpress-to-markdown", "--config", str(config)])
    main()
    assert "Hello" in (project / "notes" / "example.md").read_text(encoding="utf-8")
