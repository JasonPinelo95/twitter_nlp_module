#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS="/home/mejareduardo/twitter_project/cred.json"
chmod +x ./extraction/extraction.py
chmod +x ./transform/transform.py
chmod +x ./load/load.py

echo "Extraction..."
./extraction/extraction.py
echo "Transform..."
./transform/transform.py
echo "Load..."
./load/load.py

rm ./transform/text.csv
rm ./load/sentiment.csv

