from components.beam import beam
from components.column import Column


class DXFGeneratorInterface:
    def __init__(self, component_type, params):
        self.component_type = component_type
        self.params = params

    def get_component(self):
        if self.component_type == "beam":
            return beam(**self.params)
        elif self.component_type == "column":
            return Column(**self.params)
        else:
            raise ValueError("Invalid component type")
