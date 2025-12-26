import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any, Optional
import ezdxf

class DXFService:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def save(self, component: Any, filename: Optional[str] = None) -> str:
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{type(component).__name__}_{timestamp}.dxf"

        doc = ezdxf.new()
        msp = doc.modelspace()
        component.draw(msp) # Assuming component has a draw method
        doc.saveas(filename)
        return filename

    def save_batch(self, components: List[Any], filenames: Optional[List[str]] = None) -> List[str]:
        if filenames is None:
            # Fallback if filenames are not provided (should be provided by main.py now)
            base_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filenames = [f"{type(comp).__name__}_{base_timestamp}_{i+1}.dxf" for i, comp in enumerate(components)]

        generated_files = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_component = {executor.submit(self.save, comp, fname): comp for comp, fname in zip(components, filenames)}
            for future in as_completed(future_to_component):
                try:
                    filename = future.result()
                    generated_files.append(filename)
                except Exception as e:
                    print(f"Error generating DXF: {e}")
                    generated_files.append(None)
        return generated_files