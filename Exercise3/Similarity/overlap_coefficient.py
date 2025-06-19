from similarity_coefficient import SimilarityCoefficient
from typing import Set, Any

class OverlapCoefficient(SimilarityCoefficient):
    """
    Implements the Overlap Coefficient, also known as the Szymkiewicz-Simpson
    coefficient.

    This class calculates similarity as the ratio of the intersection size
    to the size of the smaller of the two sets.
    """

    def calculate(self, set_a: Set[Any], set_b: Set[Any]) -> float:
        """
        Calculates the Overlap Coefficient between two sets.

        The formula is Overlap(A,B) = |A∩B|/min(|A|,|B|). A check is included to prevent
        division by zero if the smaller set is empty.

        Args:
            set_a (Set[Any]): First set for comparison.
            set_b (Set[Any]): Second set for comparison.

        Returns:
            float: The calculated Overlap Coefficient.
        """
        intersection_size = len(set_a.intersection(set_b))
        min_size = min(len(set_a), len(set_b))

        # Handle the edge case where the smaller set is empty.
        if min_size == 0:
            return 0.0

        return intersection_size / min_size

def calculate_string_overlap(string_a: str, string_b: str) -> float:
    """
    A helper function to calculate the Overlap Coefficient between two strings.

    It validates that both strings have a length greater than 3, converts
    them to sets of unique, lowercase characters, and then computes
    the coefficient.

    Args:
        string_a (str): First string.
        string_b (str): Second string.

    Returns:
        float: The calculated Overlap Coefficient.

    Raises:
        ValueError: If either string has a length of 3 or less.
    """
    if len(string_a) <= 3 or len(string_b) <= 3:
        raise ValueError("Both strings must have a length greater than 3.")

    # Convert strings to sets of characters.
    set_a = set(string_a.lower())
    set_b = set(string_b.lower())

    # Instantiate the calculator.
    overlap_calculator = OverlapCoefficient()
    
    # Perform the calculation and return the result.
    return overlap_calculator.calculate(set_a, set_b)
