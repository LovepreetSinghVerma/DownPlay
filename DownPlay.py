import os.path
import tkinter as tk
from tkinter import filedialog
from pytube import Playlist
from pytube import YouTube


root = tk.Tk()
root.title("YouTube Playlist Downloader")

#func to select path to download the file/files
def select_folder():
    download_folder = filedialog.askdirectory()
    if download_folder:
        download_btn["state"] = "normal"
        folder_path.set(download_folder)

#func to check if URL is of playlist or a yt video
def checkurl():
    tocheck=url_entry.get()

    if 'playlist' in tocheck:
        download_playlist()
    else:
        download_video()

#func to download video
def download_video():
    video_url=url_entry.get()
    videofetch = YouTube(video_url)
    video_stream = videofetch.streams.get_highest_resolution()
    if mp3_var.get():
        #boolvariable for mp3 (audio)
        outfile=videofetch.streams.filter(only_audio=True).first().download(output_path=folder_path.get())
        base, ext=os.path.splitext(outfile)
        newfile=base + '.mp3'
        os.rename(outfile,newfile)
        tk.messagebox.showinfo("Download Complete", "Audio downloaded successfully!")
    else:
        video_stream.download(output_path=folder_path.get())
        tk.messagebox.showinfo("Download Complete", "Video downloaded successfully!")

#func to download playlist
def download_playlist():
    playlist_url = url_entry.get()
    playlist = Playlist(playlist_url)

    for video in playlist.videos:
        video_stream = video.streams.get_highest_resolution()
        if mp3_var.get():
            outfile=video.streams.filter(only_audio=True).first().download(output_path=folder_path.get())
            base, ext = os.path.splitext(outfile)
            newfile = base + '.mp3'
            os.rename(outfile, newfile)

        else:
            video_stream.download(output_path=folder_path.get())

    tk.messagebox.showinfo("Download Complete", "Playlist downloaded successfully!")

#main tkinter (buttons and labels)
folder_path = tk.StringVar()
tk.Label(root, text="Save folder:").grid(row=0, column=0)
folder_entry = tk.Entry(root, textvariable=folder_path, state="readonly")
folder_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_folder).grid(row=0, column=2)

tk.Label(root, text="Enter URL:").grid(row=1)
url_entry = tk.Entry(root)
url_entry.grid(row=1, column=1)

mp3_var = tk.BooleanVar()
mp3_checkbox = tk.Checkbutton(root, text="MP3", variable=mp3_var)
mp3_checkbox.grid(row=2, column=0, sticky='w')

download_btn = tk.Button(root, text="Download", state="disabled", command=checkurl)
download_btn.grid(row=2, column=1)

root.mainloop()