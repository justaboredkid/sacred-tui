# sacred-tui  ![travis-ci](https://api.travis-ci.org/justaboredkid/sacred-tui.svg?branch=development)
ASCII art import and terminal graphics made simple. 
  

[![asciicast](https://asciinema.org/a/236218.svg)](https://asciinema.org/a/236218)

  

  Let's say you want something like this in your script:
```
 _____________________________,----,__
|==============================<| /___\          ____,-------------.____
 `------------------.-----.---.___.--'     __.--'-----------------------`--.__
                     `._   `.            =======================================
                    ____`.___`._____,----'     `--------,----------------'
                   /_|___________-----<       ========,'
                                 `-.                ,'
                                    `----.______,--'
```
ASCII ᴀʀᴛ ᴍᴀᴅᴇ ʙʏ Jᴏsʜᴜᴀ Bᴇʟʟ  
  
And what if you wanted it at *exactly*, *precisely* 10 spaces to the right?
You can do this:
```
print("           _____________________________,----,__")
print("          |==============================<| /___\\          ____,-------------.____")
print("            `------------------.-----.---.___.--'     __.--'-----------------------`--.__")
print("                                `._   `.            =======================================")
print("                              ____`.___`._____,----'     `--------,----------------'")
print("                              /_|___________-----<       ========,'")
print("                                            `-.                ,'")
print("                                              `----.______,--'")
```
And add more spaces and backslashes and lose track of which line you added and then restart. **Eww no.**
  

Or maybe this:
```
from blessed import Terminal # pip install blessed

term = Terminal()

print(term.clear)

with open("ent_e.txt", "r") as f: # ent_e.txt contains the ASCII art itself
    ent = f.readlines()

with term.location(10, 0):
    for line in ent:
        print(line)
```
Wait a minute:
```
           _____________________________,----,__

|==============================<| /___\          ____,-------------.____

 `------------------.-----.---.___.--'     __.--'-----------------------`--.__

                     `._   `.            =======================================

                    ____`.___`._____,----'     `--------,----------------'

                   /_|___________-----<       ========,'

                                 `-.                ,'

                                    `----.______,--'
```                                  
*AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA the ship is falling apart!!!!*
  

## **Behold, sacred-tui.**
```
import sacred

scene = sacred.Scene()
cam = sacred.Camera()
sacred.clear()

scene.obj("ent_e.json", 10, 0) # asciigen ent_e.txt ent_e
cam.render()
```
and voilà!
```
           _____________________________,----,__
          |==============================<| /___\          ____,-------------.____
           `------------------.-----.---.___.--'     __.--'-----------------------`--.__
                               `._   `.            =======================================
                              ____`.___`._____,----'     `--------,----------------'
                             /_|___________-----<       ========,'
                                           `-.                ,'
                                              `----.______,--'
```                                            
Though you have to convert the ASCII art from text to the json format that my script uses (asciigen), there is no hassle for just putting the spaceship a little bit more to the right. Or a bit toward the bottom. Anywhere on the terminal.

***ANYWHERE.***  
  
  
[*Maniacal laughter*](https://www.youtube.com/watch?v=gY2k8_sSTsE)  
  
  
And using this, you can still make complex scenes like this:
```
from blessed import Terminal
from math import floor
import sacred

scene = sacred.Scene()
t = Terminal()

# snippet from https://github.com/justaboredkid/ultimate-tic-tac-toe
sacred.clear()

scene.box()
scene.obj("objs/grid.json", floor(t.width / 2) - 12, floor(t.height / 2) - 11) # JSON file not included
scene.txt("For best gameplay, use numpad and 80x24 terminal", t.width - 49,
    t.height - 2)
scene.txt("1) Single Player", 4, 5)
scene.txt("2) Local Multiplayer", 4, 6)
scene.txt("3) Help", 4, 7)
scene.txt("4) Exit", 4, 8)
scene.txt("Ultimate Tic Tac Toe TERMINAL EDITION", 0, 0)
scene.render()
```
  
```
Ultimate Tic Tac Toe TERMINAL EDITION------------------------------------------
|                                                                             |
|                            . .  |  . .  |  . .                              |
|                           .|.|. | .|.|. | .|.|.                             |
|                            | |  |  | |  |  | |                              |
|   1) Single Player        .|.|. | .|.|. | .|.|.                             |
|   2) Local Multiplayer     | |  |  | |  |  | |                              |
|   3) Help                       |       |                                   |
|   4) Exit                 ------+-------+------                             |
|                            . .  |  . .  |  . .                              |
|                           .|.|. | .|.|. | .|.|.                             |
|                            | |  |  | |  |  | |                              |
|                           .|.|. | .|.|. | .|.|.                             |
|                            | |  |  | |  |  | |                              |
|                                 |       |                                   |
|                           ------+-------+------                             |
|                            . .  |  . .  |  . .                              |
|                           .|.|. | .|.|. | .|.|.                             |
|                            | |  |  | |  |  | |                              |
|                           .|.|. | .|.|. | .|.|.                             |
|                            | |  |  | |  |  | |                              |
|                                 |       |                                   |
-------------------------------For best gameplay, use numpad and 80x24 terminal
```
  
  
## *Wait a minute, I have bigger ASCII art, but `scene.render()` won't allow objects to exceed terminal size. EXPLAIN*

That's where `Camera()` and `create_stage()` comes in.  

`Camera.move()` allows you to move around the stage. Using `create_stage()` you can define an area that is bigger than the terminal size.  

This means you can move around your camera instead of creating individual frames just to view a different part of the large model.

See [`demosacred.py`](https://github.com/justaboredkid/sacred-tui/blob/master/demosacred.py) for the full potential of this library.

  

# Terminology

*Camera*:  V-Cam. Something like the [Virtual Camera in Adobe Animate](https://helpx.adobe.com/ca/animate/how-to/virtual-camera.html).  
*Scene*:  Layer of objects.  
*Screen/Stage*:  The work area. It can be larger than the terminal size.  
*Objects*: Text, Boxes, ASCII art etc.



# Installation
Clone repo and install:
```
# Dependency
pip install blessed


