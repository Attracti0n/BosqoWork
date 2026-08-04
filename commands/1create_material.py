import FreeCAD
import FreeCADGui
import os

from app_paths import ICONS_DIR

from objects.bosqo_material import create_material
from dialogs.material_dialog import MaterialDialog
from library.material_library import MaterialLibrary


class CreateMaterialCommand:

    def GetResources(
        self
    ):

        return {

            "MenuText":
                "Nuevo material",

            "ToolTip":
                "Crear un nuevo material Bosqo",

            "Pixmap":
                os.path.join(
                    ICONS_DIR,
                    "material.svg"
                )

        }


    def Activated(
        self
    ):

        doc = FreeCAD.ActiveDocument


        #
        # No active document
        #

        if doc is None:

            FreeCAD.Console.PrintWarning(
                "No hay documento activo.\n"
            )

            return


        #
        # Create material object
        #

        material = create_material(
            doc
        )


        material.Label = "Nuevo material"


        #
        # Open dialog
        #

        dialog = MaterialDialog()


        result = dialog.exec()


        #
        # Cancel
        #

        if not result:

            doc.removeObject(
                material.Name
            )

            doc.recompute()

            return


        #
        # Get data
        #

        data = dialog.getData()


        #
        # Basic validation
        #

        code = str(
            data.get(
                "Code",
                ""
            )
        ).strip()


        name = str(
            data.get(
                "MaterialName",
                ""
            )
        ).strip()


        if not code:

            FreeCAD.Console.PrintWarning(
                "El material debe tener un código.\n"
            )

            doc.removeObject(
                material.Name
            )

            doc.recompute()

            return


        if not name:

            FreeCAD.Console.PrintWarning(
                "El material debe tener un nombre.\n"
            )

            doc.removeObject(
                material.Name
            )

            doc.recompute()

            return


        #
        # Check duplicate in persistent library
        #

        if MaterialLibrary.exists(
            code
        ):

            FreeCAD.Console.PrintWarning(
                "Ya existe un material en la biblioteca "
                "con el código: "
                + code
                + "\n"
            )

            doc.removeObject(
                material.Name
            )

            doc.recompute()

            return


        #
        # Check duplicate inside current document
        #

        duplicate = False


        for obj in doc.Objects:

            if obj == material:

                continue


            if not hasattr(
                obj,
                "Code"
            ):

                continue


            existing_code = str(
                obj.Code
            ).strip()


            if existing_code == code:

                duplicate = True

                break


        if duplicate:

            FreeCAD.Console.PrintWarning(
                "Ya existe un material en el documento "
                "con el código: "
                + code
                + "\n"
            )

            doc.removeObject(
                material.Name
            )

            doc.recompute()

            return


        #
        # Apply material data
        #

        material.Proxy.setData(
            material,
            data
        )


        #
        # Use material name as tree label
        #

        material.Label = name


        #
        # Recompute document
        #

        doc.recompute()


        #
        # Save material to persistent library
        #

        saved = MaterialLibrary.add(
            material,
            doc
        )


        if not saved:

            FreeCAD.Console.PrintWarning(
                "No se pudo guardar el material "
                "en la biblioteca.\n"
            )

            doc.removeObject(
                material.Name
            )

            doc.recompute()

            return


        #
        # Refresh material lists in existing parts
        #

        MaterialLibrary.refreshParts(
            doc
        )


        #
        # Recompute after refreshing lists
        #

        doc.recompute()


        #
        # Get available material codes
        #

        material_codes = MaterialLibrary.codes()


        #
        # Message
        #

        FreeCAD.Console.PrintMessage(
            "Material creado correctamente: "
            + code
            + " - "
            + name
            + "\n"
        )


        FreeCAD.Console.PrintMessage(
            "Materiales disponibles: "
            + str(
                material_codes
            )
            + "\n"
        )


    def IsActive(
        self
    ):

        return (
            FreeCAD.ActiveDocument
            is not None
        )


FreeCADGui.addCommand(
    "Bosqo_CreateMaterial",
    CreateMaterialCommand()
)