import FreeCADGui

from gui.workbench import BosqoWorkbench
import commands.add_module
import commands.analyze_geometry
import commands.import_parts
import commands.analyze_orientation
import commands.analyze_planes
import commands.analyze_panel
import commands.cut_list

FreeCADGui.addWorkbench(BosqoWorkbench())