from abc import abstractmethod

from .our_object import OurObject
from datetime import date
from . import temp

class Item(OurObject):
    def __init__(self, **kwargs):
        temp.deprecation_warning("item","DELETE",date(2024,7,25))
        super().__init__(**kwargs)

    @abstractmethod
    def get_id(self):
        raise NotImplementedError("Subclasses must implement the 'get_id' method.")
