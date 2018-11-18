
seed_help = "List of wiki pages to start with. This has to be " \
            "provided as comma seperated string like so 'seed1, seed2'"

match_help = "Regular expression. Only wiki pages that match this criteria " \
             "will be included in train, test and val datasets."

recursive_help = "If this flag is set, links in wiki page will be read " \
                 "recursively upto limit times. Default is True. " \
                 "For example: if the seed is 'Brain' and limit is 20, " \
                 "20 additional pages that match the match criteria will be read. " \
                 "These additional pages are from the links in seed and their child pages. " \
                 "Also see, --match, --limit"

limit_help = "Number of additional pages to be read. These pages are either " \
             "picked from pickle file or from links in previous pages. " \
             "Note that for this argument to take effect only if --recursive is true. " \
             "(It is by default). If this argument is not provided, " \
             "it will be defaulted to 20. Also see, --match, --recursive, --pickle"

pickle_help = "Path to pickle file tracking items that are read. " \
              "This enables to incrementally read items. Pickle file stores a dict. " \
              "Example: {'item1' : 1, 'item2': 0, 'item3': -1} " \
              "In the above example, item1 was read previously hence, wont " \
              "be read again. item2 was not read and will be consider in " \
              "future reads. item3 errored out in previous reads and will " \
              "be attempted to read again "

output_help = "Path to store the datasets"

chunk_splitter_help = "This, along with chunks_per_page defines a book. Regular expression " \
                      "to split book to chunks. Default is '(?<=[.!?]) +'. This will split " \
                      "text based on either a ., ! or ? "

chunks_per_page_help = "This, along with chunk_splitter defines a book. Default value is 5." \
                       "This mean 5 chunks make a page. "

split_ratio_help = "This, along with datasets defines the datasets and their ratios." \
                   "Default is 0.8, 0.1 & 0.1 for train, val and test respectively"


datasets_help = "This, along with split_ratio defines the datasets and their ratios." \
                   "Default is train, val and test with a ratio of 0.8, 0.1 and 0.1 respectively"

shuffle_help = "If true, Shuffles book pages (see chunk_splitter and chunks_per_page for book definitions " \
               "before creating datasets. Default is true"



