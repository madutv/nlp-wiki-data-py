from typing import List
import math
from nlp_data_py.commons.utils.helpers import Helpers
from nlp_data_py.commons.utils.logging import Logging
from logging import Logger


class Splitter:
    """Splits pages in a book to datasets. This class will simple determine
    what page numbers make each datasets.

    Args:
        num_of_pages: Book.
        split_ratios: ratio to split the book. Default
            ratio is 90% train, 5% val and 5% test
        dataset_names: dataset names to be split to
        shuffle: shuffle pages

    Properties:
        ds_to_pages: Contains the dict of datasets and page number in
        each of the datasets.

    Example:
    ::

        splitter: Splitter = Splitter(split_ratios=[0.8, 0.1, 0.1], dataset_names=['train', 'val', 'test'], shuffle=True)
        splitter.num_of_pages = 10

        print(splitter.shuffled_pages)
        >>> [4, 3, 1, 0, 8, 6, 9, 7, 2, 5]
        print(splitter.ds_to_page)
        >>> {
                'train': [4, 3, 1, 0, 8, 6, 9, 7]
                'val': [2]
                'test': [5]
            }

    """
    logger: Logger = Logging.get_logger("SplitBook")

    def __init__(self,
                 split_ratios: List[float]=[0.8, 0.1, 0.1],
                 dataset_names: List[str]=['train', 'val', 'test'],
                 shuffle=True):
        self.split_ratios = split_ratios
        self.dataset_names = dataset_names
        self.shuffle = shuffle
        #self.num_of_pages = 0


    @property
    def num_of_pages(self):
        """Number of pages for splitting. Once num_of_pages is set ds_to_page dict will be availabe.

        ds_to_pages: Contains the dict of datasets and page number in each of the datasets.

        """

        return self.__num_of_pages

    @num_of_pages.setter
    def num_of_pages(self, numberofpages):
        self.__num_of_pages = numberofpages
        self.shuffled_pages = self.__num_of_pages
        self.ds_to_pages = self.pages_to_datasets()
        self.logger.debug(f"ds_to_pages: {self.ds_to_pages}")

    @property
    def shuffled_pages(self):
        """List of shuffled page number if shuffle is true, else just ordered page numbers.

        """

        return self.__shuffled_pages

    @shuffled_pages.setter
    def shuffled_pages(self, num_of_pages):
        if self.shuffle:
            self.__shuffled_pages = Helpers.generate_random_shuffle(num_of_pages)
        else:
            self.__shuffled_pages = list(range(0, num_of_pages))

    @staticmethod
    def match_splitratios_and_datasetnames(split_ratios=[], dataset_names=[]):
        """If parameters passed to split and datasets are not even, this expands
        the shorter one. If the dataset_name is shorter, it creates default
        dataset name as 'set_{position of missing item}. If ratio is shorter
        its set to 0 and no pages for it are created

        Args:
            split_ratios: list of ratios for pages
            dataset_names: list of names for the datasets

        Returns:
            Normalized ratio and datasetnames

        """
        if len(split_ratios) == len(dataset_names) == 0:
            split_ratios = [1]
            dataset_names = ['train']
        Helpers.extend_shorter_list(split_ratios, dataset_names, 0)
        dataset_names = ["set_" + str(i) if ds == 0 else ds for i, ds in enumerate(dataset_names)]
        return Helpers.normalize_ratios(split_ratios), dataset_names

    def pages_to_datasets(self):
        """creates a dict of dataset names and page numbers.

        Example:
        ::

            This returns somethings like
            {
               "train": [0, 1, 4, 8, 9, 3, 6]
               "val" : [2, 5]
               "test": [7]
            }
            In the above example, train set will contain pages in its list
            and so on for val and test

        """

        self.split_ratios, self.dataset_names = Splitter.match_splitratios_and_datasetnames(self.split_ratios, self.dataset_names)
        num_of_pages = len(self.shuffled_pages)
        pages_per_ds = [math.ceil(num_of_pages * r) for r in self.split_ratios]
        self.logger.debug(f"pages_per_ds: {pages_per_ds}")
        start = 0
        pages_to_ds = {}
        for p, d in zip(pages_per_ds, self.dataset_names):
            end = max(0, min(start + p, num_of_pages))
            pages_to_ds[d] = self.shuffled_pages[start:end]
            start = max(0, min(start + p, num_of_pages - 1))
        return pages_to_ds



