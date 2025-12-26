import threading
import datetime
import os

class DXFService:
    """
    DXFService.save(component, filename=None, wait=True)
    - component: object implementing generate_dxf(filepath)
    - filename: optional output filename. If None, a timestamped file will be used.
    - wait: if True, the function will wait until generation completes (thread.join()).
            if False, it will return the Thread object immediately so caller can track it.
    """
    @staticmethod
    def save(component, filename=None, wait=True):
        def generate(final_name):
            # ensure directory exists
            folder = os.path.dirname(final_name)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            component.generate_dxf(final_name)
            print(f"DXF generated: {final_name}")

        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output_{timestamp}.dxf"

        thread = threading.Thread(target=generate, args=(filename,), daemon=False)
        thread.start()
        if wait:
            thread.join()
            return None
        return thread
