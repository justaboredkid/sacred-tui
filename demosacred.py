import sacred
import blessed

scene = sacred.Scene()
cam = sacred.Camera()
t = blessed.Terminal()
sacred.clear()

scene.obj("testassets/spacedock.json", 5, 0)
scene.obj("testassets/ent_e.json", 10, 3)
scene.box(0, 15, sacred.width, sacred.height - 16)
scene.txt(t.bright_red_on_bright_yellow("tests are inevitable"), 5, 30)
cam.render()
