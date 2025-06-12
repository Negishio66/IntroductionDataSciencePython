from abc import ABC, abstractmethod

class tHanoiAbstract(ABC):
    @abstractmethod
    def move_disk(self, source, target):
        """
        print statement to keep track of disk movement

        :param source:
        :param target:
        :return:
        """
        pass

    @abstractmethod
    def solve(self, disks, source, auxiliary, target):
        """
        solves the Tower of Hanoi using recursion

        :param disks:
        :param source:
        :param auxiliary:
        :param target:
        :return:
        """
        pass