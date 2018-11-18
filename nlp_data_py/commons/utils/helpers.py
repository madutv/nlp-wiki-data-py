import numpy as np
from typing import List
from logging import Logger
from nlp_data_py.commons.utils.logging import Logging


class Helpers:
    """Generic helper methods.

    """
    logger: Logger = Logging.get_logger("Helpers")

    @staticmethod
    def generate_random_shuffle(length: int):
        """Randomly shuffles the range from 0 to given length

        Args:
            length: Length for range

        Returns:
            Shuffled list of length = length

        Example:
        ::

            generate_random_shuffle(10) may produce
            shuffled list rangning from 0 and 9

        """
        Helpers.logger.debug(f"Params: {length}")
        shuffled = np.random.permutation(range(0, length))
        Helpers.logger.debug(f"Shuffled: {shuffled}")
        return shuffled

    @staticmethod
    def normalize_ratios(ratio_list: List):
        """Softmax of list.

        Args:
            ratio_list: List of numbers

        Returns:
            Softmaxed list

        Example:
        ::

            normalize_ratios([8, 2, 2]) will produce
            [0.8, 0.2, 0.2]

        """
        Helpers.logger.debug(f"Params: {ratio_list}")
        density = float(sum(ratio_list))
        normalized = [r/density for r in ratio_list]
        Helpers.logger.debug(f"Density: {density} Normalized: {normalized}")
        return normalized

    @staticmethod
    def extend_list(lst: List, ext_with, times):
        """Extends given list with elements. This is with
        side effects

        Args:
            lst (List): List to be extended
            ext_with (Any): Element with which to extend
                the list
            times (Int): ext_with with be added to list
                times times

        Returns:
            None

        Example:
        ::

            extend_list([1,2,3], 0, 5) will produce [1, 2, 3, 0, 0, 0, 0, 0]

        """

        Helpers.logger.debug(f"Params: {lst} {ext_with} {times}")
        lst.extend([ext_with] * times)

    @staticmethod
    def extend_shorter_list(list1: List, list2: List, ext_with):
        """Compares 2 lists and extends the shorter with to
        longer ones length. Shorter list is extended by the
        element provided in ext_with parameter

        Args:
            list1 (List): First list
            list2 (List): Second list
            ext_with (Any): Element with which to extend
                the list

        Returns:
            None

        Example:
        ::

            extend_shorter_list([1,2,3], [1, 2], 0) will
            produce keep first the same but changes 2nd one to [1, 2, 0]

        """

        diff = len(list1) - len(list2)
        Helpers.logger.debug(f"Diff between {list1} and {list2}: {diff}")
        if diff < 0:
            Helpers.extend_list(list1, ext_with, abs(diff))
        else:
            Helpers.extend_list(list2, ext_with, abs(diff))

    @staticmethod
    def extend_shorter_lists(lists: [List[List]], ext_with):
        """Compares lists of lists and extends shorter lists with
        ext_with to match the length of largest list.

        Args:
            lists (List[List]): List of lists
            ext_with (Any): Element with which to extend the list

        Returns:
            None

        Example:
        ::

            list1 = [1, 3, 4, 5, 8]
            list2 = [1, 3]
            list3 = [5]
            list4 = [3, 4, 2, 2, 2]
            Helpers.extend_shorter_lists([list1, list2, list3, list4], 9)
            assert list1 == [1, 3, 4, 5, 8]
            assert list2 == [1, 3, 9, 9, 9]
            assert list3 == [5, 9, 9, 9, 9]
            assert list4 == [3, 4, 2, 2, 2]

        """

        lengths = [len(l) for l in lists]
        Helpers.logger.debug(f"Lengths of all list: {lengths}")
        max_length = max(lengths)
        for i, l in enumerate(lengths):
            if l < max_length:
                Helpers.extend_list(lists[i], ext_with, max_length - l)




