import sys
import random
from pigeonHoleSortAbstract import pigeonHoleSortAbstract


class PigeonHoleSort(pigeonHoleSortAbstract):
    """
    A concrete implementation of the Pigeonhole Sort algorithm.
    This class inherits from pigeonHoleSortAbstract and provides the logic
    to sort a list of numbers. It is designed to be executed from the
    command line, taking the number of random elements to sort as an argument.
    """

    def sort(self, arr):
        """
        Sorts a list of numbers using the Pigeonhole Sort algorithm.
        This method works best when the range of values in the list is not
        significantly larger than the number of elements.

        :param arr: The list of numbers to be sorted. It is sorted in-place.
        :return: The sorted list.
        """
        # A list with 0 or 1 elements is already sorted.
        if len(arr) <= 1:
            return arr

        # Find the minimum and maximum values in the input array to determine the range.
        try:
            min_val = min(arr)
            max_val = max(arr)
        except TypeError:
            print("Error: Pigeonhole sort can only be applied to lists of comparable items (like numbers).",
                  file=sys.stderr)
            return arr  # Return original array if it contains non-comparable types

        # Calculate the size of the 'pigeonhole' array.
        # The range is the difference between max and min values plus one.
        size = max_val - min_val + 1

        # Create the pigeonholes. Each hole corresponds to a value in the range.
        # Initialize all holes to zero.
        holes = [0] * size

        # Populate the pigeonholes. Iterate through the input array and increment
        # the count for the corresponding pigeonhole.
        for x in arr:
            holes[x - min_val] += 1

        # Reconstruct the sorted array from the pigeonholes.
        # 'i' will be the current index in the original array to place the sorted element.
        i = 0
        # Iterate through the pigeonholes from the start.
        for count in range(size):
            # For each pigeonhole, place its elements back into the array
            # as many times as its count.
            while holes[count] > 0:
                holes[count] -= 1
                arr[i] = count + min_val
                i += 1

        return arr


# Main execution block to allow running the script from the terminal.
if __name__ == "__main__":
    # --- Argument Validation ---
    # The script expects exactly one argument: the number of elements to sort.
    # sys.argv[0] is the script name itself, so we check for a total length of 2.
    if len(sys.argv) != 2:
        # Print an error message to standard error if the argument count is wrong.
        print("Error: The user does not specify the correct number of input parameters.", file=sys.stderr)
        print("Syntax is: python pigeonHoleSort.py randomN", file=sys.stderr)
        # Exit the script with a non-zero status code to indicate an error.
        sys.exit(1)

    try:
        # Convert the command-line argument to an integer.
        n = int(sys.argv[1])
        if n <= 0:
            print("Error: The number of elements must be a positive integer.", file=sys.stderr)
            sys.exit(1)
    except ValueError:
        # Handle the case where the argument is not a valid integer.
        print("Error: The input 'randomN' must be an integer.", file=sys.stderr)
        sys.exit(1)

    # Generate a list of 'n' random integers for demonstration.
    # The range of random numbers is chosen to be suitable for Pigeonhole Sort.
    random_list = [random.randint(0, 1000) for _ in range(n)]

    print(f"Original list of {n} random numbers:")
    print(random_list)
    print("-" * 40)

    # Create an instance of our sorting class.
    sorter = PigeonHoleSort()
    # Call the sort method to sort the list.
    sorted_list = sorter.sort(random_list)

    print("List after Pigeonhole Sort:")
    print(sorted_list)