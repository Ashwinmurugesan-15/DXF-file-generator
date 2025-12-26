from .base_component import BaseComponent
import ezdxf

class Column(BaseComponent):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, msp):
        # Draw a simple rectangle for the column
        points = [
            (0, 0),
            (self.width, 0),
            (self.width, self.height),
            (0, self.height)
        ]
        msp.add_lwpolyline(points, close=True)