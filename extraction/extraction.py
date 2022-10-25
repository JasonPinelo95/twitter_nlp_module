#!/home/mejareduardo/.pyenv/versions/extraction/bin/python
from google.cloud import bigquery
def extraction():
    # [START bigquery_simple_app_client]
    client = bigquery.Client()
    # [END bigquery_simple_app_client]
    # [START bigquery_simple_app_query]
    query_job = client.query(
        """
        SELECT
          text
        FROM `places-api-364005.fs_trends.tweets`
        """
    )

    results = query_job.result()  # Waits for job to complete.
    # [END bigquery_simple_app_query]

    df = results.to_dataframe()
    
    df.to_csv("/home/mejareduardo/twitter_project/transform/text.csv",header=False)

if __name__ == "__main__":
    extraction()
    print("Done")
