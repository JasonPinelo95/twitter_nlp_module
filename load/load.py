#!/home/mejareduardo/.pyenv/versions/load/bin/python
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()
table_id = "places-api-364005.nlpjob.sentiment"


df =  pd.read_csv("/home/mejareduardo/twitter_project/load/sentiment.csv",
        names=[
            "tweet_quantity",
            "positives",
            "negatives",
            "subjectives",
            "objectives",
            "rank_1",
            "rank_2",
            "rank_3",
            "rank_4",
            "rank_5",
            "rank_6",
            "rank_7",
            "rank_8",
            "rank_9",
            "rank_10"], header=None)


#job_config = bigquery.LoadJobConfig()

job = client.load_table_from_dataframe(df, table_id)
job.result()
print("Done")
