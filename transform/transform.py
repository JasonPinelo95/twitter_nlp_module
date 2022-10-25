#!/home/mejareduardo/.pyenv/versions/transform/bin/python
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import re,os
import os.path
import json
import nltk
from nltk.corpus import stopwords
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

# ----------------------------- Methods ------------------------------------

# Helpler method to remove emojis from comments 
def remove_emojis(string):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', string)

# Main Method to clean a comment 
def cleanString(string):
    
    clean_string = string.lower()                                         # string to lower case
    clean_string = remove_emojis(clean_string)                            # remove emojis 
    clean_string = re.sub(r'http\S+', '', clean_string)                   # remove links
    clean_string = re.sub(r'[0-9]+', '', clean_string)                    # remove digits
    clean_string = re.sub(r"\b's\b", '', clean_string)                    # remove 's
    clean_string = clean_string.encode('ascii', errors='ignore').decode() # remove nonASCII chars
    
    # remove special chars
    cleaned_words = []
    special_chars = ",.?!¬-—\''=+*/()[]{}``&:;™_<>^%|~"+'"'            # define spacial chars
    for char in special_chars:
        clean_string = clean_string.replace(char, '')
    clean_string = clean_string.split(" ")
    
    # remove extra white-spaces
    for word in clean_string:
        if len(word.replace(" ", "")) > 0:
            cleaned_words.append(word.replace(" ", ""))
            
    # return cleaned comment
    return " ".join(cleaned_words)   


# Method to get polarity
def polarity(model,text):
    doc = model(text)
    return doc._.blob.polarity

# Method to clasify polarity
def classify_polarity(num):
    if num >= (0.0):
        return 'Positive'
    else:
        return 'Negative'

# Method to get subjectivity
def subjectivity(model,text):
    doc = model(text)
    return doc._.blob.subjectivity

# Method to clasify subjectivity
def classify_subjectivity(num):
    if num >= (0.5):
        return 'Subjective'
    else:
        return 'Objective'

# Method to build lexicon
def update_lexicon(df, sw):
    
    # Create folder lexicon if not exist
    if not os.path.exists("/home/mejareduardo/twitter_project/transform/lexicon"):
        os.mkdir("/home/mejareduardo/twitter_project/transform/lexicon")
    
    # File path 
    file_exists = os.path.exists('/home/mejareduardo/twitter_project/transform/lexicon/lexicon.json')
    
    # JSON file
    if file_exists == True:
        f = open ('/home/mejareduardo/twitter_project/transform/lexicon/lexicon.json', "r")
        tweet_lexicon = json.loads(f.read()) # Reading from file
        f.close() # Closing file
    else:
        tweet_lexicon = {}

    # Make comments lexicon
    for t in df["clean_text"]: 
        tokens = tokenizer.tokenize(t)
        for token in tokens:
            if not token in tweet_lexicon:
                tweet_lexicon[token] = 1
            else:
                tweet_lexicon[token] += 1
                    
    # Remove stop words
    for key in sw:
        if key in list(tweet_lexicon.keys()):
            tweet_lexicon.pop(key)            

    return tweet_lexicon #137 tokens


# Method to get top n rank of words
def get_n_rank(tweet_lexicon, n):

    Dict = tweet_lexicon.copy()
    List = []

    for i in range(0,n):
        max_key = max(Dict, key=Dict.get)
        List.append(max_key.capitalize())
        Dict.pop(max_key)
    
    return List


# --------------------------------------- Drive code -------------------------------------

