#!/bin/python3
#
# Reverse word order, then swap letter case (Python 3).
# HackerRank: "Python: Reverse Words and Swap Cases"
#
# Sample: "aWESOME is cODING" -> reverse -> "cODING is aWESOME" -> swapcase -> "Coding IS Awesome"
#

import sys


def reverse_words_order_and_swap_cases(sentence):
    """Return words in reverse order with each letter's case swapped."""
    words = sentence.split()
    back = " ".join(reversed(words))
    return back.swapcase()


def _read_sentence_from_stdin():
    line = sys.stdin.readline()
    if line == "":
        raise SystemExit("Expected one line (sentence) on stdin.")
    return line.rstrip("\n\r")


def main():
    s = _read_sentence_from_stdin()
    sys.stdout.write(reverse_words_order_and_swap_cases(s) + "\n")


if __name__ == "__main__":
    assert reverse_words_order_and_swap_cases("rUns dOg") == "DoG RuNS"
    assert reverse_words_order_and_swap_cases("aWESOME is cODING") == "Coding IS Awesome"
    main()
