from tkinter import Frame, Label, Tk, Checkbutton, IntVar, Button, Entry, StringVar
from tkinter import filedialog as fd
import os, shutil
from io import StringIO
from html.parser import HTMLParser
from colorutils import Color
import random as r

g_done = False

blacklisted = ["Badges.txt", "Items.txt"]

rootdir = ""
newfolderpath = ""

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.colour = IntVar()
        self.italics = IntVar()
        self.bold = IntVar()
        self.size = IntVar()
        self.caps = IntVar()
        
        self.sourcefolder = StringVar()
        
        self.uppersize = StringVar()
        self.uppersize.set("50")
        
        self.lowersize = StringVar()
        self.lowersize.set("30")
        
        self.foldername = StringVar()
        self.foldername.set("Custom translation pack")
        self.error = StringVar()
        self.error.set("")
        
        Button (frame, text="Select source Folder", command=pickfoldersource).grid(row=0, column=0)
        Label (frame, textvariable=self.sourcefolder).grid(row=0, column=1)
        
        Checkbutton (frame, text="Random Colour", variable=self.colour).grid(row=1, column=0)
        Checkbutton (frame, text="Random Italics", variable=self.italics).grid(row=2, column=0)
        Checkbutton (frame, text="Random Bolding", variable=self.bold).grid(row=3, column=0)
        Checkbutton (frame, text="Random Capitals", variable=self.caps).grid(row=4, column=0)
        
        Checkbutton (frame, text="Random Sizing", variable=self.size).grid(row=5, column=0)
        Label (frame, text="Lower size limit").grid(row=6, column=0)
        Entry (frame, textvariable=self.lowersize).grid(row=6, column=1, sticky="W")
        Label (frame, text="Upper size limit").grid(row=7, column=0)
        Entry (frame, textvariable=self.uppersize).grid(row=7, column=1, sticky="W")
        
        
        Label (frame, text="Translations Name").grid(row=8, column=0)
        Entry (frame, textvariable=self.foldername).grid(row=8, column=1, sticky="W")
        
        
        Button (frame, text="Apply", command=Generate).grid(row=9, column=0)
        
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
    """
    

    Parameters
    ----------
    html : str
        HTML data to get stripped of HTML tags (<> tags)

    Returns
    -------
    str
        DESCRIPTION.

    """
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_rand_colour():
    """
    Returns
    -------
    str
        String with a random Hue HSV colour

    """
    
    return "<color=" + Color(hsv=(r.randint(0, 359), 1, 1)).hex + ">"

def rand_formatting(string, args):
    _colour, _bold, _italics, _caps, _size, _sizeL, _sizeU = args[0], args[1], args[2], args[3], args[4], args[5], args[6]
    
    if  round(r.random()) and _caps:
        if round(r.random()):
            string = string.upper()
        else:
            string = string.lower()
    
    if _colour: string = get_rand_colour() + string + "</color>"

    if  round(r.random()) and _bold: string = "<b>" + string + "</b>"
    if  round(r.random()) and _italics: string = "<i>" + string + "</i>"
    
    if round(r.random()) and _size: string = "<size={}>".format(r.randint(_sizeL, _sizeU)) + string + "</size>"
 
    return string

       
def Generate():
    global newfolderpath, rootdir
    try:
        args = [app.colour.get(), app.bold.get(), app.italics.get(), app.caps.get(), app.size.get(), int(app.lowersize.get()), int(app.uppersize.get())]
        if rootdir and app.foldername.get():
            segs = rootdir.split("/")[0:-1]
            # print(segs)
            newfolderpath = ""
            for c in segs:
                newfolderpath += c + "/"
            newfolderpath += app.foldername.get()
            # print(newfolderpath)
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
                                if not (c=="\n"):
                                    newfile += rand_formatting(c, args)
                                else:
                                    newfile += c
                            else:
                                newfile += c
            
            
                            if special_next:
                                special_flop = True
                                special_next = False
                            else:
                                special_flop = False
                        
                        with open(newfolderpath + "/" + filename, "w") as _newfile:
                            _newfile.write(newfile)
                            _newfile.close()
    
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
    
   
def pickfoldersource():
    global rootdir
    rootdir = (fd.askdirectory(title="Select source Folder"))
    app.sourcefolder.set(rootdir)
    print(rootdir)
        

root = Tk()

root.event_generate("<<Foo>>", when="tail")
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
