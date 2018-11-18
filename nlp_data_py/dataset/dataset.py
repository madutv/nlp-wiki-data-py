import re
from abc import abstractmethod
from nlp_data_py.commons.bookdef import Book
from nlp_data_py.commons.splitter import Splitter
from nlp_data_py.commons.utils.fileutils import FileUtils as fu


class Dataset:
    """Abstract class to create datasets like train, test and val

    Args:
        scanned_pickle: Path to pickle file tracking items that are read.
            This enables to incrementally read items. Pickle file
            stores a dict. Example:
            {
                    "item1": 1,
                    "item2": 0,
                    "item3": -1
            }
            In the above example, item1 was read previously hence, wont
            be read again. item2 was not read and will be consider in
            future reads. item3 errored out in previous reads and will
            be attempted to read again


        match: regular expression as string. Only items matching
            regular expression will be read for creating datasets

        save_dataset_path: Path to folder where the datasets will
            be saved.

        book_def: Book. This object defines a book. Default is
            5 sentences per page. Each sentence is by default defined
            as string ending in . ! or ?

        splitter: Splitter: Defines how to split datasets.
            Default is to create train, val and test sets in the
            ratio of 80%, 10% & 10% respectively. Also, by default
            shuffle is set to true. With shuffle set to true, pages,
            as defined by book_def will be shuffled before creating
            datasets


    Once the datasets are created, the items that are covered is
    tracked as self.scanned. This is written to a pickle file. This
    helps in continuing to update dataset at a latter point in time


    """

    def __init__(self, name, scanned_pickle, match,  save_dataset_path,
                 book_def: Book, splitter: Splitter):

        self.name = name
        self.scanned_pickle = scanned_pickle
        self.match = match
        self.save_dataset_path = save_dataset_path
        self.book_def = book_def
        self.splitter = splitter
        self.scanned = self.load_scanned_tracker()
        self.reg = re.compile(match, re.IGNORECASE)
        fu.mkdir(self.save_dataset_path)

    @abstractmethod
    def handle_contents(self, seed):
        """Abstract method that handles contents of items. This mainly
        includes creating datasets

        """
        pass

    def load_scanned_tracker(self):
        """checks if scanned_pickle file is provided. If so, its read
        and contents are returned. Otherwise and empty dict is returned

        Returns:
            dict of scanned items or empty dict.

        """
        if self.scanned_pickle and fu.file_exist(self.scanned_pickle):
            return fu.read_pickle(self.scanned_pickle)
        else:
            return {}

    def write_scanned_tracker(self):
        """write self.scanned which is tracking items for this run
        into a pickle file

        """
        if self.scanned_pickle:
            fu.write_pickle(self.scanned, self.scanned_pickle)

    def filter_scannable(self, items):
        """filters items that meet the criteria for creating this dataset.
        For the item to meet the criteia, it should match the regular exp
        specified. And it should be an unread item as tracked by self.scanned

        Args:
            items: List of items to be considered for scanning.

        Returns:
            items that meet the criteria.

        """
        return filter(lambda a: self.reg.match(a) and (a not in self.scanned or self.scanned[a] == 0), items)

    def generate_datasets(self, text):
        """Main method for creating datasets. This method takes care of:
            - splitting text as defined by book and splitter.
            - writting the contents into datasets such as train, test and val

        """
        self.book_def.text = text
        self.splitter.num_of_pages = self.book_def.num_of_pages
        splits = self.splitter.ds_to_pages
        for ds_name, page in splits.items():
            fu.write_content_tofile("\n".join([self.book_def.read_page(p) for p in page]),
                                    self.save_dataset_path + ds_name + '.txt')

