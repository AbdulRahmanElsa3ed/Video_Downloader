import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import filedialog
import pyperclip, threading, yt_dlp, shutil

app = CTk()
app.title("Video Downloader")
app.geometry("806x500")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app.iconbitmap("_images/icon.ico")
app.resizable(False, False)
mode = None
can_download = True

if shutil.which("ffmpeg") is None:
    print("FFmpeg not found! Please download it and put it in the same folder as this script.")
    sys.exit(1)

def app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
path = f"{app_path()}/downloads"

def write_log(message, color):
    textbox.configure(state="normal")
    textbox.insert("end", message, color)
    textbox.see("end")
    textbox.configure(state="disabled")

def paste():
    text = pyperclip.paste()
    url_entry.delete(0, "end")
    url_entry.insert(0, text)

def video():
    global mode
    mode = "Video"
    video_btn.configure(fg_color="#00D100", text_color="#000000", hover_color="#00D100")
    audio_btn.configure(fg_color="#343638", text_color="#FFFFFF", hover_color="#00A300")
    muted_video_btn.configure(fg_color="#343638", text_color="#FFFFFF", hover_color="#00A300")

def audio():
    global mode
    mode = "Audio"
    audio_btn.configure(fg_color="#00D100", text_color="#000000", hover_color="#00D100")
    video_btn.configure(fg_color="#343638", text_color="#FFFFFF", hover_color="#00A300")
    muted_video_btn.configure(fg_color="#343638", text_color="#FFFFFF", hover_color="#00A300")

def muted_video():
    global mode
    mode = "Muted Video"
    muted_video_btn.configure(fg_color="#00D100", text_color="#000000", hover_color="#00D100")
    video_btn.configure(fg_color="#343638", text_color="#FFFFFF", hover_color="#00A300")
    audio_btn.configure(fg_color="#343638", text_color="#FFFFFF", hover_color="#00A300")

def savepath():
    global path
    dir = filedialog.askdirectory(title="Select Save Directory") 
    dir.replace("\\", "/")
    if dir != '':
        path = dir
        write_log(f"SavePath set : {path}\n", 'white')

def quality_colorization(quality):
    if quality == "Low":
        quality_combobox.configure(fg_color="#9C2215", text_color="#000000")
    elif quality == "SD":
        quality_combobox.configure(fg_color="#FF962E", text_color="#000000")
    elif quality == "HD":
        quality_combobox.configure(fg_color="#D2FF2E", text_color="#000000")
    elif quality == "FHD":
        quality_combobox.configure(fg_color="#38FF2E", text_color="#000000")

def write_downloadinfo(mode, url, quality):
    write_log(f"Download a {mode}\n", "white")
    write_log(f"    [URL] {url}\n", "white")
    if mode != "Audio":
        write_log(f"    [Quality] {quality}\n", "white")
    write_log(f"    [SavePath] {path}\n", "white")

