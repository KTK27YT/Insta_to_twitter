## This code was heavily based off of https://github.com/xacnio/tweetcapture/blob/main/tweetcapture/examples/tweet_screenshot_to_instagram.py
## All rights goes to him/her/them for the code. I just modified it to work with my needs. 
from instagrapi import Client
from instagrapi.types import StoryMedia, StoryMention, StoryLink, StoryHashtag, StoryLocation
from tweetcapture import TweetCapture
import os
import asyncio
import time
from PIL import Image


print("What's your Instagram username? \n")
username = input()
print("What's your Instagram password? \n")
password = input()

cl = None

print("What's the url of your tweet you want to publish? \n")
url = input()


def upload_post(filename, caption=""):
    global cl
    if cl is None:
        cl = Client()
        cl.login(username, password)
    post = cl.photo_upload(filename, caption=caption)
    return post

async def fetch_tweet(url):
    tweet = TweetCapture()
    try:
        path = await tweet.screenshot(url, "tweet.png", mode=3, night_mode=2)
    except Exception as e:
        print(e)
        return None

    img = Image.open(path)
    filename = path + ".jpg"
    rgb_img = img.convert('RGB')

    width,height = img.size
    rs = max(width,height)
    size = rs, rs
    background_color = (0,0,0)
    fit_image = Image.new('RGB', size, background_color)
    bg_w, bg_h = fit_image.size
    offset = ((bg_w - width) // 2, (bg_h - height) // 2)
    fit_image.paste(rgb_img, offset)
    fit_image.save(filename)
    os.remove(path)

    if os.path.exists(filename):
        print("What Caption do you want? (Leave blank for none)")
        caption = input()
        upload_post(filename, caption=caption)
        os.remove(filename)
    else:
        print("convert error")


asyncio.run(fetch_tweet(url))