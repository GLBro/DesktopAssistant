import os

import vlc
import pafy
import pytube
from pytubefix import *
from pytube.exceptions import VideoUnavailable
import yt_dlp


def get_video(search):
    try:
        searching = Search(search)
        video = searching.videos[0]
        if video is not None:
            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename='temp.mp4')
            os.startfile("temp.mp4")
            return "playing " + search
    except IndexError and VideoUnavailable:
        return "No videos found"