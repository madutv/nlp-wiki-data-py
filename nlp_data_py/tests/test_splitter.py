import pytest
from nlp_data_py import Splitter


@pytest.fixture
def default_splitbook():
    splitter = Splitter()
    splitter.num_of_pages = 10
    return splitter


@pytest.fixture
def notshuffled_splitbook():
    splitter = Splitter(split_ratios=[3, 5, 2], dataset_names=['val', 'train'], shuffle=False)
    splitter.num_of_pages=10
    return splitter


@pytest.fixture
def train_only_splitbook():
    splitter = Splitter(split_ratios=[], dataset_names=[], shuffle=False)
    splitter.num_of_pages = 10
    return splitter

@pytest.fixture
def no_test_only_splitbook():
    splitter = Splitter(split_ratios=[8, 2], dataset_names=['train', 'val', 'test'], shuffle=False)
    splitter.num_of_pages = 10
    return splitter


def test_shuffled_page(default_splitbook):
    assert len(default_splitbook.shuffled_pages) == 10


def test_not_shuffled_page(notshuffled_splitbook):
    assert notshuffled_splitbook.shuffled_pages == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_shuffled_ds_to_pages(default_splitbook):
    assert len(default_splitbook.ds_to_pages['train']) == 8
    assert len(default_splitbook.ds_to_pages['val']) == 1
    assert len(default_splitbook.ds_to_pages['test']) == 1


def test_default_name_for_dataset_name(notshuffled_splitbook):
    assert list(notshuffled_splitbook.ds_to_pages.keys()) == ['val', 'train', 'set_2']


def test_pages(notshuffled_splitbook):
    assert notshuffled_splitbook.ds_to_pages['val'] == [0, 1, 2]
    assert notshuffled_splitbook.ds_to_pages['train'] == [3, 4, 5, 6, 7]
    assert notshuffled_splitbook.ds_to_pages['set_2'] == [8, 9]


def test_train_only_pages(train_only_splitbook):
    assert train_only_splitbook.ds_to_pages['train'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_no_test_pages(no_test_only_splitbook):
    assert no_test_only_splitbook.ds_to_pages['train'] == [0, 1, 2, 3, 4, 5, 6, 7]
    assert no_test_only_splitbook.ds_to_pages['val'] == [8, 9]
    assert no_test_only_splitbook.ds_to_pages['test'] == []


