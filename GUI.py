from tkinter import Frame, Label, Tk, Checkbutton, IntVar, Button, Entry, StringVar, Toplevel, Scale, DoubleVar, ttk
from tkinter import filedialog as fd
import os
import shutil
import json
from io import StringIO
from html.parser import HTMLParser
from colorsys import hsv_to_rgb
import random as r

g_done = False

blacklisted = ["Badges.txt", "Items.txt", "InventoryGUI.txt"]

rootdir = ""
newfolderpath = ""
cycle = 0


class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack(side="left")

        self.italics = IntVar()
        self.bold = IntVar()
        self.size = IntVar()
        self.caps = IntVar()

        self.sourcefolder = StringVar()

        self.uppersize = StringVar(value="50")
        self.lowersize = StringVar(value="40")

        self.foldername = StringVar(value="Custom translation pack")
        self.error = StringVar(value="")

        self.cycle_step = StringVar(value="2")
        self.cycle_offset = IntVar(value=0)
        self.cycle_sat = DoubleVar(value=1.0)
        self.cycle_value = DoubleVar(value=1.0)

        self.ColourMode = StringVar()

        _row = 0
        Button(frame, text="Select source Folder",
               command=pickfoldersource, justify="left").grid(row=_row, column=0)
        Label(frame, textvariable=self.sourcefolder,
              justify="left").grid(row=_row, column=1, sticky="W")

        _row += 1
        ttk.Combobox(frame, state="readonly", values=[
                     "None", "Random", "Cycle"], textvariable=self.ColourMode, justify="left").grid(row=_row, column=0, sticky="W")

        _row += 1
        Button(frame, text="Cycle mode options",
               command=opensettings, justify="left").grid(row=_row, column=0, sticky="W")

        _row += 1
        Checkbutton(frame, text="Random Italics",
                    variable=self.italics, justify="left").grid(row=_row, column=0, sticky="W")

        _row += 1
        Checkbutton(frame, text="Random Bolding",
                    variable=self.bold, justify="left").grid(row=_row, column=0, sticky="W")

        _row += 1
        Checkbutton(frame, text="Random Capitals",
                    variable=self.caps, justify="left").grid(row=_row, column=0, sticky="W")

        _row += 1
        Checkbutton(frame, text="Random Sizing",
                    variable=self.size, justify="left").grid(row=_row, column=0, sticky="W")

        _row += 1
        Label(frame, text="Lower size limit:").grid(
            row=_row, column=0, sticky="W")
        Entry(frame, textvariable=self.lowersize, justify="left").grid(
            row=_row, column=1, sticky="W")

        _row += 1
        Label(frame, text="Upper size limit:").grid(
            row=_row, column=0, sticky="W")
        Entry(frame, textvariable=self.uppersize, justify="left").grid(
            row=_row, column=1, sticky="W")

        _row += 1
        Label(frame, text="Translations Name:").grid(
            row=_row, column=0, sticky="W")
        Entry(frame, textvariable=self.foldername, justify="left").grid(
            row=_row, column=1, sticky="W")

        _row += 1
        Button(frame, text="Apply", command=Generate,
               justify="left").grid(row=_row, column=0)

        Entry(frame, text=self.error)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def hsv_to_hex(hue: float, saturation: float, value: float) -> str:

    col = hsv_to_rgb(hue, saturation, value)
    return "#{:02x}{:02x}{:02x}".format(int(clamp(col[0]*255, 0, 255)), int(clamp(col[1]*255, 0, 255)), int(clamp(col[2]*255, 0, 255)))


def clamp(a, b=0, c=100): return max(b, min(c, a))


def get_rand_colour(): return "<color=" + \
    hsv_to_hex(r.randint(0, 359)/359.0, 1, 1) + ">"


def get_cycle_colour():
    global cycle
    cycle += clamp(int(app.cycle_step.get()), 1, 100)
    return "<color=" + hsv_to_hex((cycle % 359)/359.0, app.cycle_sat.get(), app.cycle_value.get()) + ">"


