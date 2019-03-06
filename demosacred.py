from blessed import Terminal
import sacred
from time import sleep, time
from random import randrange
import math

t = Terminal()
scene = sacred.Scene()
back = sacred.Scene()
cam = sacred.Camera()
sd = 30  # star density
p = 10000  # Stage width
f = 25  # FPS
m = False  # multiprocessing
loop = True

sacred.create_stage(p, t.height)

r = [randrange(5, t.height - 3) for _ in range(1, p, 25)]


def bkground(warp=False):
    back.box()
    m = 0
    if warp:
        for i in range(math.floor(t.width / 2), p, sd):
            back.txt("________", i, r[m])
            m += 1
    else:
        for i in range(1, t.width, sd):
            back.txt(".", i, r[m])
            m += 1


def test(i):
    scene.obj("testassets/ent_e.json", i, 6)
    if i <= 7700:
        scene.obj("testassets/enterprise-kelvin.json", 7500, 30)
    if i <= 5200:
        scene.obj("testassets/stardestroyer.json", 5000, 23)
    if i <= 2700:
        scene.obj("testassets/milfalcon.json", 2500, 25)
    scene.txt("test i: {}".format(str(abs(i) - 5 / 5)), i - 148, t.height - 5)
    scene.txt("window x: {}".format(str(t.width)), i - 148, t.height - 4)
    scene.txt("window y: {}".format(str(t.height)), i - 148, t.height - 3)


def status(i, l):
    scene.txt("test i: {}".format(str(abs(i) - 5 / 5)), i, t.height - 5)
    scene.txt("window x: {}".format(str(t.width)), i, t.height - 4)
    scene.txt("window y: {}".format(str(t.height)), i, t.height - 3)
    scene.txt("fps: {}".format(1 / (time() - l)), i, t.height - 6)
    scene.txt("performance: {}%".format(((1 / f) / (time() - l)) * 100), i,
              t.height - 7)
    return (1 / f) / (time() - l)


def main():
    try:

        cam.move(0, 0)

        for i in range(5, 150):
            start_time = time()

            bkground()

            scene.obj("testassets/spacedock.json", 5, 3)
            scene.obj("testassets/ent_e.json", abs(i), 6)

            if not time() - start_time >= 1 / f:
                sleep((1 / f) - (time() - start_time))

            status(2, start_time)

            cam.render(multi=m)
            scene.reset()

        sleep(0.5)

        for i in range(150, p - 250, 25):
            start_time = time()

            cam.move(i - 150, 0)

            bkground(True)
            test(i)

            if not time() - start_time >= 1 / f:
                sleep((1 / f) - (time() - start_time))

            a = status(i - 148, start_time)

            cam.render(multi=m)
            scene.reset()

        return a

    except KeyboardInterrupt:
        sacred.clear()
        print("quitting")
        exit()

    except ValueError:
        print("FPS OR VALUE OF 'P' TOO HIGH")
        exit()


if loop:
    while True:
        main()
else:
    b = main()
