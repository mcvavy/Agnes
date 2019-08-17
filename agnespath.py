import os

# Agnes main directory
APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))


# LIB_PATH = os.path.join(APP_PATH, "./Agnes")
PLUGIN_PATH = os.path.join("../Agnes", "modules")

