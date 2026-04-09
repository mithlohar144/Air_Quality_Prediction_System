import os
import sys

# Ensure the dashboard package directory is importable when running from pages/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import air  # noqa: F401
