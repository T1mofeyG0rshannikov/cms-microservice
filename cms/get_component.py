from .models import Component

def get_component(base_component: Component):
    component = None
    if base_component.excomponent.first() is not None:
        component = base_component.excomponent.first()

    elif base_component.navcomponent.first() is not None:
        component = base_component.navcomponent.first()

    if component is not None:
        component.template = "cms/" + component.template

    return component