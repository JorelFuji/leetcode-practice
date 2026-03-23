import pytest
from problems.zigzag_conversion import Solution

@pytest.mark.parametrize("input_str, num_rows, expected", [
    # Example 1 from problem statement
    ("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"),
    
    # Example 2 with 4 rows
    ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"),
    
    # Edge cases
    ("A", 1, "A"),                  # Single character
    ("AB", 1, "AB"),                # Single row
    ("ABC", 2, "ACB"),              # Two rows
    ("ABCDE", 1, "ABCDE"),          # numRows = 1 (no zigzag)
    ("ABCDEF", 2, "ACEBDF"),        # Two rows zigzag
    
    # Special cases
    ("", 3, ""),                    # Empty string
    ("Hello World!", 3, "Horel ol!lWd"), # With spaces and special characters
    ("12345", 5, "12345"),          # numRows = length of string
    ("ABCDEFGH", 100, "ABCDEFGH"),  # numRows > length of string
])
def test_zigzag_conversion(input_str, num_rows, expected):
    solution = Solution()
    result = solution.convert(input_str, num_rows)
    assert result == expected, f"Failed for input '{input_str}' with {num_rows} rows. Expected '{expected}', got '{result}'"