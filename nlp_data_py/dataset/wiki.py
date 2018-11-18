import wikipedia
from itertools import count
from nlp_data_py.commons.bookdef import Book
from nlp_data_py.commons.splitter import Splitter
from nlp_data_py.dataset.dataset import Dataset


class WikiDataset(Dataset):
    """Create datasets such as train, test and val from wikipedia. This is an
    implemention of Dataset class

    Args:

        book_def: Book. This object defines a book. Default is
            5 sentences per page. Each sentence is by default defined
            as string ending in . ! or ?

        splitter: Splitter: Defines how to split datasets.
            Default is to create train, val and test sets in the
            ratio of 80%, 10% & 10% respectively. Also, by default
            shuffle is set to true. With shuffle set to true, pages,
            as defined by book_def will be shuffled before creating
            datasets

        seeds: List of dataset pages. If seeds are specified and recursive
            is false, only items in seeds will be read.
            If seeds are specified and recursive is True, seeds will be
            read first and then additional pages upto limit will be read

        match: regular expression as string. Only items matching
            regular expression will be read for creating datasets

        recursive: Boolean: Default True. This flag indicates if
            additional should be read or tracked.
            i.e. Links in the wikipages will be tracked extracted and
            tracked in scanned variable which will then be written to
            pickle file

        limit: int: default 20. Number of additional pages to be
            read in addition to seeds. These pages are read from
            self.scanned variable

        scanned_pickle: Path to pickle file tracking items that are
            read. This enables to incrementally read items. Pickle file
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

        save_dataset_path: Path to folder where the datasets will
            be saved.

    """

    def __init__(self, book_def, splitter, seeds=[], match="", recursive=True,
                       limit=20, scanned_pickle="./vars/scanned.pkl",
                       save_dataset_path="./vars/"):

        super(WikiDataset, self).__init__("WikiDataset", scanned_pickle, match,
                                          save_dataset_path, book_def=book_def, splitter=splitter, )
        self.seeds = seeds
        self.recursive = recursive
        self.limit = limit

    @classmethod
    def create_dataset_from_wiki(cls, seeds=[], match="", recursive=True,
                                 limit=20, scanned_pickle="./vars/scanned.pkl",
                                 save_dataset_path="./vars/",
                                 book_def: Book = Book(chunk_splitter='(?<=[.!?]) +', chunks_per_page=5),
                                 splitter: Splitter = Splitter(split_ratios=[0.8, 0.1, 0.1],
                                                    dataset_names=['train', 'val', 'test'], shuffle=True)):

        """class method to read from wikipedia anc create datasets

        Args:

            seeds: List of dataset pages. If seeds are specified and recursive
                is false, only items in seeds will be read.
                If seeds are specified and recursive is True, seeds will be
                read first and then additional pages upto limit will be read

            match: regular expression as string. Only items matching
                regular expression will be read for creating datasets

            recursive: Boolean: Default True. This flag indicates if
                additional should be read or tracked.
                i.e. Links in the wikipages will be tracked extracted and
                tracked in scanned variable which will then be written to
                pickle file

            limit: int: default 20. Number of additional pages to be
                read in addition to seeds. These pages are read from
                self.scanned variable

            scanned_pickle: Path to pickle file tracking items that are
                read. This enables to incrementally read items. Pickle file
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

        Example:

            create_dataset_from_wiki(['Brain', 'Medulla_oblongata'])

            In the above example,
                - Brain will be read from wikipedia
                - contents will be broken to pages as defined by default book
                - pages will be shuffled
                - pages will be split as defined by default splitter
                - links will be extracted from the page
                - links matching patter in match (in this case all links)
                  will be added to self.scanned if they are not already there
                - Brain will be set to 1 in self.scanned to indicate that this
                  page is already read
                - same steps are repeated with 'Medulla_oblongata'
                - since recursive is set to true, and limit is 20, next
                  20 unread items from self.scanned will be read and their
                  links will be tracked in self.scanned
                - finally self.scanned is written to a pickle file
                - if the same code is run again, pickle file will be read
                  and since Brain and Medulla oblangata are already read,
                  they will be skipped and next 20 items from self.scanned
                  are read


        """

        ds_wiki = cls(book_def, splitter, seeds, match, recursive, limit, scanned_pickle, save_dataset_path)

        filtered_seed = filter(lambda a: a not in ds_wiki.scanned or ds_wiki.scanned[a] == 0, seeds)
        for seed in filtered_seed:
            ds_wiki.handle_contents(seed)
        if recursive:
            to_scan = list(filter(lambda a, c=count(): a[1] == 0 and next(c) < ds_wiki.limit, ds_wiki.scanned.items()))
            for item in to_scan:
                ds_wiki.handle_contents(item[0])
        #print(f"self.scanned[seed] {ds_wiki.scanned}")
        ds_wiki.write_scanned_tracker()
        return ds_wiki

    def handle_contents(self, seed):

        """This method is responsible for reading contents from wikipedia,
        extracting links from page, adds links to self.

        """
        try:
            #print(f'*******seed********* {seed}')
            self.scanned[seed] = 1
            w_page = wikipedia.WikipediaPage(seed)
            self.generate_datasets(w_page.content)
            scanable_links = list(self.filter_scannable(w_page.links))
            #print(f"scanable_links {scanable_links}")
            for s in scanable_links:
                if s not in self.scanned:
                    self.scanned[s] = 0
        except Exception as e:
            #print(f'Failed to read {seed} {e}')
            self.scanned[seed] = -1