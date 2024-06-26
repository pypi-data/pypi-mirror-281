from abc import abstractmethod

from .our_object import OurObject
import warnings
class Item(OurObject):
    def __init__(self, **kwargs):
        warnings.warn("DELETE __init__",DeprecationWarning,stacklevel=2)
        super().__init__(**kwargs)

    @abstractmethod
    def get_id(self):
        warnings.warn("DELETE get_id",DeprecationWarning,stacklevel=2)
        raise NotImplementedError("Subclasses must implement the 'get_id' method.")