def rand_formatting(string: str, args: list):

    UseBold, UseItalics, UseCaps, UseSize, SizeLowerBounds, SizeUpperBound, ColourMode = args[
        0], args[1], args[2], args[3], args[4], args[5], args[6]

    if UseCaps:
        string = [string.lower(), string.upper()][int(r.random() > 0.5)]

    if ColourMode == "Random":
        string = get_rand_colour() + string + "</color>"
    if ColourMode == "Cycle":
        string = get_cycle_colour() + string + "</color>"

    if (r.random() > 0.5) and UseBold:
        string = "<b>" + string + "</b>"
    if (r.random() > 0.5) and UseItalics:
        string = "<i>" + string + "</i>"
    if (r.random() > 0.5) and UseSize:
        string = "<size={}>".format(
            r.randint(SizeLowerBounds, SizeUpperBound)) + string + "</size>"

    return string


def Generate():
    global newfolderpath, rootdir
    try:
        args = [app.bold.get(), app.italics.get(), app.caps.get(),
                app.size.get(), int(app.lowersize.get()), int(app.uppersize.get()),
                app.ColourMode.get()]
        if rootdir and app.foldername.get():
            segs = rootdir.split("/")[0:-1]
            newfolderpath = ""
            for c in segs:
                newfolderpath += c + "/"
            newfolderpath += app.foldername.get()
            try:
                shutil.rmtree(newfolderpath)
            except FileNotFoundError:
                pass  # The folder doesn't exist. good
            os.makedirs(newfolderpath)

            for filename in os.listdir(rootdir):
                if filename.endswith(".txt") and not filename in blacklisted:
                    with open(rootdir + "/" + filename, "r") as file:
                        content = file.read()
                        file.close()
                        content = strip_tags(content)

                        special_characters = ["\\", "[", "]", "(", ")"]
                        special_curly = False
                        special_square = False
                        special_next = False
                        special_flop = False

                        newfile = ""

                        for num, c in enumerate(content):
                            if (c in special_characters):
                                if c == "[":
                                    special_square = True
                                if c == "]":
                                    special_square, special_flop = False, True

                                if c == "{":
                                    special_curly = True
                                if c == "}":
                                    special_curly, special_flop = False, True

                                if c == "\\":
                                    special_next = True

                            if not (special_curly or special_square or special_next or special_flop or c == " "):
                                if not (c == "\n"):
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

                if filename == "manifest.json":
                    newfile = ""
                    with open(rootdir + "/" + filename, "r") as file:
                        content = file.read()
                        file.close()
                        _jsoncontent = (json.loads(content))
                        _jsoncontent["Name"] = app.foldername.get()
                        _jsoncontent["Authors"].append("Scordi's Translation Modifier")
                        with open(newfolderpath + "/" + filename, "w") as _newfile:
                            _newfile.write(json.dumps(_jsoncontent))
                            _newfile.close()

                if filename == "SCP079.txt":
                    with open(newfolderpath + "/" + filename, "r") as _newfile:
                        content = _newfile.readlines()
                        _newfile.close()
                        with open(newfolderpath + "/" + filename, "w") as _newfile:
                            newfile = content[0:len(content)-2]
                            newfile.append(
                                "<color=#ff0000>SCPs{0}</color><color=#020040>MTF & Guards{1}</color><color=#fff200>Scientists{2}</color><color=#ff8800>Class-D{3}</color><color=#026900>Chaos Insurgents{4}</color>")
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
    ccs.wm_title("Cycle Mode settings")
    _row = 0
    Label(ccs, text="Step:").grid(row=_row, column=0)
    Entry(ccs, textvariable=app.cycle_step).grid(row=_row, column=1)

    _row += 1
    Scale(ccs, from_=359, to_=0, length=100, resolution=1,
          variable=app.cycle_offset) .grid(row=_row, column=0)
    Scale(ccs, from_=1, to_=0, length=100, resolution=0.01,
          variable=app.cycle_sat) .grid(row=_row, column=1)
    Scale(ccs, from_=1, to_=0, length=100, resolution=0.01,
          variable=app.cycle_value) .grid(row=_row, column=2)

    _row += 1
    Label(ccs, text="Hue Offset").grid(row=_row, column=0)
    Label(ccs, text="Saturation").grid(row=_row, column=1)
    Label(ccs, text="Value").grid(row=_row, column=2)


root = Tk()
root.wm_title('SCP:SL Translation modifier')
app = App(root)


def on_closing():
    root.destroy()  # Destory the TK interface
    global g_done  # Specify g_done as a Global variable
    g_done = True  # Set done as true


root.protocol("WM_DELETE_WINDOW", on_closing)

while not g_done:
    try:
        root.update()  # Update the interface
    except:
        pass
try:
    root.destroy()  # Destroy the interface
except:
    pass
