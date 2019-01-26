import unittest
import sacred

scene = sacred.Scene()
cam = sacred.Camera()
scene_test = [
    '----------------------------------------',
    '_____________________________,----,__  |',
    '|==============================<| /___\\          ____,-------------.____',
    "`------------------.-----.---.___.--'     __.--'-----------------------`--.__",
    '|                   `._   `.            =======================================',
    "|                   ____`.___`._____,----'     `--------,----------------'",
    "|               /_|___________-----<       ========,'",
    "|                               `-.                ,'",
    "|                                   `----.______,--'",
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |this is a test',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '|                                      |',
    '----------------------------------------'
]


class sacred_test(unittest.TestCase):

    def test_bigobj(self):
        with self.assertRaises(sacred.TooLarge):
            scene.obj("testassets/ent_e.json", 2000, 2000)

    def test_stage(self):
        sacred.create_stage(10, 10)
        self.assertEqual(sacred.screen, [
            "          ", "          ", "          ", "          ",
            "          ", "          ", "          ", "          ", "          "
        ])

    def test_add(self):
        self.maxDiff = None
        scene.reset()
        sacred.create_stage(40, 44)

        scene.box(0, 0, 40, 43)
        scene.obj("testassets/ent_e.json", 0, 0)
        scene.txt("this is a test", 40, 30)
        self.assertEqual(sacred.screen, scene_test)
