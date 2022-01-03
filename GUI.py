from tkinter import Frame, Label, Tk, Checkbutton, IntVar, Button, Entry, StringVar, Listbox, Toplevel, Scale, DoubleVar
from tkinter import filedialog as fd
import os, shutil, json
from io import StringIO
from html.parser import HTMLParser
from colorutils import Color
import random as r

g_done = False

blacklisted = ["Badges.txt", "Items.txt", "InventoryGUI.txt"]

rootdir = ""
newfolderpath = ""
cycle = 0

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.italics = IntVar()
        self.bold = IntVar()
        self.size = IntVar()
        self.caps = IntVar()
        
        self.sourcefolder = StringVar()
        
        self.uppersize = StringVar(value="50")
        self.lowersize = StringVar(value="40")
        
        self.foldername = StringVar(value="Custom translation pack")
        self.error = StringVar(value="")
        
        self.cc_step = StringVar(value="2")

        self.cc_offset = IntVar(value=0)
        self.cc_sat = DoubleVar(value=1.0)
        self.cc_value = DoubleVar(value=1.0)
        
        _row = 0
        Button (frame, text="Select source Folder", command=pickfoldersource).grid(row=_row, column=0)
        Label (frame, textvariable=self.sourcefolder).grid(row=_row, column=1)
        
        _row +=1
        self.colourmodes = Listbox(frame, height=4)
        self.colourmodes.insert(1, "None")
        self.colourmodes.insert(2, "Random")
        self.colourmodes.insert(3, "Cycle")
        self.colourmodes.grid(row=_row, column=0)
        
        _row +=1
        Button (frame, text="Cycle mode options", command=opensettings).grid(row=_row, column=0)
        
        _row +=1
        Checkbutton (frame, text="Random Italics", variable=self.italics).grid(row=_row, column=0)
        
        _row +=1
        Checkbutton (frame, text="Random Bolding", variable=self.bold).grid(row=_row, column=0)
        
        _row +=1
        Checkbutton (frame, text="Random Capitals", variable=self.caps).grid(row=_row, column=0)
        
        _row +=1
        Checkbutton (frame, text="Random Sizing", variable=self.size).grid(row=_row, column=0)
        
        _row +=1
        Label (frame, text="Lower size limit").grid(row=_row, column=0)
        Entry (frame, textvariable=self.lowersize).grid(row=_row, column=1, sticky="W")
        
        _row +=1
        Label (frame, text="Upper size limit").grid(row=_row, column=0)
        Entry (frame, textvariable=self.uppersize).grid(row=_row, column=1, sticky="W")
        
        _row +=1        
        Label (frame, text="Translations Name").grid(row=_row, column=0)
        Entry (frame, textvariable=self.foldername).grid(row=_row, column=1, sticky="W")
        
        _row +=1
        Button (frame, text="Apply", command=Generate).grid(row=_row, column=0)
        
        Entry (frame, text=self.error)

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def loopover(a, b=0, c=359):
    while a > c: a -= c
    while a < b: a += c
    return a

def clamp(a, b=0, c=100):
    if a < b: return b
    if a > c: return c
    return a

def get_rand_colour(): return "<color=" + Color(hsv=(r.randint(0, 359), 1, 1)).hex + ">"

def get_cycle_colour():
    global cycle
    cycle += clamp(int(app.cc_step.get()), 1, 100)
    return "<color=" + Color(hsv=(loopover(cycle), app.cc_sat.get(), app.cc_value.get())).hex + ">"

def rand_formatting(string, args):
    _bold, _italics, _caps, _size, _sizeL, _sizeU = args[0], args[1], args[2], args[3], args[4], args[5]

    if len(args[6]) >=1: _colmode =  args[6][0]
    else: _colmode = 0
    
    if  round(r.random()) and _caps:
        if round(r.random()): string = string.upper()
        else: string = string.lower()
    
    if _colmode==1: string = get_rand_colour() + string + "</color>"
    if _colmode==2: string = get_cycle_colour() + string + "</color>"

    if  round(r.random()) and _bold: string = "<b>" + string + "</b>"
    if  round(r.random()) and _italics: string = "<i>" + string + "</i>"  
    if round(r.random()) and _size: string = "<size={}>".format(r.randint(_sizeL, _sizeU)) + string + "</size>"
 
    return string

