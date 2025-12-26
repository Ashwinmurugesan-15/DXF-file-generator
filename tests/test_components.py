import unittest
import ezdxf
import sys
import os
from unittest.mock import patch
import io

# Add the project root to the sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.components.beam import IBeam
from backend.components.column import Column

class TestComponents(unittest.TestCase):
    def setUp(self):
        self.doc = ezdxf.new()
        self.msp = self.doc.modelspace()

    def test_ibeam_draw(self):
        # Create an I-beam: H=200, B=100, tw=10, tf=15
        beam = IBeam(H=200, B=100, tw=10, tf=15)
        with patch('sys.stdout', new=io.StringIO()):
            beam.draw(self.msp)
        
        # Check if something was added to modelspace
        entities = list(self.msp)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].dxftype(), 'LWPOLYLINE')
        
        # Check number of points (I-beam profile should have 12 points)
        self.assertEqual(len(entities[0]), 12)

    def test_column_draw(self):
        # Create a column: width=100, height=200
        column = Column(width=100, height=200)
        with patch('sys.stdout', new=io.StringIO()):
            column.draw(self.msp)
        
        # Check if something was added to modelspace
        entities = list(self.msp)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].dxftype(), 'LWPOLYLINE')
        
        # Check number of points (Rectangle should have 4 points)
        self.assertEqual(len(entities[0]), 4)

if __name__ == '__main__':
    unittest.main()
