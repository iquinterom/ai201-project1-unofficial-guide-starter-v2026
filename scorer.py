"""Judges whether a generated answer actually contains what a question expects.

`run_eval.py::load_scorer` picks this up automatically once it exists — the
Run columns switch from blank to pass/fail without anything else changing.
"""

import re


def _normalize(text: str | None) -> str:
    """Lower-case, strip punctuation, and collapse whitespace."""
    if not text:
        return ""
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(text.split())


def _contains_phrase(haystack: str, phrase: str) -> bool:
    """True if `phrase` (or all its words) shows up in `haystack`, normalized."""
    norm_haystack = _normalize(haystack)
    norm_phrase = _normalize(phrase)
    if not norm_phrase:
        return False
    if norm_phrase in norm_haystack:
        return True
    words = norm_phrase.split()
    haystack_words = norm_haystack.split()
    return len(words) > 1 and all(w in haystack_words for w in words)


def judge(question: str, expects: str, answer: str | None, results) -> bool:
    """True when the answer, or a retrieved chunk, contains what `expects` names.

    `expects` may list more than one acceptable phrase, separated by ';' or
    '|' — the question passes if any one of them shows up.
    """
    phrases = [p.strip() for p in re.split(r"[;|]", expects or "") if p.strip()]
    if not phrases or not answer:
        return False

    if any(_contains_phrase(answer, p) for p in phrases):
        return True

    retrieved = " ".join(getattr(r, "text", "") for r in results or [])
    return any(_contains_phrase(retrieved, p) for p in phrases)
