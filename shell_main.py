import tkinter as tk
from tkinter import font as tkfont
import sys , os , getpass , socket , subprocess
from datetime import datetime
from pathlib import Path
import ctypes

def check_elevate():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return "Administrator: "
    else:
        return ""

root = tk.Tk()

def cd(dir = None):
    global CURR_DIR
    if dir == None:
        text.insert(tk.END , f"\n{CURR_DIR}\n")
        return
    start_dir = CURR_DIR
    with os.scandir(f"C:/{CURR_DIR}") as d:
        for i in d:
            if i.is_dir():
                if str(dir.upper()) == str(i.name.upper()):
                    CURR_DIR = f"{CURR_DIR}/{i.name}"
    end_dir = CURR_DIR
    if start_dir == end_dir:
        text.insert(tk.END , f"\nThe input '{dir}' is not a valid subdirectory\n")
    return
def exit(catch = None):
    if catch:
        inspos = text.index(tk.INSERT)
        row = inspos[:inspos.find(".")]
        cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
        return
    global EXISTS
    EXISTS = False
    root.destroy()
    sys.exit()
def cls(catch = None):
    if catch:
        inspos = text.index(tk.INSERT)
        row = inspos[:inspos.find(".")]
        cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
        return
    text.delete(0.0 , tk.END)
def needcmd(catch = None):
    if catch:
        inspos = text.index(tk.INSERT)
        row = inspos[:inspos.find(".")]
        cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
        return
    os.startfile("cmd.exe")
    exit()
def help(catch = None):
    if catch:
        inspos = text.index(tk.INSERT)
        row = inspos[:inspos.find(".")]
        cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
        return
    help = dict(zip(strcmds , explanations))
    text.insert(tk.END , "\n\n")
    for cmd , ex in sorted(help.items()):
        text.insert(tk.END , f"{cmd.upper()}\t\t{ex.upper()}\n")
def dir(catch = None):
    if catch:
        inspos = text.index(tk.INSERT)
        row = inspos[:inspos.find(".")]
        cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
        return
    text.insert(tk.END , f"\n\n   Directory of {CURR_DIR}\n\n")
    names = []
    modes = []
    times = []
    size = 0
    dir_count = 0
    file_count = 0
    with os.scandir(f"C:/{CURR_DIR}") as d:
        for i in d:
            names.append(i.name)
            if i.is_dir():
                modes.append("<DIR>")
                dir_count += 1
            elif i.is_file():
                modes.append(i.stat().st_size)
                size += i.stat().st_size
                file_count += 1
            else:
                modes.append("<MAGIC>")
            times.append(datetime.fromtimestamp(i.stat().st_atime).strftime("%m/%d/%Y %I:%M %p"))
    table = list(zip(names , modes , times))
    for name , mode , time in sorted(table):
        text.insert(tk.END , f" {time}\t{mode}\t\t{name}\n")
    text.insert(tk.END , f"   {file_count} File(s): {size} bytes")
    text.insert(tk.END , f"\n   {dir_count} Dir(s)\n")
def md(name = ""):
    if name:
        for char in name:
            if char in INVALID:
                name = name.replace(char , "" , 1)
        try:
            os.mkdir(f"C:/{CURR_DIR}/{name}")
            text.insert(tk.END , f"\n\nDir '{name}' created in C:/{CURR_DIR}")
        except:
            text.insert(tk.END , f"\n'{name}' is not a valid name")
    else:
        text.insert(tk.END , f"\n'{name}' is not a valid name")
    text.insert(tk.END , "\n")
def host(catch = None):
    if catch:
        inspos = text.index(tk.INSERT)
        row = inspos[:inspos.find(".")]
        cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
        return
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    text.insert(tk.END , f"\nlocalhost name: {name}\nlocalhost IP Address: {ip}\n")
def start(object = ""):
    if object:
        for char in object:
            if char in INVALID:
                object = object.replace(char , "" , 1)
        try:
            os.startfile(object)
        except:
            try:
                os.startfile(f"C:/{CURR_DIR}/{object}")
            except:
                text.insert(tk.END , f"\n'{object}' is not an operable program, subdirectory, or file\n")
    else:
        text.insert(tk.END , f"\n'{object}' is not an operable program, subdirectory, or file\n")
def color(clr = ""):
    if clr:
        if clr.lower() == "red" or clr.lower() == "r":
            text.config(fg = RED)
        elif clr.lower() == "green" or clr.lower() == "g":
            text.config(fg = GREEN)
        elif clr.lower() == "blue" or clr.lower() == "b":
            text.config(fg = BLUE)
        elif clr.lower() == "white" or clr.lower() == "w" or clr.lower() == "d":
            text.config(fg = WHITE)
        else:
            text.insert(tk.END , f"\n'{clr}' is not a valid color\n")
    else:
        text.insert(tk.END , f"\n'{clr}' is not a valid color\n")
def whoami(catch = None):
    if catch:
        inspos = text.index(tk.INSERT)
        row = inspos[:inspos.find(".")]
        cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
        return
    device = socket.gethostname()
    if ctypes.windll.shell32.IsUserAnAdmin():
        text.insert(tk.END , "\nSYSTEM32\n")
    else:
        text.insert(tk.END , f"\n{device}/{USER}\n")
