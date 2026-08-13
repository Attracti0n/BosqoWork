import FreeCADGui

from gui.workbench import BosqoWorkbench
import commands.cut_list
import commands.cutlist_report_command
import commands.bom
import commands.materials
import commands.parts_table
import commands.parametric_module
import commands.module_placement

FreeCADGui.addWorkbench(BosqoWorkbench())