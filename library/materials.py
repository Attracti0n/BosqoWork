from library.material import Material



def create_material(
    code,
    name,
    thickness,
    category="Panel",
    supplier="",
    manufacturer="",
    finish="",
    color="",
    price=0.0
):


    material = Material()


    #
    # Identification
    #

    material.Code = code

    material.Name = name

    material.Category = category


    #
    # Technical
    #

    material.Thickness = thickness

    material.Finish = finish

    material.Color = color


    #
    # Commercial
    #

    material.Supplier = supplier

    material.Manufacturer = manufacturer


    #
    # Stock
    #

    material.Price = price


    return material





MATERIALS = {



    #
    # MDF
    #

    "MDF19_WHITE": create_material(

        code="MDF19_WHITE",

        name="MDF Blanco 19 mm",

        thickness=19,

        supplier="",

        manufacturer="",

        finish="Melamina",

        color="Blanco",

        price=0.0

    ),



    "MDF16_WHITE": create_material(

        code="MDF16_WHITE",

        name="MDF Blanco 16 mm",

        thickness=16,

        finish="Melamina",

        color="Blanco"

    ),



    "MDF10_WHITE": create_material(

        code="MDF10_WHITE",

        name="MDF Blanco 10 mm",

        thickness=10,

        finish="Melamina",

        color="Blanco"

    ),



    #
    # Traseras
    #

    "BACK_10_WHITE": create_material(

        code="BACK_10_WHITE",

        name="Trasera blanca 10 mm",

        thickness=10,

        finish="Melamina",

        color="Blanco"

    ),



    #
    # Contrachapado
    #

    "PLY18": create_material(

        code="PLY18",

        name="Contrachapado 18 mm",

        thickness=18,

        category="Panel",

        finish="Natural"

    ),



    #
    # Compacto
    #

    "COMPACT12_WHITE": create_material(

        code="COMPACT12_WHITE",

        name="Compacto blanco 12 mm",

        thickness=12,

        finish="Compacto",

        color="Blanco"

    )


}





def get_materials():

    return MATERIALS