import os

BASE_DIR = os.path.dirname(__file__)

RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
ICONS_DIR = os.path.join(RESOURCES_DIR, "icons")
UI_DIR = os.path.join(RESOURCES_DIR, "ui")
TRANSLATIONS_DIR = os.path.join(RESOURCES_DIR, "translations")


#
# Module types
#

class ModuleType:

    BASE = "Módulo bajo"
    WALL = "Módulo alto"
    COLUMN = "Columna"
    WARDROBE = "Armario"
    CUSTOM = "Personalizado"


#
# Part roles
#

class PartRole:

    SIDE = "Side"
    TOP = "Top"
    BOTTOM = "Bottom"
    BACK = "Back"
    SHELF = "Shelf"
    DOOR = "Door"
    FRONT = "Front"
    PANEL = "Panel"
    DIVIDER = "Divider"


#
# Part sources
#

class PartSource:

    MODULE = "Module"
    MANUAL = "Manual"
    LIBRARY = "Library"