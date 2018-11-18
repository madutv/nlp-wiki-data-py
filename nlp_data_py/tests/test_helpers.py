from nlp_data_py import Helpers


def test_generate_random_shuffle():
    shuffled = Helpers.generate_random_shuffle(10)
    assert len(shuffled) == 10


def test_normalize_ratios():
    assert Helpers.normalize_ratios([80, 10, 10]) == [.8, .1, .1]


def test_extend_list():
    lst = [1, 2, 3]
    Helpers.extend_list(lst, 0, 5)
    assert [1, 2, 3, 0, 0, 0, 0, 0] == lst


def test_same_length_extend_shorter_list():
    list1 = [1, 2, 3]
    list2 = [0, 3, 4]
    Helpers.extend_shorter_list(list1, list2, 0)
    assert list1 == [1, 2, 3]
    assert list2 == [0, 3, 4]


def test_list1_shorter_extend_short_list():
    list1 = [1, 2]
    list2 = [0, 3, 4]
    Helpers.extend_shorter_list(list1, list2, 0)
    assert list1 == [1, 2, 0]
    assert list2 == [0, 3, 4]


def test_list2_shorter_extend_short_list():
    list1 = ['1', '2', '4', 'L']
    list2 = ['0']
    Helpers.extend_shorter_list(list1, list2, 'Peace')
    assert list1 == ['1', '2', '4', 'L']
    assert list2 == ['0', 'Peace', 'Peace', 'Peace']


def test_lists_extend_shorter_lists():
    list1 = [1, 3, 4, 5, 8]
    list2 = [1, 3]
    list3 = [5]
    list4 = [3, 4, 2, 2, 2]
    Helpers.extend_shorter_lists([list1, list2, list3, list4], 9)
    assert list1 == [1, 3, 4, 5, 8]
    assert list2 == [1, 3, 9, 9, 9]
    assert list3 == [5, 9, 9, 9, 9]
    assert list4 == [3, 4, 2, 2, 2]


