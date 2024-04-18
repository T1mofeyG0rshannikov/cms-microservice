# from .models import ComponentsName


def get_component(components_name):
    component = None
    if components_name.navbar_set.first() is not None:
        component = components_name.navbar_set.first()

    if components_name.examplecomponent_set.first() is not None:
        component = components_name.examplecomponent_set.first()

    return component
