Create Train, Test and Validation Datasets for NLP from wikipedia

### Installation
## TODO
```
    pip install nlp-data-py
```


### Command line

#### QuickStart 
```
wiki_dataset --seed Brain Human_Brain --match .*neuro|.*neural 
```

In short the above command:
 - **Read Wiki**: Reads Brain and Human_Brain pages from wikipedia
 - **Shuffle**: Shuffles data based on some default criteria 
 (see, chunk_splitter & chunks_per_page for defaults) 
 - **Create Datasets**: Creates train, validation and test datasets in ./vars/ folder. 
 By default, split ratio is 80%, 10% and 10% for train, val and test datasets
 - **Extract Links**: Extracts any link that match the pattern mentioned in -match 
 option. In this example, links that contain neuro or neural are tracked
 - **Read More**: Additional 20 pages from the above "Extract Links" are read 
 and appended to datasets and the links in those pages that match pattern 
 are also tracked.
 - **Track Read**: Pages that are read are tracked and written to a pickle 
 file at ./vars/scanned.pkl. This will be useful when the same command 
 is run again. i.e. if the above command is re-run, Brain & Human_brain 
 & 20 pages from "Read More" will not be read again. Instead, the next 
 20 pages due to "Extract Links" will be read and appened to datasets 
 in ./vars/
 
#### Command Line Options

- --seed or -s
- --match or -m
- --recursive or -r
- --limit or -l
- --pickle or -p
- --output or -o
- --chunk_splitter or -cs
- --chunks_per_page or -cp
- --split_ratio or -sr
- --datasets or -ds
- --shuffle or -sf

##### --seed or -s:
**Description**: List of initial Wiki Page names to start with. 

**Default**: None. If nothing is specified, items in [pickle](#--pickle-or--p) 
file will be read. If pickle file file dose not exists, nothing will be 
done and the code exits.

**Example**: 
```
wiki_dataset --seed Brain Human_Brain
```

##### --match or -m: 
**Description**: This option serves 2 purpose. One to track links in WikiPages 
and another to read additional pages either from links or saved pickle file. 
Links that match the pattern will be considered for current or future reading.
Also see [limit](#--limit-or--l)  

**Default**: "". All links from a wikipage will be considered and tracked.

**Example**: 
```
wiki_dataset --seed Brain Human_Brain -m .*neuro|.*neural
```
In the above example, any links that match *neuro* or *neural* will be tracked 
and/or read to create datasets. 

##### --recursive or -r:
**Description**: If this option is true, then additional pages will be read 
either based on links or previously scanned pickle file. This option will 
be used in conjunction with limit which determines number of additional 
pages to be read.
Also see [limit](#--limit-or--l)


**Default**: true

**Example**: 
```
wiki_dataset --seed Brain Human_Brain -m .*neuro|.*neural -r false
```

In the above example, only Brain and Human_Brain wiki pages will be read. 
However, links that match the match patter in the above pages will be tracked 
and stored in a pickle file which may be useful in future.

##### --limit or -l:

##### --pickle or -p:

##### --output or -o:

##### --chunk_splitter or -cs:

##### --chunks_per_page or -cp:

##### --split_ratio or -sr:

##### --datasets or -ds:

##### --shuffle or -sf:


### Programmatic Usage

Below is a simple example:

```python
from dataset import WikiDataset

WikiDataset.create_dataset_from_wiki(seeds=['Brain', 'Human_brain'], match=".*neuro")

```

Below is an example where default options are overridden:

```python
from dataset import WikiDataset
from commons import Book, Splitter

scanned_pickle = "/User/vars/scanned.pkl"
save_dataset_path = "/User/datasets/"

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

    


