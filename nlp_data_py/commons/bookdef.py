import re
import math
from logging import Logger
from nlp_data_py.commons.utils.logging import Logging


class Book:
    """For managing data spliting, contents are added to Book class. This
    will manage things like spliting the contents, based on delimiter,
    chunking contents into pages. These pages can then be used to create
    train, test and val sets.

    Args:
        chunk_splitter:regular expression. Pattern on which to split the text
        chunks_per_page: int: Number of chunks that make up a page

    Example:
    ::

        book_def: Book = Book(chunk_splitter='(?<=[.!?]) +', chunks_per_page=2)
        book_def.text = "This is. A Simple. Book! That makes. No Sense?"

        println(book_def.num_of_chunks)
        >>> 5
        println(book_def.num_of_pages)
        >>> 3

    """

    def __init__(self, chunk_splitter='(?<=[.!?]) +', chunks_per_page=5):
        self.logger: Logger = Logging.get_logger("Book")
        self.chunk_splitter = chunk_splitter
        self.chunks_per_page = chunks_per_page
        #self.text = ""


    @property
    def text(self):
        """This is content of entire book and has to be set before reading pages.
        Once this property is set, below properties will be availableself.

        chucks: Array[str]: Actual chunks after splitting text on reg_ex

        num_of_chunks: Number of chunks in the book

        num_of_pages: pages in the book. num_of_chunks/chunks_per_page

        """
        return self.__text

    @text.setter
    def text(self, book_text):
        self.__text = book_text
        self.chunks = re.split(self.chunk_splitter, self.text)
        self.num_of_chunks = len(self.chunks)
        self.num_of_pages = math.ceil(float(self.num_of_chunks)/self.chunks_per_page)
        self.logger.debug(f"num_of_chunks: {self.num_of_chunks}")
        self.logger.debug(f"num_of_pages: {self.num_of_pages}")

    def read_page(self, page_number):
        """Reads the content of the page.

        Args:
            page_number: int: Number of the page to be read

        Returns:
            Contents of the asked page

        """
        self.logger.debug(f"Reading Page: {page_number}")
        start_chunk = min(page_number * self.chunks_per_page, self.num_of_chunks)
        self.logger.debug(f"start_chunk: {start_chunk}")
        end_chunk = min((page_number + 1) * self.chunks_per_page, self.num_of_chunks)
        self.logger.debug(f"end_chunk: {end_chunk}")
        return ". ".join(self.chunks[start_chunk:end_chunk])
