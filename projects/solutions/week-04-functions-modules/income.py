"""Income sources.

A "source" is a dict with exactly two keys: "label" (str) and "amount" (float).
A collection of sources is a plain list of those dicts. Nothing in this module
prints, reads input, or touches global state.
"""


def add_income(sources: list[dict], label: str, amount: float) -> list[dict]:
    """Return a new list: `sources` plus one more income source."""
    return [*sources, {"label": label, "amount": float(amount)}]


def total_income(sources: list[dict]) -> float:
    """Return the sum of every source's amount, or 0.0 for no sources."""
    return sum((source["amount"] for source in sources), 0.0)


def _demo() -> str:
    """Return a short demonstration of this module's two public functions."""
    sources = add_income([], "salary", 2500)
    sources = add_income(sources, "freelance", 400)
    return "\n".join(
        [
            f"sources: {sources}",
            f"total_income: {total_income(sources):.2f}",
            f"total_income([]): {total_income([]):.2f}",
        ]
    )


if __name__ == "__main__":
    print(_demo())
