# SCPSL_Translation_Randomiser
Script to apply random rich text formatting to SCP: Secret Laboratory translation files.

# How to use

### Step 1: Run the script
This can be done by downloading and running the code in [GUI.py](https://github.com/Scordi8/SCP-SL-Translation-Randomiser/blob/main/GUI.py) or by downloading a [release](https://github.com/Scordi8/SCP-SL-Translation-Randomiser/releases) exe.

### Step 2: Source folder
The Source folder is where the script will copy the text from. It will be located in the games files for SCP: Secret Laboratory, which can be found by browsing the games's local files from it's launcher (e.g. Steam, Discord). Once accessed, select your chosen language folder from the the Translations folder.

Once selected, the path should look similar to this: <ins>C:\Program Files (x86)\Steam\steamapps\common\SCP Secret Laboratory\Translations\English (default)</ins>, but will depend on your install location.

### Step 3: Colour Mode
Default Colour Mode is Cycle, however by interacting with the drop-down options, it can be changed to *None* or *Random*. None will apply no colour variation to the text, and Random will make every letter a random colour.

### Step 3.5 (Optional): Cycle Mode Options
Underneath the Colour Mode drop-down, the button Cycle mode options allows modification of the colour cycling.\
__Step__ is how much the colour changes per character. As all values are in the [HSV colour space](https://en.wikipedia.org/wiki/HSL_and_HSV), this means it will take (360/Steps) steps to return to the starting colour. A step of 2 will take 180 steps, and a step of 10 will take 36 steps before reaching the starting colour.  
__Saturation__ controls how [saturated](https://en.wikipedia.org/wiki/Colorfulness) the colour are. Higher values mean more vibrant colours, lower values means duller colours.  
__Value__ controls the vibrance of the colour. Lower values cause darker colours (0 is black) and higher values cause brighter colours.  

### Step 4: Formatting
The script provides the additional options to randomize italics, boldness, case, and font size.
__Italics, Bolding__ and __Capitalization__ can all be controlled using the listed checkboxes underneath the ColourMode Options.  
__Font Size__ Has a checkbox, and is controlled by it's following fields: *Lower size limit* and *Upper size limit*. 

### Step 5: Translation Name
The final field, Translation Name, is what the generated folder will be titled, and the name that will show up in-game. Avoid naming it after a pre-existing translation, because it *will* overwrite them. If you do overwrite important translations, you can retrieve them [here](https://github.com/northwood-studios/SCPSL-Translations) or by verifying your game files.

### Step 6: Generate
It's self explanatory.

### Step 7: Select your custom translation
Run or reload SCP:SL, go to settings/other, search the language/translations box for the name you picked in step 5, and select it.
<ins>If the new translations comes up red in the translations list, it will still work. It is simply missing the optional manifest.json file. Likewise, not all text fields are compatable with rich text formatting, so some things may show up as raw messy text.</ins>  

If contacting me is necessary, do so through the Oceanic SL Community