def download_video(URL: str = None, Quality: int = 360, SavePath: str = ''):
    if URL == None or URL == "":
        return 
    if Quality == "Low":
        Qualityt = 144
    elif Quality == "SD":
        Qualityt = 360
    elif Quality == "HD":
        Qualityt = 720
    elif Quality == "FHD":
        Qualityt = 1080
    options = {
        "format": f"""bestvideo[height={Qualityt}][ext=mp4]+bestaudio[ext=m4a]/
                      bestvideo[height>{Qualityt}][ext=mp4]+bestaudio[ext=m4a]/
                      bestvideo[height<{Qualityt}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]""",
        "outtmpl": f"{SavePath}/%(title).50sV{Quality}.%(ext)s",
        "ffmpeg_location": "ffmpeg.exe",
        'progress_hooks': [progress_hook]
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(URL)
    except:
        return "Error"


def download_audio(URL: str = None, SavePath: str = ''):
    if URL == None or URL == "":
        return 
    options = {
        "format": f"bestaudio[ext=m4a]",
        "outtmpl": f"{SavePath}/%(title).50sA.%(ext)s",
        "ffmpeg_location": "ffmpeg.exe",
        'progress_hooks': [progress_hook]
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(URL)
    except:
        return "Error"
    
def download_muted_video(URL: str = None, Quality: int = 360, SavePath: str = ''):
    if URL == None or URL == "":
        return 
    if Quality == "Low":
        Qualityt = 144
    elif Quality == "SD":
        Qualityt = 360
    elif Quality == "HD":
        Qualityt = 720
    elif Quality == "FHD":
        Qualityt = 1080
    options = {
        "format": f"""bestvideo[height={Qualityt}][ext=mp4]/
                      bestvideo[height>{Qualityt}][ext=mp4]/
                      bestvideo[height<{Qualityt}][ext=mp4]""",
        "outtmpl": f"{SavePath}/%(title).50sMV{Quality}.%(ext)s",
        "ffmpeg_location": "ffmpeg.exe",
        'progress_hooks': [progress_hook]
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(URL)
    except:
        return "Error"

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total:
            percent = downloaded / total
            progressbar.set(percent)

def download():
    url = url_entry.get()
    quality = quality_combobox.get()
    modet = mode
    global path
    global can_download
    can_download = False
    path = path.replace("\\", "/")
    progressbar.set(0)

    if url == "" or not url.startswith("https://"):
        write_log("Invalid URL.\n", "red")
        can_download = True
        return
    elif modet == None:
        write_log("Download mode not selected.\n", "red")
        can_download = True
        return
    elif quality not in ["Low", "SD", "HD", "FHD"] and modet != "Audio":
        write_log("Quality not selected.\n", "red")
        can_download = True
        return

    write_downloadinfo(modet, url, quality)
    write_log("    Downloading...\n", "white")
    if modet == "Video":
        returned = download_video(url, quality, path)
        if returned == "Error":
            write_log("    An error occurred during download.\n", "red")
        elif progressbar.get() == 0.0:
            write_log(f"    This video has already been downloaded\n", "yellow")
        else:
            write_log(f"    {modet} downloaded Successfuly\n", "green")
    elif modet == "Audio":
        returned = download_audio(url, path)
        if returned == "Error":
            write_log("    An error occurred during download.\n", "red")
        elif progressbar.get() == 0.0:
            write_log(f"    This audio has already been downloaded\n", "yellow")
        else:
            write_log(f"    {modet} downloaded Successfuly\n", "green")
    elif modet == "Muted Video":
        returned = download_muted_video(url, quality, path)
        if returned == "Error":
            write_log("    An error occurred during download.\n", "red")
        elif progressbar.get() == 0.0:
            write_log(f"    This muted video has already been downloaded\n", "yellow")
        else:
            write_log(f"    {modet} downloaded Successfuly\n", "green")
    can_download = True

def download_thread():
    if can_download:
        threading.Thread(target=download, daemon=True).start()


url_entry = ctk.CTkEntry(app, 716, 40, 10, 1, font=("Ariel", 20), placeholder_text="Enter URL")
url_entry.place(x=10, y=10)

paste_btn = CTkButton(app, width=35, height=40, text="Paste", corner_radius=7, font=("Ariel", 20), command=lambda: paste())
paste_btn.place(x=730, y=10)

video_btn = CTkButton(app, 1, 40, 10, 1, font=("Ariel", 20), fg_color="#343638", hover_color="#00A300", text="Video", text_color="#FFFFFF", command=lambda: video())
video_btn.place(x=10, y=60)

audio_btn = CTkButton(app, 1, 40, 10, 1, font=("Ariel", 20), fg_color="#343638", hover_color="#00A300", text="Audio", text_color="#FFFFFF", command=lambda: audio())
audio_btn.place(x=86, y=60)

muted_video_btn = CTkButton(app, 10, 40, 10, 1, font=("Ariel", 20), fg_color="#343638", hover_color="#00A300", text="Muted Video", text_color="#FFFFFF", command=lambda: muted_video())
muted_video_btn.place(x=160, y=60)

quality_combobox = CTkComboBox(app, 150, 40, 10,  1, fg_color="#343638", font=("Ariel", 20), values=["Low", "SD", "HD", "FHD"], dropdown_font=("Ariel", 20), state="readonly" ,command= quality_colorization) 
quality_combobox.place(x=296, y=60)
quality_combobox.set("Quality")

img = CTkImage(Image.open("images/savemark.png"), size=(20,20))
savepath_btn = CTkButton(app, 150, 40, 10, 1, font=("Ariel", 20), fg_color="#343638", hover_color="#494949", text="Save Path", image=img, compound="right", command=lambda: savepath())
savepath_btn.place(x=450, y=60)

progressbar = CTkProgressBar(app, 786, 10, fg_color="#494949", progress_color="#03FF18", corner_radius=17)
progressbar.place(x=10, y=110)
progressbar.set(0)

img = CTkImage(Image.open("images/download.png"), size=(30,30))
download_btn = CTkButton(app, 120, 40, 10, font=("Ariel", 30), text="Download", image=img, fg_color="#000000", text_color="#FFFFFF", hover_color="#1F6AA5", compound="right", command=lambda: download_thread())
download_btn.place(x=604, y=60)

textbox = CTkTextbox(app, 786, 360, 10, 1, font=("Ariel", 20), wrap="none")
textbox.place(x=10, y=130)
textbox.tag_config("white", foreground="white")
textbox.tag_config("orange", foreground="#FF8626")
textbox.tag_config("red", foreground="#DB0000")
textbox.tag_config("green", foreground="#00FF00")
textbox.tag_config("yellow", foreground="#FFD000")
textbox.tag_config("lightYellow", foreground="#EEFF00")
textbox.tag_config("black", foreground="#000000")
textbox.tag_config("blue", foreground="#1a9fff")
textbox.configure(state="disabled")

app.mainloop()