# Problem: Longest Palindrome
"""
approach: 
Expand Around Center

Time Complexity: O(n^2)
Space Complexity: O(1)

Pattern: Two Pointers / Expansion
"""

def longestPalindrome(s: str) -> str:
    # Define a function that takes a string 's'
    # and returns another string (the longest palindrome)

    if not s:
        # If the string is empty ("")
        return ""
        # Just return empty string because there's nothing to process

    start, end = 0, 0
    # These will store the START and END index
    # of the longest palindrome found so far

    def expand(left: int, right: int):
        # This is a helper function
        # It expands outward from the center (left, right)

        while left >= 0 and right < len(s) and s[left] == s[right]:
            # Keep expanding while:
            # 1. left is within bounds
            # 2. right is within bounds
            # 3. characters match (palindrome condition)

            left -= 1
            # move left pointer one step left

            right += 1
            # move right pointer one step right

        return left + 1, right - 1
        # We went one step too far in the loop,
        # so we correct it:
        # left + 1 → last valid left index
        # right - 1 → last valid right index

    for i in range(len(s)):
        # Loop through every index in the string
        # Each index can be the CENTER of a palindrome

        l1, r1 = expand(i, i)
        # Case 1: odd-length palindrome (like "aba")
        # center is one character

        l2, r2 = expand(i, i + 1)
        # Case 2: even-length palindrome (like "abba")
        # center is between two characters

        if r1 - l1 > end - start:
            # If this palindrome is longer than the current best

            start, end = l1, r1
            # update the best palindrome indices

        if r2 - l2 > end - start:
            # Same check for even-length palindrome

            start, end = l2, r2
            # update if it's longer

    return s[start:end + 1]
    # Return the substring from start to end (inclusive)