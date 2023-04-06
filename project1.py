import pandas as pd
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
import json
import streamlit as st
import datetime

#function_block

@st.cache_data # IMPORTANT: Cache the conversion to prevent computation on every rerun
def twitter_scrape(search_word, tweet_count=10, until=datetime.date.today(), since=(datetime.date.today() - datetime.timedelta(days=10))):
    scrape_data = []

    search_query = f"{search_word} until:{until} since:{since}"

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        if i >= int(tweet_count):
            break
        tweet_data = {
            "Scrape_word":search_word,
            "id": tweet.id,
            "url": tweet.url,
            "content": tweet.content,
            "user": tweet.user.username,
            "reply_count": tweet.replyCount,
            "retweet_count": tweet.retweetCount,
            "language": tweet.lang,
            "source": tweet.sourceLabel,
            "like_count": tweet.likeCount
        }

        scrape_data.append(tweet_data)

    return scrape_data

@st.cache_data # IMPORTANT: Cache the conversion to prevent computation on every rerun
def data_frame(scrape_data):
    tweet_data=pd.DataFrame(scraped_data,columns=["date","id","url","content","user","reply_count","retweet_count","Language","source","like_count"])        
    return tweet_data
    
#Main_block

search_word = st.text_input("Enter the word to search", key="word1")

# Default scrape block
st.checkbox("""CLICK FOR DEFAULT SCRAPE""", key="Default")

st.write(":red[**** Default 1000  Scraped data from past 100 days ****]")

if st.session_state.Default == True:
    if st.button("Scrape Tweets"):
        scraped_data = twitter_scrape(search_word)
        tweet_data = data_frame(scraped_data)
        st.dataframe(tweet_data)
        
        # To download the scraped data as csv
        csv= tweet_data.to_csv()
        c = st.download_button("Download as CSV",data=csv, file_name='Twitter_data.csv',key="csv1")
        if st.session_state.csv1 == True:
            st.success("The Scraped Data is Downloaded as .CSV file:",icon="✅")
            
        # To download the scraped data as json    
        j_son= tweet_data.to_json()
        j = st.download_button("Download as json",data=j_son, file_name='Json_data.json',key="json1")
        if st.session_state.json1 == True:
            st.success("The Scraped Data is Downloaded as .json file:",icon="✅")
    #Upload scraped data to MongoDB database
    if st.button("Upload to MongoDB"):
        scraped_data = twitter_scrape(search_word)
        tweet_data = data_frame(scraped_data)

        client = MongoClient('localhost', 27017)
        db = client["twitter_db_streamlit"]
        collection = db['tweet']
        tweet_data_json = json.loads(tweet_data.to_json(orient='records'))
        collection.insert_many(tweet_data_json)
        st.success('Uploaded to MongoDB')  

# Custome scrape block
st.checkbox("""CLICK FOR CUSTOME SCRAPE""", key="Custome")

st.write(":red[**** For custome No of tweets, starting date and end date ****]")

if st.session_state.Custome == True:
    no_tweets= st.text_input("Please enter the number of tweets to scrape", key="no_of_tweets")
    since =st.date_input("Enter the start date:", key="start")
    until =st.date_input("Enter the end date:", key="end")
   
    if st.button("Custome Tweets"):
        scraped_data = twitter_scrape(search_word, no_tweets, until, since)
        tweet_data = data_frame(scraped_data)
        st.dataframe(tweet_data)
        st.write("iam i in")
        
        # To download the scraped data as csv
        csv= tweet_data.to_csv()
        c = st.download_button("Download as CSV",data=csv, file_name='Twitter_data.csv', key="cc")
        if st.session_state.cc == True:
            st.success("The Scraped Data is Downloaded as .CSV file:",icon="✅")
            
        # To download the scraped data as json   
        j_son= tweet_data.to_json()
        j = st.download_button("Download as json",data=j_son, file_name='Json_data.csv', key="jj")
        if st.session_state.jj == True:
            st.success("The Scraped Data is Downloaded as .json file:",icon="✅")
            
    #Upload scraped data to MongoDB database
    if st.button("Upload to MongoDB "):
        scraped_data = twitter_scrape(search_word, no_tweets, until, since)
        tweet_data = data_frame(scraped_data)

        client = MongoClient('localhost', 27017)
        db = client["twitter_db_streamlit"]
        collection = db['tweet']
        tweet_data_json = json.loads(tweet_data.to_json(orient='records'))
        collection.insert_many(tweet_data_json)
        st.success('Uploaded to MongoDB')





            
    
    
