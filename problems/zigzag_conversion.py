# THE STIRNG IS WRITTEN IN ZIGZAG PETTER ON A GIVEN NUMBER OF ROWS
# WRITE THE CODE THAT WILL TAKE A STING AND MAKE COVERSION GIVEN BY NUMBER OF ROWS
# INPUT: s = "PAYPALISHIRING", numRows = 3
# OUTPUT: "PAHNAPLSIIGYIR"
# CONSTRAINTS:
# 1 <= s.length <= 1000
# s consists of English letters (lowercase and uppercase), digits, and special characters.
"""
need to understand the difference in 
comment and how they can written in python 
"""
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # Edge case: if only 1 row, nothing changes
        if numRows == 1:
            return s
        
        # Create a list for each row
        rows = [""] * numRows
        
        current_row = 0  # track which row we're on
        direction = 1    # 1 = going down, -1 = going up
        
        # Go through each character in the string
        for char in s:
            # Add character to the current row
            rows[current_row] += char
            
            # If we hit top or bottom, change direction
            if current_row == 0:
                direction = 1
            elif current_row == numRows - 1:
                direction = -1
            
            # Move to next row
            current_row += direction
        
        # Join all rows into one string
        return "".join(rows)