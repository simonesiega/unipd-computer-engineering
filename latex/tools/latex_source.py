"""Small helpers for inspecting LaTeX source without interpreting TeX."""

from __future__ import annotations


def is_escaped(text: str, position: int) -> bool:
    """Return whether the character at *position* follows an odd backslash run."""
    backslashes = 0
    cursor = position - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def strip_comments(text: str) -> str:
    """Remove unescaped LaTeX comments while preserving line boundaries."""
    result: list[str] = []
    position = 0
    while position < len(text):
        if text[position] == "%" and not is_escaped(text, position):
            newline = text.find("\n", position)
            if newline < 0:
                break
            result.append("\n")
            position = newline + 1
            continue
        result.append(text[position])
        position += 1
    return "".join(result)
