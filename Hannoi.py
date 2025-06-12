from tHanoiAbstract import tHanoiAbstract

class Hannoi(tHanoiAbstract):
    """
    A concrete implementation of the Tower of Hanoi solver.
    This class inherits from tHanoiAbstract and implements the recursive
    algorithm to solve the puzzle.
    """

    def move_disk(self, source, target):
        """
        Prints a statement to track the movement of a disk from a source rod
        to a target rod. This fulfills the move_disk abstract method.

        :param source: The name of the source rod (e.g., 'Rod A').
        :param target: The name of the target rod (e.g., 'Rod C').
        """
        print(f"Move disk from {source} to {target}")

    def solve(self, disks, source, auxiliary, target):
        """
        Solves the Tower of Hanoi problem using a classic recursive algorithm.
        This fulfills the solve abstract method.

        The logic is as follows:
        1. Move n-1 disks from the source to the auxiliary rod.
        2. Move the nth (largest) disk from the source to the target rod.
        3. Move the n-1 disks from the auxiliary rod to the target rod.

        :param disks: The number of disks to move.
        :param source: The name of the source rod.
        :param auxiliary: The name of the auxiliary rod.
        :param target: The name of the target rod.
        """
        # Base case: If there is only one disk, move it directly.
        if disks == 1:
            self.move_disk(source, target)
        else:
            # Recursive step 1: Move n-1 disks from source to auxiliary.
            # The target rod becomes the auxiliary for this subproblem.
            self.solve(disks - 1, source, target, auxiliary)

            # Step 2: Move the largest remaining disk from source to target.
            self.move_disk(source, target)

            # Recursive step 3: Move the n-1 disks from auxiliary to target.
            # The source rod becomes the auxiliary for this subproblem.
            self.solve(disks - 1, auxiliary, source, target)


# --- Main Execution Block ---
# This part of the script will only run when the file is executed directly.

if __name__ == "__main__":
    # 1. Create an instance of our Hannoi solver class.
    hanoi_solver = Hannoi()

    # 2. Define the parameters for the problem.
    # You can change num_disks to solve for a different number of disks.
    num_disks = 3
    source_rod = "Rod A"
    auxiliary_rod = "Rod B"
    target_rod = "Rod C"

    # 3. Print the initial setup for clarity.
    print(f"Solving Tower of Hanoi for {num_disks} disks.")
    print(f"Source: {source_rod}, Auxiliary: {auxiliary_rod}, Target: {target_rod}\n")

    # 4. Call the solve method to run the algorithm.
    hanoi_solver.solve(num_disks, source_rod, auxiliary_rod, target_rod)

    # 5. Print a confirmation message upon completion.
    print("\nTower of Hanoi solved!")