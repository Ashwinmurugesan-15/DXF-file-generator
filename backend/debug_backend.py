import sys
import os
import uuid
import tempfile
import traceback

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.interfaces.dxf_generator_interface import DXFGeneratorInterface
from backend.services.dxf_service import DXFService

def test_generation():
    print("Testing Beam Generation...")
    params = {'H': 200.0, 'B': 100.0, 'tw': 10.0, 'tf': 12.0}
    component_type = "beam"
    
    try:
        # Simulate main.py logic
        generated_filename = f"{uuid.uuid4()}.dxf"
        tmp_path = os.path.join(tempfile.gettempdir(), generated_filename)
        print(f"Target file: {tmp_path}")

        # 1. Generator Interface
        print("Initializing Generator...")
        generator = DXFGeneratorInterface(component_type, params)
        component = generator.get_component()
        print(f"Component created: {component}")

        # 2. Service Save
        print("Saving DXF...")
        dxf_service = DXFService()
        saved_file = dxf_service.save(component, filename=tmp_path)
        print(f"Success! File saved at: {saved_file}")

        # Cleanup
        if os.path.exists(saved_file):
            os.remove(saved_file)
            print("Cleanup successful.")

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    test_generation()