python3 setup.py install
```
or use pip:
```
pip install sacred-tui
```

*Note: does not support Python 2*

# Documentation
### [asciigen.py](https://github.com/justaboredkid/sacred-tui/blob/master/asciigen.py)
Python script for generating ASCII json files. All you need to do is to grab some ASCII art (from the web or somewhere else), type `asciigen` in the terminal to covert it into json, and:
```
import sacred

scene = sacred.Scene()

sacred.clear()
scene.obj("test.json", 5, 10)
scene.render()
```
Usage:
```
asciigen.py <inputfile> <outputname>
```

The data is in this format:
```
{"line#":["text", SpaceBeforeText]}
```
Where `line#` means which line it is, `text` being what is printed on the line, and `SpaceBeforeText` means the, well, space before the line. Note that this tool isn't perfect, so you might have to edit the `SpaceBeforeText` part.
### sacred.create_stage(w=width, h=height)
This (by default) creates a stage that is the size of the terminal. By manipulating the `w` and `h` values, you can set the stage size to whatever you want.  

Want a epic long chase? Increase the width and move the camera around by using `sacred.Camera()`.  

*Note: The camera always starts at the top left corner of the stage*

Args:
```
w (int): width of the stage
h (int): height to the stage
```

## *sacred.Scene(object)*
Class for all objects in render. It has the following objects:
### Scene.reset()
This function clears everything in the scene, kind of like a 'Erase everything on the scene' function. It keeps the original stage size as well.


### Scene.obj(file, x=0, y=0)
Imports ASCII json files.  Those are generated by `asciigen`. It adds the ASCII art to the scene as well as returning the json.

Args:
```
file (str): path to the .json file
x (int): position on the x axis
y (int): position on the y axis
```
### Scene.txt(txt, x=0, y=0)
Adds text to the position (x, y). Similar to `print()`, but you can put it wherever you want on the scene.


Args:
```
txt (str): content to print at (x,y)
x (int): position on the x axis
y (int): position on the y axis
```
### Scene.box(x=0, y=0, w=t.width - 1, h=t.height - 1, fill=" ")
Adds a box on terminal. Creates a box around the terminal by default. (Note that a character on the terminal is a tall rectangle, which means that having the same height and width does not create a square.)
  
  
*Example:*
```
import sacred

scene = sacred.Scene()
cam = sacred.Camera() 

scene.box(5, 5, 10, 10, fill="*")
cam.render()
```
*Output:*
```


     ┌────────┐
     │********│
     │********│
     │********│
     │********│
     │********│
     │********│
     │********│
     │********│
     └────────┘

     
```
  
Args:
```
x (int): position on x axis
y (int): position on y axis
w (int): width (by char)
h (int): height (by char)
fill (str): content that fills inside box. (Will return ValueError if fill is more than one char.)
```


### ~~Scene.render()~~ (deprecated)

**`this has been deprecated. Will remove soon.`**

### Scene.export()
This function takes the stage, converts it into string, and return the stage. You could do whatever you want with it, it is a large nested list. That includes but not limited to storing it as a variable.

### Scene.restore(scr)
This takes the output of `Scene.export()` and restore it. You can restore the scene from the aforementioned variable.



## sacred.Camera(object)
Class for moving around the camera, using the terminal like a viewport.

### Camera.move(x=0, y=0)

Moves the the camera inside stage. This way you can have objects that are bigger than the terminal and it will still be able to render.

### Camera.render(multi=False)

Renders (or print, if you prefer) all the objects added. Note that it prints in the order of the added objects, so each object goes on top of other objects in the order of the objects added.

The `multi` argument allows multi-thread rendering. *This is still work in progress.*


## sacred.TooLarge(Exception)
Error raised when the objects that are added are bigger than the width of the terminal itself.

So if you do this in a 80x24 terminal:
```
scene.box(0, 0, 500, 500)
scene.render()
```
then this happens:
```
Scene exceeds terminal width
User: If possible, maximize the terminal window.
Dev: Make sure your x values are in check.
Traceback (most recent call last):
  File "test.py", line 7, in <module>
    scene.render()
  File "/home/henry/Github/sacred/sacred.py", line 47, in render
    printobj(obj, self.pos[i][0], self.pos[i][1])
  File "/home/henry/Github/sacred/sacred.py", line 83, in printobj
    raise TooLarge
sacred.TooLarge
```
## sacred.txtbox(txt, x=0, y=t.height - 1)
When `input()` is not enough. This is basically a moveable version of that, where you can set the position of it at anywhere.

By default, it prints from the bottom of the terminal.

## sacred.clear()
Clears terminal by printing spaces by the width and height of the terminal. Not very efficient, but effective.