def ping(address = ""):
    if address:
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            result = subprocess.check_output(f"ping -n 4 {address}", startupinfo = startupinfo , stderr = subprocess.PIPE , stdin = subprocess.PIPE , universal_newlines = True)
        except subprocess.CalledProcessError:
            result = "Windows Interpreter encountered an error"
        text.insert(tk.END , f"\n{result}")
    else:
        text.insert(tk.END , f"\n'{address}' is not a valid address\n")

EXISTS = True
VERSION = "1.4 beta"
INVALID = ["\\" , "/" , ":" , "*" , "?" , "\"" , "<" , ">" , "|"]
BLACK = "#000000"
WHITE = "#ffffff"
RED = "#ff0000"
GREEN = "#00ff00"
BLUE = "#0000ff"
FONT = tkfont.Font(family = "Consolas" , size = 11)
ELEVATION = check_elevate()
if ELEVATION:
    USER = "SYSTEM32"
else:
    USER = getpass.getuser()
if USER == "SYSTEM32":
    CURR_DIR = "Users"
else:
    CURR_DIR = f"Users/{USER}"
PROMPTLEN = len(f"{USER}@{CURR_DIR}$")
strcmds = ["CD" , "EXIT" , "CLS" , "NEEDCMD" , "HELP" , "DIR" , "MD" , "HOST" , "START" , "COLOR" , "WHOAMI" , "PING"]
explanations = ["displays the current directory or migrates to the given one" , "quits the windows interpreter" , "clears the screen" , "replaces the windows interpreter with an instance of cmd.exe" , "displays this menu" , "displays all files and subdirectories in the current directory with recent access times" , "creates a new directory at the current location with the given name" , "gives the device name and ip address" , "opens the given program , file , or subdirectory of the current directory" , "changes the text color to one of: 'red' , 'blue' , or 'green'" , "displays the current user and the privileges of Windows Interpreter" , "sends packets to given address (URL or IP address) and determines connection speed"]
funcs = [cd , exit , cls , needcmd , help , dir , md , host , start , color , whoami , ping]
funcnames = dict(zip(strcmds , funcs))
ICON_PHOTO = tk.PhotoImage(file = str(Path(__file__).parents[0]) + "/window_icon.png")

root.title(f"{ELEVATION}Windows Interpreter")
root.iconphoto(True , ICON_PHOTO)
root.resizable(0 , 0)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row = 0 , column = 1 , sticky = "ns")
text = tk.Text(root , width = 120 , height = 30 , bg = BLACK , bd = 0 , font = FONT , fg = WHITE , selectbackground = WHITE , selectforeground = BLACK , insertbackground = WHITE , insertwidth = 8 , wrap = "char")
text.grid(row = 0 , column = 0)
scrollbar.config(command = text.yview)
text.config(yscrollcommand = scrollbar.set)

def begin(event):
    text.insert(0.0 , f"Windows Interpreter [Version {VERSION}]\n(c) 2020 Isaac Darling (Jones College Prep)\n\n{USER}@{CURR_DIR}$")
    text.focus_set()
def startline(event):
    global PROMPTLEN
    inspos = text.index(tk.INSERT)
    row = inspos[:inspos.find(".")]
    cmd = text.get(f"{row}.{PROMPTLEN}" , inspos)
    cmd_prefix = cmd[:cmd.find(" ")]
    cmd_suffix = cmd[cmd.find(" ") + 1:]
    if cmd.find(" ") == -1:
        cmd_prefix = cmd
        cmd_suffix = None
    if cmd_prefix.upper() in strcmds:
        if cmd_suffix:
            funcnames[cmd_prefix.upper()](cmd_suffix)
        else:
            funcnames[cmd_prefix.upper()]()
    elif cmd_prefix != "":
        text.insert(tk.END , f"\n'{cmd}' is not recognized as a command or operable program. Note: Windows Interpreter ignores elevation.\n")
    if EXISTS:
        text.insert(tk.END , f"\n{USER}@{CURR_DIR}$")
        text.see(tk.END)
        PROMPTLEN = len(f"{USER}@{CURR_DIR}$")
        return "break"
def illegaldel(event):
    inspos = text.index(tk.INSERT)
    insposx = int(inspos[inspos.find(".") + 1:])
    insposy = int(inspos[:inspos.find(".")])
    if event.keycode != 8 and event.keycode != 46:
        if insposx <= PROMPTLEN - 1 or insposy < int(text.index(tk.END)[:text.index(tk.END).find(".")]) - 1:
            text.mark_set(tk.INSERT , tk.END)
            return "break"
        else:
            pass
    else:
        if insposx <= PROMPTLEN or insposy < int(text.index(tk.END)[:text.index(tk.END).find(".")]) - 1:
            text.mark_set(tk.INSERT , tk.END)
            return "break"
        else:
            pass
    try:
        if int(text.index(tk.SEL_FIRST)[text.index(tk.SEL_FIRST).find(".") + 1:]) >= PROMPTLEN and int(text.index(tk.SEL_LAST)[:text.index(tk.SEL_LAST).find(".")]) >= int(text.index(tk.END)[:text.index(tk.END).find(".")]) - 1:
            pass
        elif int(text.index(tk.SEL_LAST)[:text.index(tk.SEL_LAST).find(".")]) >= int(text.index(tk.END)[:text.index(tk.END).find(".")]) - 1:
            text.mark_set(tk.INSERT , tk.END)
            return "break"
        else:
            pass
    except:
        pass

text.bind("<Configure>" , begin)
text.bind("<Return>" , startline)
text.bind("<Key>" , illegaldel)

root.mainloop()
