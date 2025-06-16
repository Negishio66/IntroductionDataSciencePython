def calculate_hamming_distance(string_a: str, string_b: str) -> int:
    """
    Calculates the Hamming distance between two strings.

    It first validates that both strings have a length greater than 3 and
    that they are of equal length, as these are prerequisites for the
    Hamming distance calculation.

    Args:
        string_a (str): First string for comparison.
        string_b (str): Second string for comparison.

    Returns:
        int: The Hamming distance, which is the number of positions at which
             the corresponding characters are different.

    Raises:
        ValueError: If either string has a length of 3 or less, or if the
                    strings are not of equal length.
    """
    # First, validate that both strings meet the minimum length requirement.
    if len(string_a) <= 3 or len(string_b) <= 3:
        raise ValueError("Both strings must have a length greater than 3.")

    # Next, validate that the strings are of equal length, a core
    # requirement for Hamming distance.
    if len(string_a) != len(string_b):
        raise ValueError("For Hamming distance, both strings must be of the same length.")

    # Calculate the distance by summing the positions where characters differ.
    return sum(1 for char_a, char_b in zip(string_a, string_b) if char_a != char_b)