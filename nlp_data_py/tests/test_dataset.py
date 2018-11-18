from nlp_data_py import WikiDataset
from nlp_data_py import Book, Splitter, FileUtils


default_txt_book = "World peace! or peace on Earth, is the concept of an ideal state of happiness, " \
           "freedom and peace within and among all people and nations on earth. " \
           "This idea of world non-violence is one motivation for people and nations " \
           "to willingly cooperate, either voluntarily or by virtue of a system of " \
           "governance that objects it will be solved by cookie love and peace. " \
           "Different cultures, religions, philosophies and organisations have varying " \
           "concepts on how such a state would come about. " \
           "Many theories as to how world peace could be achieved have been proposed. " \
           "Several of these are listed below. " \
           "Peace is the concept of harmonious well-being and freedom from hostile aggression."

book_def: Book = Book(chunk_splitter='(?<=[.!?]) +', chunks_per_page=2)
splitter: Splitter = Splitter(split_ratios=[0.5, 0.25, 0.25], dataset_names=['train', 'val', 'test'], shuffle=False)
scanned_pickle = "./tests/datasets/scanned.pkl"
match = ".*psych|.*limbic"
save_dataset_path = "./tests/datasets/"
wiki_dataset = WikiDataset(book_def, splitter, scanned_pickle=scanned_pickle, match=match, save_dataset_path=save_dataset_path)
wiki_dataset.generate_datasets(default_txt_book)


def test_book_setup():
    assert(wiki_dataset.book_def.chunks_per_page == 2)


def test_splitter_setup():
    assert(wiki_dataset.splitter.split_ratios == [0.5, 0.25, 0.25])


def test_check_scanned_pickle():
    wiki_dataset.load_scanned_tracker()
    if FileUtils.file_exist(wiki_dataset.scanned_pickle):
        assert(wiki_dataset.scanned == {"world": True, "peace": True})
    else:
        assert(wiki_dataset.scanned == {})


def test_save_scanned_tracker():
    wiki_dataset.scanned = {"world": True, "peace": True}
    wiki_dataset.write_scanned_tracker()
    assert (wiki_dataset.load_scanned_tracker() == {"world": True, "peace": True})


def test_filter_scannable():
    filtered = list(wiki_dataset.filter_scannable(["brain", "limbic system", "word", "limbic connections"]))
    assert(filtered == ["limbic system", "limbic connections"])


def test_dataset_text_is_set():
    assert(wiki_dataset.book_def.text == default_txt_book)


def test_dataset_num_pages_is_set():
    assert (wiki_dataset.book_def.num_of_pages == 4)


def test_dataset_splits():
    assert(len(wiki_dataset.splitter.ds_to_pages['train']) == 2)
    assert (len(wiki_dataset.splitter.ds_to_pages['val']) == 1)
    assert (len(wiki_dataset.splitter.ds_to_pages['test']) == 1)









"""
def test_create_dataset_from_wiki():
    dataset = WikiDataset.create_dataset_from_wiki( seeds=['Brain', 'Medulla_oblongata', 'Pons', 'Hypothalamus', 'Thalamus',
                                                        'Cerebellum', 'Superior_colliculus', 'Pallium_(neuroanatomy)',
                                                        'Hippocampus', 'Basal_ganglia', 'Olfactory_bulb', 'Medulla_oblongata',
                                                        'Dendrite', 'Neuroplasticity', 'Synapse'],
                                                 match=".*psych|.*limbic|.*epilepsy|.*nerves|.*axon|.*gyrus|.*cephalon|.*colliculus|.*brain|.*neuro|.*cortex|.*glia|.*thalmus|.*lobe|.*colliculus",
                                                 recursive=True,
                                                 limit=100,
                                                 scanned_pickle="./var/scanned.pkl",
                                                 datasets=['train', 'test', 'val'],
                                                 split_ratio=[.8, 0.1, 0.1],
                                                 shuffle=True,
                                                 save_dataset_path="./vars/")
    print(dataset.scanned)
"""