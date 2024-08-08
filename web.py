import os

import lxml
import requests
from dotenv import load_dotenv
from lxml import html
from PIL import Image
from bs4 import BeautifulSoup



def get_image(search):
    url = "https://www.google.com/search?q="+search+"&udm=2"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    first_image = tree.xpath("//img/@src")
    image = Image.open(requests.get(first_image[1], stream=True).raw)
    return image

def get_description(search):
    AGENT = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }
    url = "https://www.google.com/search?q="+search
    response = requests.get(url, headers=AGENT)
    tree = html.fromstring(response.content)
    try:
        desc = tree.xpath("//block-component//text()")
        if desc == []:
            print("backup")
            desc = tree.xpath("//div[@data-sncf=\"1\"][1]/div[@style=\"-webkit-line-clamp:2\"]//text()")
        else:
            desc[0] = ""
            print("success")
    except:
        desc = tree.xpath("//div[@data-sncf=\"1\"][1]/div[@style=\"-webkit-line-clamp:2\"]//text()")
    first = ""
    print(desc)
    for i in range(len(desc)):
        if "..." not in desc[i] or first == "":
            first += desc[i]
        else:
            temp = desc[i].split("\\")
            first += temp[0]
            break
    print(first)
    if len(first) >= 150:
        pos = 0
        for i in range(148):
            if (first[i] == "." or first[i] == ",") and first[i + 1] == " " and 65 <= ord(first[i + 2]) <= 90:
                pos = i
        if pos == 0:
            first = first.split(".")[0]
        else:
            first = first[0:pos]
    print(first)
    return first


