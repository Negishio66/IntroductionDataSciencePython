from Similarity.similarity_coefficient import SimilarityCoefficient
from typing import Set, Any

class JaccardCoefficient(SimilarityCoefficient):
    """
    Implements the Jaccard Coefficient

    This class calculates similarity as the ratio of the intersection size
    to the union size of the two sets.
    """

    def calculate(self, set_a: Set[Any], set_b: Set[Any]) -> float:
        """
        Calculates the Jaccard Coefficient between two sets.

        The formula is J(X,Y) = |X∩Y| / |X∪Y|. A check is included to prevent
        division by zero if the union is empty.

        Args:
            set_a (Set[Any]): First set for comparison.
            set_b (Set[Any]): Second set for comparison.

        Returns:
            float: The calculated Jaccard Coefficient.
        """
        intersection_size = len(set_a.intersection(set_b))
        union_size = len(set_a.union(set_b))

        # Handle the edge case where the union of sets is empty.
        if union_size == 0:
            return 0.0

        return intersection_size / union_size

def calculate_string_jaccard(string_a: str, string_b: str) -> float:
    """
    A helper function to calculate the Jaccard Coefficient between two strings.

    It validates that both strings have a length greater than 3, converts
    them to sets of unique, lowercase characters, and then computes
    the coefficient.

    Args:
        string_a (str): First string.
        string_b (str): Second string.

    Returns:
        float: The calculated Jaccard Coefficient.

    Raises:
        ValueError: If either string has a length of 3 or less.
    """
    if len(string_a) <= 3 or len(string_b) <= 3:
        raise ValueError("Both strings must have a length greater than 3.")

    # Convert strings to sets of characters.
    set_a = set(string_a.lower())
    set_b = set(string_b.lower())

    # Instantiate the calculator.
    jaccard_calculator = JaccardCoefficient()
    
    # Perform the calculation and return the result.
    return jaccard_calculator.calculate(set_a, set_b)