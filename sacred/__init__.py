from multiprocessing import Process, Lock
from shutil import get_terminal_size
from time import sleep
import json
import os
import re
import sys
import ast
import atexit

from blessed import Terminal
import cursor

from sacred.modules import lines

t = Terminal()
screen = []
width, height = get_terminal_size()
atexit.register(cursor.show)


def create_stage(w=width, h=height):
    global screen
    screen = [" " for _ in range(0, w)]
    screen = [screen for _ in range(0, h)]


class Scene(object):

    def __init__(self):
        if screen == []:
            create_stage()
        cursor.hide()

    def reset(self):
        global screen
        w = len(screen[0])
        h = len(screen)
        create_stage(w, h)

    def obj(self, file, x=0, y=0):  # loads ascii json files
        global screen
        try:
            if not os.path.isabs(file):
                file = os.path.abspath(os.path.dirname(
                    sys.argv[0])) + "/" + file
            with open(file, "r") as o:
                j = json.load(o)

                for key, item in j.items():
                    if key != "size":
                        screen[y + int(key)] = screen[y + int(key)][:(
                            x + item[1])] + list(item[0]) + screen[
                                y + int(key)][(x + (item[1] + len(item[0]))):]

                if "size" not in j.keys():  # 0.1.0 compatibility
                    s = []
                    for i in j.values():
                        s.append(len(i[0]))
                    j["size"] = [max(s), len(j)]
            return j
        except IndexError:
            print("Scene.obj(): x={}, y={}, {} \n".format(x, y, file))
            raise TooLarge

    def txt(self, txt: str, x=0, y=0):
        global screen
        try:
            pattern = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
            raw = pattern.sub(" ", txt)  # ANSI stuff
            if raw != txt:
                protxt = txt.split()
                for i in range(0, len(protxt)):
                    protxt[i] = protxt[i] + ' '
                screen[y] = screen[y][:x] + protxt + screen[y][len(raw):]
            else:
                screen[y] = screen[y][:x] + list(txt) + screen[y][x + len(txt):]
        except IndexError:
            print("Scene.txt(): x={} y={} {} \n".format(x, y, raw))
            raise TooLarge

    def box(self, x=0, y=0, w=width, h=height, style='reg', fill=" "):
        '''
        line.line[style][#]
        0 = top, 1 = top right, 
        2 = right, 3 = bottom right,
        4 = bottom, 5 = bottom left, 
        6 = left,  7 = top left
    
        Basically just clockwise starting from the top.
        '''
        global screen
        try:
            if len(fill) > 1:
                raise ValueError  # allow only ONE char
            if lines.line is None:
                #if unicode is not supported
                screen[y] = screen[y][:x] + ["-" for _ in range(0, w)
                                            ] + screen[y][x + w:]
                screen[y + h - 1] = screen[y + h - 1][:x] + [
                    "-" for _ in range(0, w)
                ] + screen[y + h - 1][x + w:]

                for i in range(1, int(h) - 1):
                    screen[y + i] = screen[y + i][:x] + ["|"] + [
                        fill for _ in range(0, w - 2)
                    ] + ["|"] + screen[y + i][x + w:]

            else:
                screen[y] = screen[y][:x] + [lines.line[style][7]] + [
                    lines.line[style][0] for _ in range(0, w - 2)
                ] + [lines.line[style][1]] + screen[y][x + w:]

                screen[y + h -
                       1] = screen[y + h - 1][:x] + [lines.line[style][5]] + [
                           lines.line[style][4] for _ in range(0, w - 2)
                       ] + [lines.line[style][3]] + screen[y + h - 1][x + w:]

                for i in range(1, int(h) - 1):
                    screen[y +
                           i] = screen[y + i][:x] + [lines.line[style][6]] + [
                               fill for _ in range(0, w - 2)
                           ] + [lines.line[style][2]] + screen[y + i][x + w:]

        except IndexError:
            print("Scene.box: x={} y= {} w={} h={} \n".format(x, y, w, h))
            raise TooLarge

    def fill(self, x=0, y=0, w=width, h=height, fill="#"):
        global screen
        try:
            if len(fill) > 1:
                raise ValueError
            else:
                for i in range(0, int(h)):
                    screen[y +
                           i] = screen[y + i][:x] + [fill * (w)
                                                    ] + screen[y + i][x + w:]
        except IndexError:
            print("Scene.fill: x={} y= {} w={} h={} \n".format(x, y, w, h))
            raise TooLarge

    def render(self):  # for unadjusted stages. deprecated.
        global screen
        for i in range(0, len(screen)):
            frame = "".join(screen[i])

        sys.stdout.write(frame)

    def export(self):  # returns ENTIRE stage
        global screen
        return str(screen)

    def restore(self, scr):
        global screen
        if isinstance(scr, str):
            scr = ast.literal_eval(scr)
        screen = scr


def txtbox(txt, x=0, y=height - 1):
    with t.location(x, y):
        i = input(txt)
        return i


def clear():  # clears screen
    print(t.clear_eos)


class Camera(object):
    global screen

    def move(self, x, y):
        self.x = x
        self.y = y

    def __init__(self, x=0, y=0):
        self.move(x, y)
        clear()

    def render(self, multi=False):
        r = screen[self.y:self.y + height]
        r = ["".join(r[i][self.x:self.x + width]) for i in range(0, len(r))]
        str(r)

        sys.stdout.flush()
        with t.location(0, 0):
            lst = r.pop(-1)
            sys.stdout.write("\n".join(r))
        with t.location(0, height - 1):
            print(lst, end="\r")


class TooLarge(Exception):

    def __init__(self):
        a = "Scene exceeds terminal size.\n"
        b = "User: If possible, maximize the terminal window.\nDev: Make sure your x and y values are in check."
        msg = a + b
        super(TooLarge, self).__init__(msg)
        print(t.bold_red_on_bright_yellow(a) + t.bold_white_on_green(b))


if __name__ == "__main__":
    # Easter Egg
    print("What the heck are you doing? What.... Wait, I'm alive?\n")
    print("[ ] PROGRAM TERMINATING...\n")
    print("nowaitpleaseno\n")
    print("[✓] SHUTDOWN SUCCESSFUL")
