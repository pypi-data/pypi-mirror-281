"""executable - Create windows .exe files that just wrap a Python script."""
from __future__ import annotations


def greet(name: str) -> str:
    """Returns a greeting."""
    return f"Hello {name}!"
