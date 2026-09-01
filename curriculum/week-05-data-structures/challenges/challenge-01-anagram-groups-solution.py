"""challenge-01-anagram-groups-solution.py — group the anagrams together.

Reflection on the structure I picked, as the rubric asks for.

I chose a dict keyed by each word's sorted-letter signature because the
anagram relation is exactly "same multiset of letters", and a sorted letter
string is a canonical, hashable name for that multiset. That turns an
O(n^2) all-pairs comparison into n independent O(k log k) key computations
plus n O(1) dict insertions. A list of lists would have forced a linear
scan per word to find the right group; the dict does that lookup by hash.
"""


def signature(word: str) -> str:
    """Return a canonical name for a word's letter multiset.

    Args:
        word: The word to name.

    Returns:
        The word's letters, sorted and joined back into a string. Two words
        are anagrams exactly when their signatures are equal.
    """
    return "".join(sorted(word))


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group the words that are anagrams of one another.

    Args:
        words: The words to group. Order is preserved within each group.

    Returns:
        One list per signature, in the order each signature was first seen.
        A word with no anagram partner comes back as a group of one.
    """
    groups: dict[str, list[str]] = {}
    for word in words:
        groups.setdefault(signature(word), []).append(word)
    return list(groups.values())


if __name__ == "__main__":
    words = [
        "eat", "tea", "tan", "ate", "nat", "bat",
        "listen", "silent", "enlist",
        "evil", "vile", "live", "veil",
        "hello",
    ]

    groups = group_anagrams(words)

    # total word count is preserved
    assert sum(len(g) for g in groups) == len(words)

    # every group is internally consistent (sorted chars match)
    for g in groups:
        sig = sorted(g[0])
        for w in g:
            assert sorted(w) == sig

    # group sizes (sorted) should be [1, 1, 2, 3, 3, 4]
    sizes = sorted(len(g) for g in groups)
    assert sizes == [1, 1, 2, 3, 3, 4]

    # the four cases the brief calls out by name
    assert group_anagrams([]) == []                           # empty input
    assert group_anagrams(["ab", "abc"]) == [["ab"], ["abc"]]  # lengths never merge
    assert group_anagrams(["a", "a"]) == [["a", "a"]]          # exact repeats, one group
    assert group_anagrams(["bat"]) == [["bat"]]                # singletons are groups

    print("All checks passed.")

    for g in groups:
        print(g)
