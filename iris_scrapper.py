import time
import random
import json
import string
import pandas as pd
import yt_dlp as youtube_dl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

# Function to generate random string
def get_long_word(subtitles):
    words = subtitles.split(" ")
    longest_word = max(words, key=len)
    return longest_word

def get_description_from_google(driver, query):
    driver.get(f"https://www.google.com/search?q={query}")
    time.sleep(3)
    search_results = driver.find_elements_by_css_selector("div.g")
    if search_results:
        description = search_results[0].text
        return description
    else:
        return None
    
# Initialize Chrome webdriver
driver = webdriver.Chrome()

class VideoMetadata:
    def __init__(self, video_link):
        self.video_link = video_link
        self.video_id = self.extract_video_id()

        self.ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True
        }

    def extract_video_id(self):
        parsed_url = urlparse(self.video_link)
        query_params = parse_qs(parsed_url.query)
        print(query_params.get('v', [''])[0])
        return query_params.get('v', [''])[0]

    def get_video_length(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            dict_meta = ydl.extract_info(self.video_link, download=False)
        return dict_meta.get('duration', 0)
    
    def get_video_title(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            dict_meta = ydl.extract_info(self.video_link, download=False)
        return dict_meta.get('title', '')

    def get_caption(self):

        # extractor for TEXT_AND_TIME 
        timed_transcript = YouTubeTranscriptApi.list_transcripts(self.video_id)
        timed_data = []

        # iterate over all available transcripts
        for transcript in timed_transcript:
            segments = transcript.fetch()

            # extract text and start fields and add to timed_data
            for segment in segments:
                timed_data.append({"text": segment['text'], "start":segment["start"]})
        
        with open("timed_text.json", "w") as file:
            json.dump(timed_data, file, indent=3)
        #------END of TEXT_AND_TIME-------------------
            
        # extractor for TEXT_ONLY caption
        full_transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
        # write whole video transcript to subtitle.txt
        with open("subtitles.txt", "w") as file:
            for i in full_transcript:
                file.write(i['text'])
        #------END of TEXT_ONLY-----------------------
    
# Input video link
video_link = input("Enter the YouTube video link: ")

# Create an instance of VideoMetadata and get the video length
video = VideoMetadata(video_link)
length = video.get_video_length()
title = video.get_video_title()
vid_id = video.extract_video_id()
caption = video.get_caption()
random_timing = random.randint(0, length)
driver.execute_script(f"window.open('{video_link}');")
print("Title of the video:", title)