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
 - **Create Datasets**: Creates train, validation and test datasets in ./vars/ folder. By default, split ratio is 80%, 10% and 10% for train, val and test datasets
 - **Extract Links**: Extracts any link that match the pattern mentioned in -match option. 
 In this example, links that contain neuro or neural are tracked
 - **Read More**: Additional 20 pages from the above "Extract Links" are read and appended to datasets and the links in those pages that match pattern are also tracked.
 - **Track Read**: Pages that are read are tracked and written to a pickle file at ./vars/scanned.pkl.
 This will be useful when the same command is run again. 
 i.e. if the above command is re-run, Brain & Human_brain & 20 pages from "Read More" will not be read again.
 instead, the next 20 pages due to "Extract Links" will be read and appened to datasets in ./vars/
 
#### Command Line Options
## TODO


    


