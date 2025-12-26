from typing import Dict, Any
from interfaces.validator import Validator # Import the Validator class

class UserInputInterface:
    def __init__(self):
        pass

    def get_component_choice(self) -> str:
        while True:
            component = input("Select Component Type (beam/column): ").strip().lower()
            if component in ("beam", "column"):
                return component
            print("Invalid component. Type 'beam' or 'column'.")

    def get_generation_mode(self) -> str:
        while True:
            mode = input("Select Generation Mode (single/batch): ").strip().lower()
            if mode in ("single", "batch"):
                return mode
            print("Invalid mode. Type 'single' or 'batch'.")

    def _get_float_input(self, prompt: str) -> float:
        while True:
            try:
                user_input = input(prompt).strip()
                val = float(user_input)
                if val < 0:
                    print("Error: Value cannot be negative.")
                    continue
                return val
            except ValueError:
                print("Error: Invalid number. Please enter a valid number.")

    def get_params(self, component: str) -> Dict[str, float]:
        params = {}
        if component == "beam":
            print("Enter parameters for I-beam:")
            params["H"] = self._get_float_input("Enter total depth (H): ")
            params["B"] = self._get_float_input("Enter flange width (B): ")
            params["tw"] = self._get_float_input("Enter web thickness (tw): ")
            params["tf"] = self._get_float_input("Enter flange thickness (tf): ")
            # Validate beam parameters using the Validator class
            is_valid, error_msg = Validator.validate_beam(params)
            if not is_valid:
                print(f"Beam parameters are invalid: {error_msg}")
                return self.get_params(component) # Re-prompt for input
        elif component == "column":
            print("Enter parameters for column:")
            params["width"] = self._get_float_input("Enter width: ")
            params["height"] = self._get_float_input("Enter height: ")
            # Validate column parameters using the Validator class
            is_valid, error_msg = Validator.validate_column(params)
            if not is_valid:
                print(f"Column parameters are invalid: {error_msg}")
                return self.get_params(component) # Re-prompt for input
        else:
            raise ValueError("Invalid component selected.")
        return params