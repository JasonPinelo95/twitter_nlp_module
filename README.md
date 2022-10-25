# This is the NLP module to process the tweets and extract the sentiment

## Pre-requisites
* Create a virtual machine on Google Cloud Platform with Ubuntu 18.04

* Install Pyenv, you can use the next script to do so https://raw.githubusercontent.com/JasonPinelo95/cassandra_workshop/main/installPy.sh

* Create three virtual environments, one for each folder "extraction", "transform" and "load"

* Install the requirements for each folder, for extract and load you should install pandas and the bigquery module with the next command:
```pip install pandas google-cloud-bigquery```

* For the transform folder you should install the next modules:
```pip install pandas nltk spacy```

* You should also download the next models for spacy:
```python -m spacy download en_core_web_sm```

* You should also download the next models for nltk:
```python -m nltk.downloader stopwords```

* Generate your credentials for bigquery and put them in the folder "load" with the name "credentials.json"

* You should also create a dataset in bigquery with the name "nlpjob" and a table with the name "sentiment"

* Add the next environment variables:
```export GOOGLE_APPLICATION_CREDENTIALS="KEYPATH"```

* Give permission to the script etl.sh to execute with the next command:
```chmod +x etl.sh```

## How to run the ETL

* When you are ready and your extraction system is working, you can either use cron or watch to execute the script etl.sh every 5 minutes with the next command:
```watch -n 300 ./etl.sh```

* You can change this depending on your needs and requirements, of course modifying the scripts inside the folders




