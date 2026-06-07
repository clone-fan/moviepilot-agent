#!/opt/venv/bin/python
"""Ensure Telegram/urllib3 compatibility patch exists after container updates.
Writes a minimal sitecustomize.py into the active virtualenv when urllib3-future
has overridden urllib3 and pyTelegramBotAPI still expects fields.format_header_param.
"""
from __future__ import annotations

import importlib
import pathlib
import sys
import sysconfig

PATCH_BODY = '''"""Runtime compatibility patch for Telegram module.
Adds urllib3.fields.format_header_param alias expected by pyTelegramBotAPI
when urllib3 has been overridden by urllib3-future.
"""
try:
    from urllib3 import fields as _fields
    if not hasattr(_fields, "format_header_param") and hasattr(_fields, "format_header_param_rfc2231"):
        _fields.format_header_param = _fields.format_header_param_rfc2231
except Exception:
    pass
'''


def main() -> int:
    try:
        fields = importlib.import_module("urllib3.fields")
    except Exception as exc:
        print(f"SKIP import urllib3.fields failed: {exc}")
        return 1

    has_target = hasattr(fields, "format_header_param")
    has_fallback = hasattr(fields, "format_header_param_rfc2231")
    try:
        importlib.import_module("urllib3_future")
        has_future = True
    except Exception:
        has_future = False

    purelib = pathlib.Path(sysconfig.get_paths()["purelib"])
    sitecustomize = purelib / "sitecustomize.py"

    if has_target:
        print(f"OK already-compatible file={sitecustomize}")
        return 0

    if not has_fallback:
        print("SKIP fallback symbol missing; no safe alias target")
        return 2

    sitecustomize.write_text(PATCH_BODY, encoding="utf-8")
    print(f"PATCHED file={sitecustomize} urllib3_future={has_future}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
