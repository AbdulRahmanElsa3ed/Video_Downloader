# Video Downloader App

## Features

- Download videos in different qualities (Low, SD, HD, FHD).  
- Supports downloading:  
  - Full video  
  - Audio only  
  - Muted video  
- Ability to choose the save location on your device.  
- Uses [yt_dlp](https://github.com/yt-dlp/yt-dlp), which allows downloading from multiple platforms and websites.  
- Built with a user-friendly interface using **CustomTkinter**.

## FFmpeg Requirement

This program relies on `ffmpeg.exe` to handle video and audio processing.  

**Important:**  
- Make sure that `ffmpeg.exe` is located in the **same folder as `main.py`**.  
- The latest release already includes `ffmpeg.exe`, so you **don't need to download it separately**.

**How to download FFmpeg.exe:**  
1. Go to the official [FFmpeg builds](https://github.com/BtbN/FFmpeg-Builds/releases).
2. Download the latest version of **ffmpeg-master-latest-win64-gpl.zip**.  
3. Get `ffmpeg.exe` from "ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe" and place it in the same folder as `main.py`.  

## Instructions

1) Enter Video URL.
2) Select Download Mode.
3) Select Quality.
4) Enter Save Path.
5) Press Download.

![image1](README_Docs/image.png)

## Requirements

- Python 3.8 or higher  
- Libraries:
```bash
pip install customtkinter pillow pyperclip yt-dlp
```

























