import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os
import subprocess  # For opening file explorer

# Create or ensure yt-downloader directory exists on the desktop
def create_directory():
    try:
        # Get the desktop path dynamically using the correct environment variable
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Get desktop path (Windows)
        download_folder = os.path.join(desktop, "yt-downloader")

        # Check if the folder exists, if not create it
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)  # Create the directory if it doesn't exist
        
        return download_folder
    except Exception as e:
        print(f"Failed to create or access folder: {e}")
        messagebox.showerror("Error", f"Failed to create or access folder on the desktop. Error: {e}")
        return None

# Video or audio download function
def download_youtube_video():
    url = url_entry.get()  # Get URL from text box
    download_type = var.get()  # Getting the type of download (video or audio)

    if not url:
        update_status_message("Error: Enter video URL.", "error")
        return

    download_folder = create_directory()  # Ensure folder exists on desktop

    if download_folder is None:
        return  # Exit if folder creation failed

    ydl_opts = {}

    # Settings for audio or video
    if download_type == "audio":
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save in yt-downloader folder on desktop
            'noplaylist': True,
        }
    elif download_type == "video":
        ydl_opts = {
            'format': 'best',  # Downloads video with audio
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save in yt-downloader folder on desktop
            'noplaylist': True,
        }

    # Display the title of the video in the text box
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown title')
            filename = ydl.prepare_filename(info)  # Get the file name after formatting
            
            # Show that it is downloading
            status_text.insert(tk.END, f"Download: {title}\n", "info")
            status_text.see(tk.END)
            
            # Video Download
            ydl.download([url])

            # Add file path to history
            history_listbox.insert(tk.END, filename)  # Add the full path to the listbox

        status_text.insert(tk.END, f"Downloaded: {title}\n", "success")
        status_text.see(tk.END)
        update_status_message(f"Downloaded: {title}", "success")
    except Exception as e:
        status_text.insert(tk.END, f"Download failed: {e}\n", "error")
        status_text.see(tk.END)
        update_status_message(f"Error: {e}", "error")

# Status update function in the bug and success window
def update_status_message(message, tag):
    status_message.config(state=tk.NORMAL)  # Enable widget text editing
    status_message.delete(1.0, tk.END)  # Clear old message
    status_message.insert(tk.END, message, tag)  # Insert new message
    status_message.tag_configure("success", foreground="#4caf50", font=("Helvetica", 12, "bold"))
    status_message.tag_configure("error", foreground="#ff6347", font=("Helvetica", 12, "bold"))
    status_message.config(state=tk.DISABLED)  # Disable editing again

# Function to open the folder or file when clicking on the history entry
def open_file(event):
    selected = history_listbox.curselection()  # Get the index of the selected item
    if selected:
        file_path = history_listbox.get(selected[0])  # Get the file path from the listbox
        if os.path.exists(file_path):
            subprocess.Popen(f'explorer /select,"{file_path}"')  # Open the file in the explorer
        else:
            messagebox.showerror("Error", "File path not found.")

# Functions for creating a gradient
def draw_gradient(canvas, width, height, color1, color2):
    steps = 100  # Number of steps in gradient
    for i in range(steps):
        r = int(color1[0] + (color2[0] - color1[0]) * i / steps)
        g = int(color1[1] + (color2[1] - color1[1]) * i / steps)
        b = int(color1[2] + (color2[2] - color1[2]) * i / steps)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_rectangle(0, i * height / steps, width, (i + 1) * height / steps, outline="", fill=color)

# Create the main application window
root = tk.Tk()
root.title("Youtube Downloader - Iniify")
root.geometry("1920x1080")

# Canvas for gradient backgrounds
canvas = tk.Canvas(root, height=650, width=700)
canvas.pack(fill="both", expand=True)

# Gradient colors (blue to black)
blue = (33, 150, 243)
black = (33, 33, 33)

draw_gradient(canvas, 700, 650, blue, black)

# Create a frame for widgets to be above the gradient
frame = tk.Frame(root, bg="#212121")
frame.place(relwidth=1, relheight=1)

# Description
title_label = tk.Label(frame, text="Enter the URL of the YouTube video", bg="#212121", fg="#ffffff", font=("Helvetica", 14, "bold"))
title_label.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

# Text field for entering URL
url_entry = tk.Entry(frame, width=50, bg="#424242", fg="#ffffff", font=("Helvetica", 12), borderwidth=2, relief="groove")
url_entry.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

# Choosing between audio and video
var = tk.StringVar(value="video")

video_radiobutton = tk.Radiobutton(frame, text="Download Video", variable=var, value="video", bg="#212121", fg="#ffffff", selectcolor="#1c1c1c", font=("Helvetica", 10))
video_radiobutton.place(relx=0.4, rely=0.2, anchor=tk.CENTER)

audio_radiobutton = tk.Radiobutton(frame, text="Download Audio", variable=var, value="audio", bg="#212121", fg="#ffffff", selectcolor="#1c1c1c", font=("Helvetica", 10))
audio_radiobutton.place(relx=0.6, rely=0.2, anchor=tk.CENTER)

# Function for button when hover
def on_enter(e):
    download_button.config(bg="#ff9800")

def on_leave(e):
    download_button.config(bg="#f57c00")

# Button to start downloading
download_button = tk.Button(frame, text="Download", command=download_youtube_video, bg="#f57c00", fg="#ffffff", font=("Helvetica", 12), relief="flat", padx=10, pady=5)
download_button.place(relx=0.5, rely=0.28, anchor=tk.CENTER)
download_button.bind("<Enter>", on_enter)
download_button.bind("<Leave>", on_leave)

# Text field to display the current download status
status_text = tk.Text(frame, height=10, width=50, bg="#1c1c1c", fg="#ffffff", font=("Helvetica", 10), relief="flat", padx=10, pady=5)
status_text.tag_configure("info", foreground="#00bfff", font=("Helvetica", 10, "bold"))
status_text.tag_configure("success", foreground="#4caf50", font=("Helvetica", 10, "bold"))
status_text.tag_configure("error", foreground="#ff6347", font=("Helvetica", 10, "bold"))
status_text.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# List for download history
history_label = tk.Label(frame, text="Download history:", bg="#212121", fg="#ffffff", font=("Helvetica", 12))
history_label.place(relx=0.5, rely=0.58, anchor=tk.CENTER)

history_listbox = tk.Listbox(frame, height=5, width=50, bg="#424242", fg="#ffffff", font=("Helvetica", 10), relief="flat", selectbackground="#757575")
history_listbox.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
history_listbox.bind('<Double-1>', open_file)  # Bind double-click to open file location

# A window to display errors and successes (in the form of a Text widget, but only for display)
status_label = tk.Label(frame, text="Status:", bg="#212121", fg="#ffffff", font=("Helvetica", 12))
status_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

status_message = tk.Text(frame, height=3, width=50, bg="#1c1c1c", fg="#ffffff", font=("Helvetica", 10), relief="flat", padx=10, pady=5)
status_message.place(relx=0.5, rely=0.83, anchor=tk.CENTER)
status_message.config(state=tk.DISABLED)

# Running the main loop of the application
root.mainloop()
