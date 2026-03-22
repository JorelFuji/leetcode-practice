import pytest
from problems.longest_palindrome import longestPalindrome

@pytest.mark.parametrize("input_str, expected", [
    ("babed", ["bab", "aba"]),
    ("cbbd", ["bb", "aba"]),
    ("a", ["a"]),
    ("ac", ["a","c"]),
    ("racecar", ["racecar"]),
    ("aaaa", ["aaaa"]),
])
def test_longest_palindrome(input_str, expected):
    result = longestPalindrome(input_str)
    assert result in expected