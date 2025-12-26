class BaseComponent:
    def __init__(self):
        pass

    def draw(self, msp):
        """
        This method should be implemented by subclasses to draw the component
        onto the given modelspace (msp) object from ezdxf.
        """
        raise NotImplementedError("Subclasses must implement the 'draw' method")