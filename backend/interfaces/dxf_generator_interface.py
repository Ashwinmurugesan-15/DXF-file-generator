from ..components.beam import IBeam
from ..components.column import Column

class DXFGeneratorInterface:
    def __init__(self, component_type: str, params: dict):
        self.component_type = component_type
        self.params = params

    def get_component(self):
        if self.component_type == "beam":
            return IBeam(self.params['H'], self.params['B'], self.params['tw'], self.params['tf'])
        elif self.component_type == "column":
            return Column(self.params['width'], self.params['height'])
        else:
            raise ValueError("Unsupported component type")