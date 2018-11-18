import argparse
from nlp_data_py.commons.bookdef import Book
from nlp_data_py.commons.splitter import Splitter
from nlp_data_py.dataset.wiki import WikiDataset
from nlp_data_py.dataset.constants import *

def wiki_dataset():
    parser = argparse.ArgumentParser(prog='nlp_data_py')

    parser.add_argument('-s', '--seed', nargs='*', default=[], help=seed_help)
    parser.add_argument('-m', '--match', type=str, default="", help=match_help)
    parser.add_argument('-r', '--recursive', type=str2bool, default=True,  help=recursive_help)
    parser.add_argument('-l', '--limit', type=int, default=20, help=limit_help)
    parser.add_argument('-p', '--pickle', type=str, default="./vars/scanned.pkl", help=pickle_help)
    parser.add_argument('-o', '--output', type=str, default="./vars/", help=output_help)
    parser.add_argument('-cs', '--chunk_splitter', type=str, default='(?<=[.!?]) +', help=chunk_splitter_help)
    parser.add_argument('-cp', '--chunks_per_page', type=int, default=5, help=chunks_per_page_help)

    parser.add_argument('-sr', '--split_ratio', nargs="*", type=float, default=[0.8, 0.1, 0.1], help=split_ratio_help)
    parser.add_argument('-ds', '--datasets', nargs="*", default=["train", "val", "test"], help=datasets_help)
    parser.add_argument('-sf', '--shuffle', type=str2bool, default=True, help=shuffle_help)

    args = parser.parse_args()

    ins = {'seed': args.seed,
            'match': args.match,
            'recursive': args.recursive,
            'limit': args.limit,
            'pickle': args.pickle,
            'output': args.output,
            'chunk_splitter': args.chunk_splitter,
            'chunks_per_page': args.chunks_per_page,
            'split_ratio': args.split_ratio,
            'datasets': args.datasets,
            'shuffle': args.shuffle
           }

    print(f"Ins: {ins}")


    wiki = WikiDataset.create_dataset_from_wiki(seeds=ins['seed'],
                                                 match=ins['match'],
                                                 recursive=ins['recursive'],
                                                 limit=ins['limit'],
                                                 scanned_pickle=ins['pickle'],
                                                 save_dataset_path=ins['output'],
                                                 book_def=Book(ins['chunk_splitter'], ins['chunks_per_page']),
                                                 splitter=Splitter(ins['split_ratio'], ins['datasets'], ins['shuffle']))
    print(wiki.scanned)



def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

