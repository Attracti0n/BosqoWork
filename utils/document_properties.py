import FreeCAD


PROJECT_PROPERTIES = {
    "ProjectName": "App::PropertyString",
    "ProjectNumber": "App::PropertyString",
    "Customer": "App::PropertyString",
    "Phone": "App::PropertyString",
    "Email": "App::PropertyString",
    "SiteAddress": "App::PropertyString",
    "InstallationAddress": "App::PropertyString",
    "Notes": "App::PropertyString",
}


def initialize_project_properties(doc):
    """
    Create Bosqo project properties if they do not exist.
    """

    for name, property_type in PROJECT_PROPERTIES.items():

        if hasattr(doc, name):
            continue

        doc.addProperty(
            property_type,
            name,
            "Bosqo",
            ""
        )


def has_project_properties(doc):
    """
    Returns True if the document has Bosqo properties.
    """

    return hasattr(doc, "ProjectName")


def get_project_property(doc, name):
    """
    Returns the value of a project property.
    """

    if hasattr(doc, name):
        return getattr(doc, name)

    return None


def set_project_property(doc, name, value):
    """
    Sets the value of a project property.
    """

    if hasattr(doc, name):
        setattr(doc, name, value)

def load_project_properties(doc):

    data = {}

    for name in PROJECT_PROPERTIES:

        if hasattr(doc, name):
            data[name] = getattr(doc, name)
        else:
            data[name] = ""

    return data

def save_project_properties(doc, data):

    initialize_project_properties(doc)

    for name, value in data.items():

        if hasattr(doc, name):
            setattr(doc, name, value)

    doc.recompute()
