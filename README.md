Create Train, Test and Validation Datasets for NLP from wikipedia. Datasets are created 
using provided seed WikiPages and also by traversing links within pages that meet the 
specified match pattern. Idea is to leverage links within wiki pages to create more data. 
The thought is, wikipedia will already contain links to additional pages that are 
relevant and links within pages can be narrowed through pattern matching.

### Installation
```
    pip install nlp-data-py
```

### Usage
-   [Command line](#command-line)
-   [Programatic](#programmatic-usage) 

### Command line

#### QuickStart Example
```
wiki_dataset --seed Brain Human_Brain --match .*neuro|.*neural 
```

In short the above command:
 - **Read Wiki**: Reads Brain and Human_Brain pages from wikipedia
 - **Shuffle**: Shuffles data based on some default criteria
 (see, [chunk_splitter](#--chunk_splitter-or--cs) & 
 [chunks_per_page](#--chunks_per_page-or--cp) for defaults) 
 - **Create Datasets**: Creates train, validation and test datasets in ./vars/ folder. 
 By default, split ratio is 80%, 10% and 10% for train, val and test datasets
 - **Extract Links**: Extracts any link that match the pattern mentioned 
 in [--match](#--match-or--m) option. In this example, links containing 
 'neuro' or 'neural' are tracked
 - **Read More**: Additional 20 pages from the above "Extract Links" are read 
 and appended to datasets and the links in those pages that match pattern 
 are also tracked.
 - **Track Read**: Pages that are read are tracked and written to a pickle 
 file at ./vars/scanned.pkl. This will be useful when the same command 
 is run again. i.e. if the above command is re-run, Brain & Human_brain 
 & 20 pages from "Read More" will not be read again. Instead, the next 
 20 pages due to "Extract Links" will be read and appended to datasets 
 in ./vars/
 
#### Command Line Options

- [--seed or -s](#--seed-or--s)
- [--match or -m](#--match-or--m)
- [--recursive or -r](#--recursive-or--r)
- [--limit or -l](#--limit-or--l)
- [--pickle or -p](#--pickle-or--p)
- [--output or -o](#--output-or--o)
- [--chunk_splitter or -cs](#--chunk_splitter-or--cs)
- [--chunks_per_page or -cp](#--chunks_per_page-or--cp)
- [--split_ratio or -sr](#--split_ratio-or--sr)
- [--datasets or -ds](#--datasets-or--ds)
- [--shuffle or -sf](#--shuffle-or--sf)

#### --seed or -s:
`Description`: List of initial Wiki Page names to start with. 

`Default`: None. If nothing is specified, items in [pickle](#--pickle-or--p) 
file will be read. If pickle file also dose not exists, nothing will be done and 
the code exits.

`Example`: 
```
wiki_dataset --seed Brain Human_Brain
```

#### --match or -m: 
`Description`: This option serves 2 purpose. One to track links in WikiPages 
and another to read additional pages either from links or [saved pickle](#--pickle-or--p) 
file. Links that match the pattern will be considered to be added to datasets.
Also see [limit](#--limit-or--l)  

`Default`: "". All links from a wikipage will be considered and tracked.

`Example`: In the below example, any links that match *neuro* or *neural* will be tracked 
and/or read to create datasets. 

```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural"
```

#### --recursive or -r:
`Description`: If this option is true, then additional pages will be read 
either based on links or previously scanned pickle file. This option will 
be used in conjunction with limit to determine number of additional 
pages to read.
Also see [limit](#--limit-or--l)


`Default`: true

`Example`: In the below example, only Brain and Human_Brain wiki pages will be read. 
However, links that match the match patter from these pages will be tracked 
and stored in a pickle file which may be used later on.

```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -r false
```

#### --limit or -l:
`Description`: Wikipedia may contain too many links especially when looking 
at pages recursively. This option limits the number of additional pages to be read.
This option will only be relevant if recursive is set to true.

`Default` 20

`Example`: In the below example, along with reading Brain & Human_Brain 
and tracking links that match the match pattern, 100 additional pages 
are read either based on links or [pickle file](#--pickle-or--p).

```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -l 100
```

#### --pickle or -p:
`Description`: Path to pickle file tracking items that are read. This enables to 
incrementally read items. Pickle file stores a dict. Example:
```
    {
        "item1": 1,
        "item2": 0,
        "item3": -1
    }
```
            
In the above example, item1 was read previously hence, wont be read again. item2 was 
not read and will be consider in future reads. item3 errored out in previous reads 
and will not be attempted again

`Default`: ./vars/scanned.pkl

`Example`:
```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -p scanned.pkl
```
In the above example:
-   Brain & Human_Brain and 20 pages matching pattern are read and stored as read 
    in the pickle file. Any additional links that were not read due to reaching
    the limit will be stored as unread in the pickle file
-   If the above command is re-run, all the read pages including seed will not
    be read again. Instead, additional unread pages from pickle file will
    be read and pickle file will be updated to track read pages and any additional
    links that were encountered in the newly traversed pages

#### --output or -o:
`Description`: Path for datasets. 

`Default`: ./vars/datasets/

`Example`: 
```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -o ./datasets/
```
In the above example, train, val and test datasets will be created in datasets/
folder. Future re-runs will append to these files


#### --chunk_splitter or -cs: 
`Description`: This option, along with [chunks_per_page](#--chunks_per_page-or--cp) 
defines a page. This comes in handy when creating datasets, especially, if the 
data needs to be shuffled.

`Default`: '(?<=[.!?]) +'

`Example`:
```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -cs '(?<=[.!?]) +'
```
In the above example, text from wiki pages are split into sentences (chunks) based on ., ! or ?

#### --chunks_per_page or -cp:
`Description`: This defines pages. i.e. this defines number of chunks for a page. 
This comes in handy when data needs to be shuffled for creating test, train and val datasets.

`Default`: 5

`Example`:
```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -cs '(?<=[.!?]) +' -cp 10
```

In the above example, wiki page is split into chunks based on ., ? or !. And 10 contiguous 
chunks form a page. For example, if wiki page has 100 sentences, in the above example,
groups of 10s are considered to form a page. So, this wiki page contain 10 pages.  

#### --split_ratio or -sr:
`Description`: Ratio to split the train, val and test datasets. Split happens based on
number of pages. 

`Default`: 80%, 10% and 10% for train, val and test

`Example`:
```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -cs '(?<=[.!?]) +' -cp 10 -sr .8 0.1 0.1
```

If a wiki page has 10 pages (as defined by [chuck_splitter](#--chunk_splitter-or--cs) and 
[chunks_per_page](#--chunks_per_page-or--cp)), then in the above example, train will contain
8, val and test will contain 1 each. Note that the actual page in each of these datasets depend
on if [shuffle](#--shuffle-or--sf) is on. If shuffle is on, pages are shuffled and any 8 page
can make train dataset and any of the remaining 2 pages can be val and test. If shuffle is 
off, then first 8 pages will be train, next 1 is val and final page is test

#### --datasets or -ds:

`Description`: Names the datasets

`Default`: train, val and test

`Example`:
```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -sr 80 20 -ds set1 set2 
```
In the above example, 2 datasets: set1 & set2 will be created

#### --shuffle or -sf:
`Description`: Shuffle pages (see [chuck_splitter](#--chunk_splitter-or--cs) and 
[chunks_per_page](#--chunks_per_page-or--cp) for pages) before creating datasets

`Default`: True

`Example`:
```
wiki_dataset --seed Brain Human_Brain -m ".*neuro|.*neural" -sf false
```

Since shuffle is false in the above example, pages in wiki page will be taken in order. i.e.
since default ratio is 80%, 10% and 10%, first 80% of this wiki page will be in train, next 10%
in val and final 10% in test.

Actual pages in each of the datasets depend on if shuffle is on. 
If shuffle is on, pages are shuffled and any 80% page can make train dataset 
and any of the remaining 20% pages can be val and test. 
If shuffle is off, then first 80% will be train, next 10% val and final 10% is test



### Programmatic Usage

Below is a simple example:

```python
from nlp_data_py import WikiDataset

WikiDataset.create_dataset_from_wiki(seeds=['Brain', 'Human_brain'], match=".*neuro")

```
In the above example,
- Brain will be read from wikipedia
- contents will be broken to pages as defined by default book. ([chuck_splitter](#--chunk_splitter-or--cs) and 
[chunks_per_page](#--chunks_per_page-or--cp))
- pages will be shuffled
- pages will be split as defined by default splitter 
([split_ratio](#--split_ratio-or--sr), [datasets](#--datasets-or--ds), [shuffle](#--shuffle-or--sf))
- links will be extracted from the page
- links matching patter in match (in this case links containing 'neuro')
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


Below is an example where default options are overridden:

```python
from nlp_data_py import WikiDataset
from nlp_data_py import Book, Splitter

scanned_pickle = "./scanned.pkl"
save_dataset_path = "./datasets/"

book_def: Book = Book(chunk_splitter='(?<=[.!?]) +', chunks_per_page=2)
splitter: Splitter = Splitter(split_ratios=[0.5, 0.25, 0.25], dataset_names=['train', 'val', 'test'], shuffle=False)

wiki = WikiDataset.create_dataset_from_wiki(seeds=['Brain', 'Human_brain'], 
                                            match=".*neuro",
                                            recursive=True, limit=2,
                                            scanned_pickle=scanned_pickle,
                                            save_dataset_path=save_dataset_path,
                                            book_def=book_def,
                                            splitter=splitter)

```

    