hashtag = "#HouseOfTheDragon"
list_tweets = ["Fire reigns. #HouseOfTheDragon, the @HBO original series and prequel to @GameofThrones, is now streaming on @HBOMax.",
               "Game of Thrones facts & news — created by @mytweetsmid | #HouseOfTheDragon | Thrones pod @culturecravepod | GoT memes @freefolkmemes|",
               "#HouseOfTheDragon Episode 8 will be the longest episode of the season, and many critics are saying it’s one of the best & most emotional episodes of television ever.",
               "Happy #HouseOfTheDragon Sunday!!",
               "Rhaenyra Targaryen's dress, the Black Queen, is impressive. #HouseOfTheDragon",
               "Oh my gosh EP 8 of #HouseOfTheDragon has a 10/10 score.",
               "When Daemon puts on a hood, we all know something is going to happen... #HouseOfTheDragon",
               "Aemond riding Vhagar for the first time #HouseOfTheDragon",
               "Congratulations to Daemon and Rhaenyra Targaryen, for celebrating the only wedding in Westeros, in which no one is dead. Long live the bride and groom. #HouseOfTheDragon",
               "I would have liked to see, before another time jump, Viserys's face when he found out that Daemon in the end did what came out of the papo and married Rhaenyra. #HouseOfTheDragon",
               "Me seeing how Viserys on top of naming Aemond in honor of his late wife also confuses Alicent with Aemma #HouseOfTheDragon",
               "The change of the Targaryen and Velaryon children in today's episode of #HouseOfTheDragon 😏",
               "Stay with someone who looks at you and supports you like Daemon to Rhaenyra, and also has your same level of perversion. #HouseOfTheDragon",
               "Luck or curse? The important thing is to be together until the end. 🔥 #HouseOfTheDragon",
               "Share this lucky Laenor Velaryon so you can live your life and your sexuality freely. #HouseOfTheDragon",
               "And here (stands up), ladies and gentlemen, why Daemon Targaryen is the best character in the world of characters. #HouseOfTheDragon",
               "Alicent and her children when Viserys asked who was spreading the rumors of Rhaenyra's children 😂😂😂 #HouseOfTheDragon",
               "Aemond took the chapter. Claiming an ancient dragon and succeeding at it, he is the only one of Alicent's children who knows where he stands. #HouseOfTheDragon #AemondTargaryen #Vhagar",
               'Our destiny was always to burn together. #HouseOfTheDragon',
               "And that was how Don Omar left Westeros. #HouseOfTheDragon | https://twitter.com/hashtag/houseofthedragon"]


# DataFrame (request de Big Query)
df = pd.read_csv("/home/mejareduardo/twitter_project/transform/text.csv", names = ['text'], header = None)

# Update Dataframe (clean text)
df['clean_text'] = df['text'].apply(lambda x: cleanString(x))

# Update Dataframe (sentimient analisys -> polarity score)
df['polarity_score'] = df['text'].apply(lambda x: polarity(nlp,x))

# Update Dataframe (classify polarity)
df['polarity_class'] = df["polarity_score"].apply(lambda x: classify_polarity(x))

# Update Dataframe (sentimient analisys -> subjectivity score)
df['subjectivity_score'] = df['text'].apply(lambda x: subjectivity(nlp,x))

# Update Dataframe (classify subjectivity)
df['subjectivity_class'] = df["subjectivity_score"].apply(lambda x: classify_subjectivity(x))


# Tweet Tokenizer
tokenizer = nltk.tokenize.TweetTokenizer()

# English stop words
sw = set(stopwords.words('english'))

# Update tweet lexicon
tweet_lexicon = update_lexicon(df, sw)

# Remove some useless tokens
No_relevant_tokens = [hashtag.lower(),'episode','episodes']
for i in No_relevant_tokens:    
    try:
        tweet_lexicon.pop(i)
    except:
        pass   
# print(len(tweet_lexicon)) # 133 -2

#Delete old lexicon.json
try:
    os.remove("/home/mejareduardo/twitter_project/transform/lexicon/lexicon.json") 
except:
    pass

#Save new lexicon.json
json_object = json.dumps(tweet_lexicon) 
with open('/home/mejareduardo/twitter_project/transform/lexicon/lexicon.json','w') as f:
    f.write(json_object)
    f.close()
     
# Get rank of words
rank = get_n_rank(tweet_lexicon,10)


# --------------------------------- Data to insert in Big Query ---------------------------------

# Data to insert in Big Query
new_row = {"Tweet_num":len(df),
           "Positives": df['polarity_class'].value_counts().Positive,
           "Negatives": df['polarity_class'].value_counts().Negative,
           "Subjectives": df['subjectivity_class'].value_counts().Subjective,
           "Objectrives": df['subjectivity_class'].value_counts().Objective,
           'rank_1': rank[0],
           'rank_2': rank[1],
           'rank_3': rank[2],
           'rank_4': rank[3],
           'rank_5': rank[4],
           'rank_6': rank[5],
           'rank_7': rank[6],
           'rank_8': rank[7],
           'rank_9': rank[8],
           'rank_10': rank[9]}

# Table in Big Query
BQ_df = pd.DataFrame(columns=["Tweet_num","Positives","Negatives","Subjectives","Objectrives",
                             'rank_1','rank_2','rank_3','rank_4','rank_5','rank_6','rank_7','rank_8','rank_9','rank_10'])
BQ_df = BQ_df.append(new_row,ignore_index=True)
BQ_df.to_csv("/home/mejareduardo/twitter_project/load/sentiment.csv", header = False)
print("Done")
