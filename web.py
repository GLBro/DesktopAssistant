import lxml
import requests
from lxml import html
from PIL import Image


def get_image(search):
    url = "https://www.google.com/search?q="+search+"&udm=2"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    first_image = tree.xpath("//img/@src")
    image = Image.open(requests.get(first_image[1], stream=True).raw)
    return image


