from multiprocessing import Process, Lock
from shutil import get_terminal_size
from time import sleep
import json
import os
import re
import sys
from blessed import Terminal
from sacred.modules import lines

t = Terminal()
screen = []
width, height = get_terminal_size()


def create_stage(w=width, h=height):
    global screen
    screen = [w * " " for _ in range(0, h - 1)]


class Scene(object):

    def __init__(self):
        if screen is None:
            create_stage()

    def reset(self):
        global screen
        screen = [len(screen[0]) * " " for i in range(0, len(screen))]

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
                            x + item[1])] + item[0] + screen[y + int(key)][(
                                x + (item[1] + len(item[0]))):]

                if "size" not in j.keys():  # 0.1.0 compatibility
                    s = []
                    for i in j.values():
                        s.append(len(i[0]))
                    j["size"] = [max(s), len(j)]
            return j
        except IndexError:
            print("Scene.obj(): {} \n".format(file))
            raise TooLarge

    def txt(self, txt: str, x=0, y=0):
        global screen
        try:
            raw = re.sub(r"\x1b\[\d{1,3}m|\x1b\(B\x1b\[m", "",
                         txt)  # ANSI stuff
            screen[y] = screen[y][:x] + txt + screen[y][x + len(raw):]
        except IndexError:
            print("Scene.txt(): {} \n".format(raw))
            raise TooLarge

    def box(self, x=0, y=0, w=width, h=height - 1, style='reg', fill=" "):
        global screen
        try:
            if len(fill) > 1:
                raise ValueError  # allow only ONE char
            if lines.line is None:
                #if unicode is not supported
                screen[y] = screen[y][:x] + "-" * w + screen[y][x + w:]
                screen[y + h -
                       1] = screen[y + h - 1][:x] + "-" * w + screen[y + h -
                                                                     1][x + w:]

                for i in range(0, int(h) - 2):
                    screen[y + i + 1] = screen[y + i][:x] + "|" + fill * (
                        w - 2) + "|" + screen[y + i][x + w:]

            else:
                screen[
                    y] = screen[y][:
                                   x] + lines.line[style][7] + lines.line[style][0] * (
                                       w - 2
                                   ) + lines.line[style][1] + screen[y][x + w:]
                screen[
                    y + h -
                    1] = screen[y + h -
                                1][:
                                   x] + lines.line[style][5] + lines.line[style][4] * (
                                       w - 2
                                   ) + lines.line[style][3] + screen[y + h -
                                                                     1][x + w:]

                for i in range(0, int(h) - 2):
                    screen[
                        y + i +
                        1] = screen[y + i][:x] + lines.line[style][6] + fill * (
                            w - 2) + lines.line[style][2] + screen[y + i][x +
                                                                          w:]

        except IndexError:
            print("Scene.box: w={} h={} \n".format(w, h))
            raise TooLarge

    def render(self):  # for unadjusted stages. deprecated.
        global screen
        frame = "\n".join(screen) + "\n"

        sys.stdout.write(frame)

    def export(self):
        global screen
        frame = "\n".join(screen) + "\n"

        return frame


class Camera(object):
    global screen

    def move(self, x, y):
        self.x = x
        self.y = y

    def __init__(self, x=0, y=0):
        self.move(x, y)

    def render(self, multi=False):
        r = screen[self.y:self.y + height]
        r = [r[i][self.x:self.x + width] for i in range(0, len(r))
            ]  # can't think of any better ideas
        if multi:
            lock = Lock()

            def f(l, i):
                l.acquire()

                sys.stdout.flush()
                with t.location(0, i):
                    sys.stdout.write("\n\n".join(r[i::2]) + "\n")
                l.release()

            for i in range(2):
                Process(target=f, args=(lock, i)).start()

        else:
            sys.stdout.flush()
            with t.location(0, 0):
                sys.stdout.write("\n".join(r) + "\n")

        t.location(0, height - 1)


class TooLarge(Exception):

    def __init__(self):
        a = "Scene exceeds terminal size.\n"
        b = "User: If possible, maximize the terminal window.\nDev: Make sure your x and y values are in check."
        msg = a + b
        super(TooLarge, self).__init__(msg)
        print(t.bold_red_on_bright_yellow(a) + t.bold_white_on_green(b))


def txtbox(txt, x=0, y=height - 1):
    with t.location(x, y):
        i = input(txt)
        return i


def clear():  # clears screen
    print((width * " " + "\n") * height)


if "__name__" == "__main__":
    print("What the heck are you doing?")
