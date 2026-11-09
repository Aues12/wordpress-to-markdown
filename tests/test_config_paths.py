import json
from pathlib import Path

from config.loader import load_config
from sources.imported_json import load_imported_json
from cli.main import parse_args


def test_paths_are_relative_to_config_file(tmp_path, monkeypatch):
    project = tmp_path / "blog"
    project.mkdir()
    config_file = project / "custom.json"
    config_file.write_text(json.dumps({
        "wordpress": {"base_url": "https://example.com"},
        "paths": {"json_file": "data/imported.json", "output_dir": "output"},
        "frontmatter": {"fields": ["title"], "include_frontmatter": True},
    }), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    config = load_config(config_file)
    assert Path(config["paths"]["json_file"]) == project / "data" / "imported.json"
    assert Path(config["paths"]["output_dir"]) == project / "output"


def test_absolute_paths_are_preserved(tmp_path):
    absolute = tmp_path / "archive.json"
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"paths": {"json_file": str(absolute)}}), encoding="utf-8")
    assert Path(load_config(config_file)["paths"]["json_file"]) == absolute


def test_frontmatter_fields_are_selected_per_invocation(tmp_path):
    data_file = tmp_path / "posts.json"
    data_file.write_text(json.dumps({"posts": [{
        "title": "Example", "slug": "example", "date": "2026-01-01"
    }]}), encoding="utf-8")
    posts = load_imported_json(data_file, frontmatter_fields=["slug"])
    assert posts[0].frontmatter == {"slug": "example"}


def test_cli_accepts_custom_config():
    assert parse_args(["--config", "another.json"]).config == "another.json"
    assert parse_args([]).config == "config.json"
