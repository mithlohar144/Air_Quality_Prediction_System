"""Compatibility shim.

The dashboard pages import `_shared`, but the canonical shared module in this repo is
`shared.py`. This file re-exports the shared symbols so existing imports keep
working.
"""

from shared import *  # noqa: F401,F403
