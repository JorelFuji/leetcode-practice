from problems.longest_palindrome import longestPalindrome


def run():
    print("=== Longest Palindromic Substring ===")

    user_input = input("Enter string: ").strip()

    result = longestPalindrome(user_input)

    print(f"Input: {user_input}")
    print(f"Output: {result}")


if __name__ == "__main__":
    run()