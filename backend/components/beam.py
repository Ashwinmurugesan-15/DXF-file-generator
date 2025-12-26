import ezdxf
from .base_component import BaseComponent

class IBeam(BaseComponent):
    def __init__(self, H, B, tw, tf):
        """
        H  = Total depth of I-beam
        B  = Flange width
        tw = Web thickness
        tf = Flange thickness
        """
        self.H = H
        self.B = B
        self.tw = tw
        self.tf = tf

    def draw(self, msp):

        # Calculations for drawing
        half_B = self.B / 2
        half_tw = self.tw / 2
        half_H = self.H / 2

        # Points of I-beam profile
        points = [
            (-half_B,  half_H), (half_B,  half_H),                # Top flange
            (half_B,  half_H - self.tf),
            (half_tw, half_H - self.tf),
            (half_tw, -half_H + self.tf),
            (half_B,  -half_H + self.tf),
            (half_B,  -half_H),
            (-half_B, -half_H),
            (-half_B, -half_H + self.tf),
            (-half_tw, -half_H + self.tf),
            (-half_tw, half_H - self.tf),
            (-half_B,  half_H - self.tf),
        ]

        msp.add_lwpolyline(points, close=True)
