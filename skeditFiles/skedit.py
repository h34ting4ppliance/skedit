#!/usr/bin/python3

# Copyright 2020 Patrick Warren

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import tkinter
import tkinter.filedialog as fd
from sys import argv, exit
import os
from platform import system
from math import floor

# Logging functions
def log(n):
    print("[#]", n)
def warn(n):
    print("[!]", n)
def die(n):
    print("[XX]", n)
    exit(1)

# linux users - this reads .Xresources file from your $HOME directory.
# this means your colors will restore to default if you run skedit as root.
# to fix this, copy your .Xresources to /root/
if system() == "Linux":
    home = os.environ["HOME"]
    # or, change 'home+"/.Xresources"' to '"yourusername/.Xresources"' in the follwing line
    try:
        Xresources = open(home+"/.Xresources")
        colors = Xresources.read()
        Xresources.close()
    except FileNotFoundError:
        pass

# read config file
if system() == "Windows":
    configPath = "C:\\Program Files\\skeditFiles\\skeditConf"
else: # Assuming other operating systems are UNIX-like
    configPath = "/usr/share/skeditFiles/skeditConf"

# Checks if the file exists
try:
    configPath = open(configPath)
except FileNotFoundError:
    die("skedit configuration missing.")

config = configFile.readlines()
configFile.close()

# get size from config file
defSize = config[config.index("defaultSize:\n") + 1]
defSize = defSize[:-1]
print(defSize)

filename = None

def get_text():
    t = text.get(0.0, tkinter.END).rstrip()
    if t[:-1] != '\n':
        t += '\n'
    return t

def newFile(self):
    global filename
    filename = "scratch document"
    text.delete(0.0, tkinter.END)
    root.title(filename+" - skedit")

def save(self):
    # NOTE : No need to set a variable as global when it comes to only read it.
    t = get_text()
    with open(filename, 'w') as f:
        f.write(t)

def saveAs(self):
    global filename
    fn = fd.asksaveasfilename(initialdir="/gui/images", title="save as", defaultextension='.txt')
    with open(fn, 'w') as f:
        root.title(fn+" - skedit")
        t = get_text()
        try:
            f.write(t)
        except PermissionError:
            # messagebox.showinfo("skedit error", "Permission Denied")   
            text.delete(0.0, tkinter.END)
        except:
            pass
        else:
            filename = fn

def openFile(self):
    global filename
    fn = fd.askopenfilename(initialdir="/gui/images", title="open file")
    
    try:
        t = open(fn, 'r').read()
    except:
        return
    else:
        filename = fn
    root.title(filename+" - skedit")
    text.delete(0.0, tkinter.END)
    text.insert(0.0, t)

def gotoTop(self):
    text.mark_set("insert", "%d.%d" % (0, 0))

# def gotoBot(self):
#     text.mark_set("insert", "%d.%d" % (tkinter.END, tkinter.END))

def removeLine(self):
    curLine = float(floor(float(text.index(tkinter.INSERT))))
    text.delete(curLine, curLine+1)

#Tk
root = tkinter.Tk()
root.title("scratch document - skedit")

#bindings
root.bind('<Control-s>', save)
root.bind('<Control-n>', newFile)
root.bind('<Control-d>', saveAs)
root.bind('<Control-o>', openFile)
root.bind('<Control-t>', gotoTop)
# root.bind('<Control-b>', gotoBot)
root.bind('<Control-x>', removeLine)

text = tkinter.Text(root)
root.update()
text.configure(background='white', height=root.winfo_height(), width=root.winfo_width())
root.geometry(defSize)
root.maxsize(1500, 1000)
root.update()
text.focus_set()
print (root.winfo_geometry())

text.pack()
try:
    if system() == "Windows":
        root.iconphoto(False, tkinter.PhotoImage(file='C:\\Program Files\\skeditFiles\\icon.png'))
    else:
        root.iconphoto(False, tkinter.PhotoImage(file='/usr/share/skeditFiles/icon.png'))
except:
    pass

root.mainloop()
