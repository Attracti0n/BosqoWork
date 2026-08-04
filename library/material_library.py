import FreeCAD
import os
import json


class MaterialLibrary:

    #
    # Persistent library
    #

    LIBRARY_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    MATERIALS_FILE = os.path.join(
        LIBRARY_DIR,
        "materials.json"
    )


    #
    # Cache
    #

    _materials = None


    #
    # Load persistent library
    #

    @classmethod
    def _load(
        cls
    ):

        if cls._materials is not None:

            return cls._materials


        if not os.path.exists(
            cls.MATERIALS_FILE
        ):

            cls._materials = []

            cls._save()

            return cls._materials


        try:

            with open(
                cls.MATERIALS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(
                    file
                )

        except Exception as error:

            print(
                "MaterialLibrary load error:",
                error
            )

            cls._materials = []

            return cls._materials


        if not isinstance(
            data,
            list
        ):

            data = []


        cls._materials = data

        return cls._materials


    #
    # Save persistent library
    #

    @classmethod
    def _save(
        cls
    ):

        if cls._materials is None:

            cls._materials = []


        try:

            with open(
                cls.MATERIALS_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    cls._materials,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except Exception as error:

            print(
                "MaterialLibrary save error:",
                error
            )

            return False


    #
    # Reload
    #

    @classmethod
    def reload(
        cls
    ):

        cls._materials = None

        return cls._load()


    #
    # Persistent materials
    #

    @classmethod
    def all(
        cls,
        document=None
    ):

        #
        # If document is supplied,
        # return BosqoMaterial objects
        #

        if document is not None:

            return cls._documentMaterials(
                document
            )


        #
        # Without document return
        # persistent material data
        #

        return cls._load()


    #
    # Materials inside document
    #

    @classmethod
    def _documentMaterials(
        cls,
        document
    ):

        if document is None:

            return []


        materials = []


        for obj in document.Objects:

            if not hasattr(
                obj,
                "Proxy"
            ):

                continue


            proxy = obj.Proxy


            if proxy is None:

                continue


            if type(proxy).__name__ != "BosqoMaterial":

                continue


            materials.append(
                obj
            )


        return materials


    #
    # Material codes
    #

    @classmethod
    def codes(
        cls,
        document=None
    ):

        #
        # Codes come from the persistent
        # library, not only the document.
        #

        materials = cls._load()

        codes = []


        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                continue


            if code not in codes:

                codes.append(
                    code
                )


        return codes


    #
    # Get material
    #

    @classmethod
    def get(
        cls,
        code,
        document=None
    ):

        if not code:

            return None


        code = str(
            code
        ).strip()


        #
        # First look inside document
        #

        if document is None:

            document = FreeCAD.ActiveDocument


        if document is not None:

            for material in cls._documentMaterials(
                document
            ):

                if not hasattr(
                    material,
                    "Code"
                ):

                    continue


                if material.Code == code:

                    return material


        #
        # Then persistent library
        #

        for data in cls._load():

            if not isinstance(
                data,
                dict
            ):

                continue


            stored_code = str(
                data.get(
                    "Code",
                    ""
                )
            ).strip()


            if stored_code != code:

                continue


            #
            # Material is in library
            # but not in document.
            #

            if document is None:

                return data


            #
            # Create material inside document
            #

            return cls._createDocumentMaterial(
                document,
                data
            )


        return None


    #
    # Get material by name
    #

    @classmethod
    def getByName(
        cls,
        name,
        document=None
    ):

        if not name:

            return None


        name = str(
            name
        ).strip()


        #
        # Document first
        #

        if document is None:

            document = FreeCAD.ActiveDocument


        if document is not None:

            for material in cls._documentMaterials(
                document
            ):

                if not hasattr(
                    material,
                    "MaterialName"
                ):

                    continue


                if material.MaterialName == name:

                    return material


        #
        # Persistent library
        #

        for data in cls._load():

            if not isinstance(
                data,
                dict
            ):

                continue


            material_name = str(
                data.get(
                    "MaterialName",
                    ""
                )
            ).strip()


            if material_name == name:

                if document is None:

                    return data


                return cls._createDocumentMaterial(
                    document,
                    data
                )


        return None


    #
    # Check existence
    #

    @classmethod
    def exists(
        cls,
        code,
        document=None
    ):

        if not code:

            return False


        code = str(
            code
        ).strip()


        for data in cls._load():

            if not isinstance(
                data,
                dict
            ):

                continue


            stored_code = str(
                data.get(
                    "Code",
                    ""
                )
            ).strip()


            if stored_code == code:

                return True


        return False


    #
    # Add material
    #

    @classmethod
    def add(
        cls,
        material,
        document=None
    ):

        if material is None:

            return False


        #
        # If a FreeCAD BosqoMaterial object
        # was supplied, convert it to data.
        #

        if hasattr(
            material,
            "Proxy"
        ):

            if not hasattr(
                material,
                "Code"
            ):

                return False


            data = {

                "Code":
                    getattr(
                        material,
                        "Code",
                        ""
                    ),

                "MaterialName":
                    getattr(
                        material,
                        "MaterialName",
                        ""
                    ),

                "MaterialType":
                    getattr(
                        material,
                        "MaterialType",
                        ""
                    ),

                "Category":
                    getattr(
                        material,
                        "Category",
                        ""
                    ),

                "Thickness":
                    float(
                        getattr(
                            material,
                            "Thickness",
                            0
                        )
                    ),

                "SheetLength":
                    float(
                        getattr(
                            material,
                            "SheetLength",
                            0
                        )
                    ),

                "SheetWidth":
                    float(
                        getattr(
                            material,
                            "SheetWidth",
                            0
                        )
                    ),

                "Supplier":
                    getattr(
                        material,
                        "Supplier",
                        ""
                    ),

                "Finish":
                    getattr(
                        material,
                        "Finish",
                        ""
                    ),

                "GrainDirection":
                    getattr(
                        material,
                        "GrainDirection",
                        ""
                    ),

                "Price":
                    float(
                        getattr(
                            material,
                            "Price",
                            0
                        )
                    ),

                "Currency":
                    getattr(
                        material,
                        "Currency",
                        "EUR"
                    )
            }


        elif isinstance(
            material,
            dict
        ):

            data = dict(
                material
            )


        else:

            return False


        #
        # Code
        #

        code = str(
            data.get(
                "Code",
                ""
            )
        ).strip()


        if not code:

            return False


        #
        # Do not create duplicates
        #

        if cls.exists(
            code
        ):

            return False


        #
        # Store
        #

        cls._load().append(
            data
        )


        if not cls._save():

            return False


        #
        # Refresh parts
        #

        if document is None:

            document = FreeCAD.ActiveDocument


        if document is not None:

            cls.refreshParts(
                document
            )


        return True


    #
    # Update material
    #

    @classmethod
    def update(
        cls,
        material
    ):

        if material is None:

            return False


        if hasattr(
            material,
            "Proxy"
        ):

            data = {

                "Code":
                    getattr(
                        material,
                        "Code",
                        ""
                    ),

                "MaterialName":
                    getattr(
                        material,
                        "MaterialName",
                        ""
                    ),

                "MaterialType":
                    getattr(
                        material,
                        "MaterialType",
                        ""
                    ),

                "Category":
                    getattr(
                        material,
                        "Category",
                        ""
                    ),

                "Thickness":
                    float(
                        getattr(
                            material,
                            "Thickness",
                            0
                        )
                    ),

                "SheetLength":
                    float(
                        getattr(
                            material,
                            "SheetLength",
                            0
                        )
                    ),

                "SheetWidth":
                    float(
                        getattr(
                            material,
                            "SheetWidth",
                            0
                        )
                    ),

                "Supplier":
                    getattr(
                        material,
                        "Supplier",
                        ""
                    ),

                "Finish":
                    getattr(
                        material,
                        "Finish",
                        ""
                    ),

                "GrainDirection":
                    getattr(
                        material,
                        "GrainDirection",
                        ""
                    ),

                "Price":
                    float(
                        getattr(
                            material,
                            "Price",
                            0
                        )
                    ),

                "Currency":
                    getattr(
                        material,
                        "Currency",
                        "EUR"
                    )
            }


        elif isinstance(
            material,
            dict
        ):

            data = dict(
                material
            )


        else:

            return False


        #
        # Code
        #

        code = str(
            data.get(
                "Code",
                ""
            )
        ).strip()


        if not code:

            return False


        materials = cls._load()


        for index, existing in enumerate(
            materials
        ):

            if not isinstance(
                existing,
                dict
            ):

                continue


            existing_code = str(
                existing.get(
                    "Code",
                    ""
                )
            ).strip()


            if existing_code == code:

                materials[index] = data

                return cls._save()


        #
        # Not found
        #

        materials.append(
            data
        )

        return cls._save()


    #
    # Remove material
    #

    @classmethod
    def remove(
        cls,
        code,
        document=None
    ):

        if not code:

            return False


        code = str(
            code
        ).strip()


        materials = cls._load()

        found = False

        remaining = []


        for material in materials:

            if not isinstance(
                material,
                dict
            ):

                continue


            material_code = str(
                material.get(
                    "Code",
                    ""
                )
            ).strip()


            if material_code == code:

                found = True

                continue


            remaining.append(
                material
            )


        if not found:

            return False


        cls._materials = remaining

        cls._save()


        #
        # Remove from document too
        #

        if document is None:

            document = FreeCAD.ActiveDocument


        if document is not None:

            for material in list(
                cls._documentMaterials(
                    document
                )
            ):

                if hasattr(
                    material,
                    "Code"
                ):

                    if material.Code == code:

                        document.removeObject(
                            material.Name
                        )


        #
        # Refresh parts
        #

        if document is not None:

            cls.refreshParts(
                document
            )


        return True


    #
    # Create material inside document
    #

    @classmethod
    def _createDocumentMaterial(
        cls,
        document,
        data
    ):

        if document is None:

            return None


        #
        # Check if already exists
        #

        code = str(
            data.get(
                "Code",
                ""
            )
        ).strip()


        for material in cls._documentMaterials(
            document
        ):

            if hasattr(
                material,
                "Code"
            ):

                if material.Code == code:

                    return material


        #
        # Import here to avoid
        # circular imports.
        #

        from objects.bosqo_material import BosqoMaterial


        material = document.addObject(
            "App::FeaturePython",
            "BosqoMaterial"
        )


        BosqoMaterial(
            material
        )


        #
        # Apply data
        #

        if hasattr(
            material,
            "Proxy"
        ):

            material.Proxy.setData(
                material,
                data
            )


        #
        # Label
        #

        if hasattr(
            material,
            "MaterialName"
        ):

            if material.MaterialName:

                material.Label = material.MaterialName


        return material


    #
    # Synchronize persistent library
    # with document
    #

    @classmethod
    def sync(
        cls,
        document=None
    ):

        if document is None:

            document = FreeCAD.ActiveDocument


        if document is None:

            return


        for data in cls._load():

            if not isinstance(
                data,
                dict
            ):

                continue


            code = str(
                data.get(
                    "Code",
                    ""
                )
            ).strip()


            if not code:

                continue


            #
            # Only create if missing
            #

            existing = cls.get(
                code,
                document
            )


            if existing is None:

                cls._createDocumentMaterial(
                    document,
                    data
                )


    #
    # Refresh material lists
    # in BosqoPart objects
    #

    @classmethod
    def refreshParts(
        cls,
        document=None
    ):

        if document is None:

            document = FreeCAD.ActiveDocument


        if document is None:

            return


        for obj in document.Objects:

            if not hasattr(
                obj,
                "Proxy"
            ):

                continue


            proxy = obj.Proxy


            if proxy is None:

                continue


            if type(proxy).__name__ != "BosqoPart":

                continue


            if not hasattr(
                proxy,
                "refreshMaterialList"
            ):

                continue


            try:

                proxy.refreshMaterialList(
                    obj
                )

            except Exception as error:

                print(
                    "MaterialLibrary refresh error:",
                    error
                )