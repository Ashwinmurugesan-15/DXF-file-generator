import re
from typing import Dict, Any

class Validator:
    validation_rules = {
        'beam': {
            'H': {'min': 1, 'max': 100000, 'description': 'Total depth (H)'},
            'B': {'min': 1, 'max': 100000, 'description': 'Flange width (B)'},
            'tw': {'min': 1, 'max': 100000, 'description': 'Web thickness (tw)'},
            'tf': {'min': 1, 'max': 100000, 'description': 'Flange thickness (tf)'}
        },
        'column': {
            'width': {'min': 1, 'max': 100000, 'description': 'Width'},
            'height': {'min': 1, 'max': 100000, 'description': 'Height'}
        }
    }

    @staticmethod
    def _validate_float(value: Any, rule: Dict[str, Any]) -> bool:
        if not isinstance(value, (int, float)):
            return False, f"Error: {rule['description']} must be a number."
        if not (rule['min'] <= value <= rule['max']):
            return False, f"Error: {rule['description']} must be between {rule['min']} and {rule['max']} mm."
        return True, ""

    @staticmethod
    def validate_beam(params: Dict[str, float]) -> tuple[bool, str]:
        print("Validating beam parameters...")
        for key, rule in Validator.validation_rules['beam'].items():
            is_valid, error_msg = Validator._validate_float(params.get(key), rule)
            if not is_valid:
                return False, error_msg

        # Add beam proportion validation
        H = params.get("H")
        B = params.get("B")
        if B is not None and B > 0 and H is not None and H / B > 10:
            print("Warning: H/B ratio exceeds 10, which is unusual for standard I-beams. Consider revising dimensions.")
        return True, ""

    @staticmethod
    def validate_column(params: Dict[str, float]) -> tuple[bool, str]:
        print("Validating column parameters...")
        for key, rule in Validator.validation_rules['column'].items():
            is_valid, error_msg = Validator._validate_float(params.get(key), rule)
            if not is_valid:
                return False, error_msg
        return True, ""