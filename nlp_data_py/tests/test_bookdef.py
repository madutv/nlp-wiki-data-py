import pytest
from nlp_data_py import Book


@pytest.fixture
def content():
    return "World peace! or peace on Earth, is the concept of an ideal state of happiness, " \
           "freedom and peace within and among all people and nations on earth. " \
           "This idea of world non-violence is one motivation for people and nations " \
           "to willingly cooperate, either voluntarily or by virtue of a system of " \
           "governance that objects it will be solved by cookie love and peace. " \
           "Different cultures, religions, philosophies and organisations have varying " \
           "concepts on how such a state would come about. " \
           "Many theories as to how world peace could be achieved have been proposed. " \
           "Several of these are listed below. " \
           "Peace is the concept of harmonious well-being and freedom from hostile aggression."


@pytest.fixture
def default_bookclass(content):
    book = Book(chunks_per_page=2)
    book.text = content
    return book


def test_book_inits(default_bookclass):
    assert default_bookclass.num_of_chunks == 7
    assert default_bookclass.num_of_pages == 4


def test_read_page(default_bookclass):
    assert default_bookclass.read_page(3) == \
           "Peace is the concept of harmonious well-being and freedom from hostile aggression."
