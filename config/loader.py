import json
from pathlib import Path


def load_config(config_path: str | Path = "config.json") -> dict:
    """Read configuration and resolve file paths relative to its location."""
    path = Path(config_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {path}")

    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    for key in ("json_file", "output_dir"):
        value = config.get("paths", {}).get(key)
        if value is not None:
            candidate = Path(value).expanduser()
            if not candidate.is_absolute():
                candidate = path.parent / candidate
            config["paths"][key] = str(candidate.resolve())

    return config
