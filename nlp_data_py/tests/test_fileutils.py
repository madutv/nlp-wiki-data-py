import pytest
from nlp_data_py import FileUtils
import os


@pytest.fixture
def default_file():
    return './temp_test.txt'

@pytest.fixture
def default_texts():
    return ('World Peace', ' World Peace!')


@pytest.fixture
def default_remove_file():
    def remove_file(file):
        try:
            os.remove(file)
        except Exception as e:
            print("There was an exception while removing file")
            print(e)
    return remove_file

@pytest.fixture
def pickle_file():
    return './temp.pkl'


def test_write_content_tofile_empty_file(default_file, default_texts):
    FileUtils.write_content_tofile(default_texts[0], default_file)
    content = FileUtils.read_file(default_file)
    assert content == default_texts[0]


def test_write_content_tofile(default_file, default_texts, default_remove_file):
    FileUtils.write_content_tofile(default_texts[1], default_file)
    content = FileUtils.read_file(default_file)
    assert content == default_texts[0] + default_texts[1]
    default_remove_file(default_file)


def test_file_exist(default_file):
    assert FileUtils.file_exist(default_file) == False


def test_read_write_pickle(pickle_file):
    write_dic = {"a": 1, "b": 2}
    FileUtils.write_pickle(write_dic, pickle_file)
    read_dic = FileUtils.read_pickle(pickle_file)
    assert write_dic == read_dic


def test_file_exist_true(default_remove_file, pickle_file):
    assert FileUtils.file_exist(pickle_file) == True
    default_remove_file(pickle_file)