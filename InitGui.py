import FreeCADGui

from gui.workbench import BosqoWorkbench
import commands.add_module
import commands.analyze_geometry
import commands.import_parts
import commands.analyze_orientation
import commands.analyze_planes
import commands.analyze_panel
import commands.cut_list
import commands.cutlist_report_command
import commands.create_module_from_selection
import commands.bom
import commands.materials
import commands.parts_table
import commands.parametric_module
import commands.module_placement

FreeCADGui.addWorkbench(BosqoWorkbench())