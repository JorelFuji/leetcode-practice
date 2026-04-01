#!/usr/bin/env python3
"""
Given STR1 and STR2 where len(STR1) = len(STR2) + 1, return all 0-based indices
in STR1 that can be removed to make STR1 equal STR2. If none, print -1.
"""

from __future__ import annotations

import sys


def removable_indices(str1: str, str2: str) -> list[int]:
    n1 = len(str1)
    n2 = len(str2)
    if n1 != n2 + 1:
        return [-1]

    # pref[i] == (str1[0:i] == str2[0:i]) for i in [0..n2]
    pref = [False] * (n2 + 1)
    pref[0] = True
    for i in range(n2):
        pref[i + 1] = pref[i] and (str1[i] == str2[i])

    # suf[i] == (str1[i+1:] == str2[i:]) for i in [0..n2]
    suf = [False] * (n2 + 1)
    suf[n2] = True  # str1[n2+1:] == str2[n2:] == ""
    for i in range(n2 - 1, -1, -1):
        suf[i] = suf[i + 1] and (str1[i + 1] == str2[i])

    ans: list[int] = []
    for i in range(n1):  # i in [0..n2]
        if pref[i] and suf[i]:
            ans.append(i)

    return ans if ans else [-1]


def _read_two_strings_from_stdin() -> tuple[str, str]:
    data = [line.strip() for line in sys.stdin.read().splitlines() if line.strip() != ""]
    if len(data) >= 2:
        return data[0], data[1]
    if len(data) == 1:
        # Allow "STR1 STR2" on one line as a fallback.
        parts = data[0].split()
        if len(parts) == 2:
            return parts[0], parts[1]
    raise SystemExit("Expected STR1 and STR2 on stdin (two lines or one line with two tokens).")


def main() -> None:
    str1, str2 = _read_two_strings_from_stdin()
    res = removable_indices(str1, str2)
    if res == [-1]:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write(" ".join(map(str, res)) + "\n")


if __name__ == "__main__":
    main()

