"""Smoke test: package imports and version are exposed correctly."""

import stormgrill


def test_version_exposed():
    assert isinstance(stormgrill.__version__, str)
    assert stormgrill.__version__
