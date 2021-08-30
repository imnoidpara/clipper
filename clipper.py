import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askyesno

import sys
import subprocess
import csv

version = "0.1"
mPath = r''
vPath = r''
oPath = r''


# GUI
mainWindow = tk.Tk()


# Clipping

def clip():
    # parse the timestamps
    print(mPath)
    timestamps = []
    with open(mPath, 'r', encoding='utf-16') as csvFile:
        csv_reader = csv.reader(csvFile, delimiter='\t')

        for row in csv_reader:
            timestamps.append(row[1:4])

        timestamps = timestamps[1:]

        print(f"Total {len(timestamps) :d} no of clips will be created")

        for row in timestamps:
            row[1] = row[1][:8] + '.' + row[1][9:]
            row[2] = row[2][:8] + '.' + row[2][9:]

    # final format
    # 0 = name 1 = start 2 = end
    # video vPath output oPath

    for row in timestamps:
        subprocess.run(f"ffmpeg.exe -ss {row[1]} -to {row[2]} -i \"{vPath}\" -c copy \"{oPath+'/'+row[0]}.mp4\"")

    tk.messagebox.showinfo(title='Clipping Result', message='Clipping finished!')


# Window Title
mainWindow.title("Clipper V" + version)

window_width = 300
window_height = 200

# get the screen dimension
screen_width = mainWindow.winfo_screenwidth()
screen_height = mainWindow.winfo_screenheight()

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# set the position of the window to the center of the screen
mainWindow.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
# Resizable
# mainWindow.resizable(False, False)

# Transparency
# mainWindow.attributes('-alpha', 0.5)

# icons
mainWindow.iconbitmap('./assets/icon.ico')
#clipit_icon = tk.PhotoImage(file='/assets/clipit.png')

# Label
ttk.Label(mainWindow, text="Welcome to Clipper! Version no: " + version).pack()


# File selection

def select_vod():
    filetypes = (
        ('Media files', '*.mp4'),
        ('All files', '*.*')
    )

    global vPath
    vPath = fd.askopenfilename(
        title='select the VOD',
        filetypes=filetypes)

    # showinfo(
    #     title='Selected VOD',
    #     message=vod_path
    # )


# open button
select_VOD_button = ttk.Button(
    mainWindow,
    text='select a VOD',
    command=select_vod
)


def select_markers():
    filetypes = (
        ('Marker file', '*.csv'),
        ('All files', '*.*')
    )
    global mPath
    mPath = fd.askopenfilename(
        title='select the Marker File',
        filetypes=filetypes)


# open button
select_MARKERS_button = ttk.Button(
    mainWindow,
    text='select the markers file',
    command=select_markers
)

select_VOD_button.pack(expand=True)
select_MARKERS_button.pack(expand=True)


# Output directory
def select_output():
    global oPath
    oPath = fd.askdirectory(
        title='select output directory')


# open button
select_OUTPUT_button = ttk.Button(
    mainWindow,
    text='select output directory',
    command=select_output
)

select_OUTPUT_button.pack(expand=True)

# Button
ttk.Button(
    mainWindow,
    text='Start Clipping',
    command=clip,
    #image=clipit_icon,
    compound=tk.LEFT
).pack(
    ipadx=5,
    ipady=5,
    expand=True
)


# Event binding
# btn = ttk.Button(mainWindow, text='Save')
# btn.bind('<Return>', clip)
#
# btn.focus()
# btn.pack(expand=True)

# agreement = tk.StringVar()

# def agreement_changed():
#     tk.messagebox.showinfo(title='Result',
#                            message=agreement.get())
#
#
# ttk.Checkbutton(mainWindow,
#                 text='I agree',
#                 command=agreement_changed,
#                 variable=agreement,
#                 onvalue='agree',
#                 offvalue='disagree').pack()

# exit button
def confirm():
    answer = askyesno(title='confirmation',
                      message='Are you sure that you want to quit?')
    if answer:
        mainWindow.destroy()


ttk.Button(
    mainWindow,
    text='Exit',
    command=confirm).pack(expand=True)

mainWindow.mainloop()