def Generate():
    global newfolderpath, rootdir
    try:
        args = [ app.bold.get(), app.italics.get(), app.caps.get(), app.size.get(), int(app.lowersize.get()), int(app.uppersize.get()), app.colourmodes.curselection()]
        if rootdir and app.foldername.get():
            segs = rootdir.split("/")[0:-1]
            newfolderpath = ""
            for c in segs:
                newfolderpath += c + "/"
            newfolderpath += app.foldername.get()
            try:
                shutil.rmtree(newfolderpath)
            except FileNotFoundError:
                pass ### The folder doesn't exist. good
            os.makedirs(newfolderpath)
            
            for filename in os.listdir(rootdir):
                if filename.endswith(".txt") and not filename in blacklisted:
                    with open(rootdir + "/" + filename, "r") as file:
                        content = file.read()
                        file.close()
                        content = strip_tags(content)
                        
                        special_characters = ["\\", "[","]", "(", ")"]
                        special_curly = False
                        special_square = False
                        special_next = False
                        special_flop = False
                        
                        newfile = ""
                        
                        for num, c in enumerate(content):
                            if (c in special_characters):
                                if c == "[": special_square = True
                                if c == "]": special_square, special_flop = False, True
                                
                                if c == "{": special_curly = True
                                if c == "}": special_curly, special_flop = False, True
                                
                                if c == "\\": special_next = True
                                
                            
                            if not (special_curly or special_square or special_next or special_flop or c == " "):
                                if not (c=="\n"): newfile += rand_formatting(c, args)
                                else: newfile += c
                            else: newfile += c
            
                            if special_next:
                                special_flop = True
                                special_next = False
                            else:
                                special_flop = False
                        
                        with open(newfolderpath + "/" + filename, "w") as _newfile:
                            _newfile.write(newfile)
                            _newfile.close()
                
                if filename == "manifest.json":
                    newfile = ""
                    with open(rootdir + "/" + filename, "r") as file:
                        content = file.read()
                        file.close()
                        _jsoncontent = (json.loads(content))
                        _jsoncontent["Name"] = app.foldername.get()
                        _jsoncontent["Authors"].append("Scordi8's Translation Modifier")
                        with open(newfolderpath + "/" + filename, "w") as _newfile:
                            _newfile.write(json.dumps(_jsoncontent))
                            _newfile.close()
                
                if filename == "SCP079.txt":
                    with open(newfolderpath + "/" + filename, "r") as _newfile:
                        content = _newfile.readlines()
                        _newfile.close()
                        with open(newfolderpath + "/" + filename, "w") as _newfile:
                                newfile = content[0:len(content)-2]
                                newfile.append("<color=#ff0000>SCPs{0}</color><color=#020040>MTF & Guards{1}</color><color=#fff200>Scientists{2}</color><color=#ff8800>Class-D{3}</color><color=#026900>Chaos Insurgents{4}</color>")
                                _newfile.writelines(newfile)

                
                if filename in blacklisted:
                    with open(rootdir + "/" + filename, "r") as file:
                        content = file.read()
                        file.close()
                        newfile = ""
                        for c in content:
                            newfile += c
                        
                        with open(newfolderpath + "/" + filename, "w") as _newfile:
                            _newfile.write(newfile)
                            _newfile.close()
  
    except Exception as err:
        print(err)
        app.error.set(err)
    
def pickfoldersource():
    global rootdir
    rootdir = (fd.askdirectory(title="Select source Folder"))
    app.sourcefolder.set(rootdir)
    print(rootdir)

def opensettings():
    ccs = Toplevel(root)
    ccs.wm_title("Cycle settings")
    _row = 0
    Label (ccs, text="Step:").grid(row=_row, column=0)
    Entry (ccs, textvariable=app.cc_step).grid(row=_row, column=1)
    
    _row +=1
    Scale (ccs, from_=359, to_=0, length=100, resolution=1, variable=app.cc_offset) .grid(row=_row, column=0)
    Scale (ccs, from_=1, to_=0, length=100, resolution=0.01, variable=app.cc_sat) .grid(row=_row, column=1)
    Scale (ccs, from_=1, to_=0, length=100, resolution=0.01, variable=app.cc_value) .grid(row=_row, column=2)
    
    _row +=1
    Label (ccs, text="Hue Offset").grid(row=_row, column=0)
    Label (ccs, text="Saturation").grid(row=_row, column=1)
    Label (ccs, text="Value").grid(row=_row, column=2)
    
root = Tk()
root.wm_title('SCP:SL Translation modifier')
app = App(root)

def on_closing():
    root.destroy()
    global g_done
    g_done = True

root.protocol("WM_DELETE_WINDOW", on_closing)

while not g_done:
    try:
        root.update()
    except:
        pass
try:
    root.destroy()
except:
    pass
