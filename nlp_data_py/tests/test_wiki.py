import pytest
from nlp_data_py import WikiDataset
from nlp_data_py import Book, Splitter


book_def: Book = Book(chunk_splitter='(?<=[.!?]) +', chunks_per_page=2)
splitter: Splitter = Splitter(split_ratios=[0.5, 0.25, 0.25], dataset_names=['train', 'val', 'test'], shuffle=False)
scanned_pickle = "./tests/datasets/scanned_2.pkl"
match = ".*neuro"
save_dataset_path = "./tests/datasets/"


@pytest.fixture
def default_wikidataset():
    return WikiDataset(book_def, splitter, scanned_pickle=scanned_pickle, match=match,
                       save_dataset_path=save_dataset_path, recursive=False)


def test_wiki_handle_contents(default_wikidataset):
    default_wikidataset.handle_contents("Sympathetic_ganglion")
    assert('Neuroblastoma' in default_wikidataset.scanned)
    assert(default_wikidataset.scanned['Neuroblastoma'] == 0)


def test_create_dataset_from_wiki():
    wiki = WikiDataset.create_dataset_from_wiki(seeds=['Brain', 'Human_brain'], match=".*neuro",
                                                recursive=True, limit=2,
                                                scanned_pickle=scanned_pickle,
                                                save_dataset_path=save_dataset_path,
                                                book_def=book_def)
    assert('Brain' in wiki.scanned)
    assert('Human_brain' in wiki.scanned)
    assert(wiki.scanned['Brain'] == 1)
    assert(wiki.scanned['Human_brain'] == 1)
    assert('Motor neuron' in wiki.scanned)




