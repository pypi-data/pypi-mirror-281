import json
from abc import ABC, abstractmethod

from .mini_logger import MiniLogger as logger
import warnings


# TODO Where are we using it? Shall we extend the usage of OurObject as the father of all our entities?
class OurObject(ABC):
    def __init__(self, **kwargs):
        warnings.warn("DELETE __init__",DeprecationWarning,stacklevel=2)
        INIT_METHOD_NAME = '__init__'
        logger.start(INIT_METHOD_NAME, object={'kwargs': kwargs})
        self.kwargs = kwargs
        logger.end(INIT_METHOD_NAME, object={'kwargs': kwargs})

    @abstractmethod
    def get_name(self):
        warnings.warn("DELETE get_name",DeprecationWarning,stacklevel=2)
        """Returns the name of the object"""
        raise NotImplementedError(
            "Subclasses must implement the 'get_name' method.")

    def get(self, attr_name: str):
        warnings.warn("DELETE get",DeprecationWarning,stacklevel=2)
        """Returns the value of the attribute with the given name"""
        GET_METHOD_NAME = 'get'
        logger.start(GET_METHOD_NAME, object={'attr_name': attr_name})
        arguments = getattr(self, 'kwargs', None)
        value = arguments.get(attr_name, None)
        logger.end(GET_METHOD_NAME, object={'attr_name': attr_name})
        return value

    def get_all_arguments(self):
        warnings.warn("DELETE get_all_arguments",DeprecationWarning,stacklevel=2)
        """Returns all the arguments passed to the constructor as a dictionary"""
        return getattr(self, 'kwargs', None)

    def to_json(self) -> str:
        warnings.warn("DELETE to_json",DeprecationWarning,stacklevel=2)
        """Returns a json string representation of this object"""
        return json.dumps(self.__dict__)

    def from_json(self, json_string: str) -> 'OurObject':
        warnings.warn("DELETE from_json",DeprecationWarning,stacklevel=2)
        """Returns an instance of the class from a json string"""
        FROM_JSON_METHOD_NAME = 'from_json'
        logger.start(FROM_JSON_METHOD_NAME,
                     object={'json_string': json_string})
        self.__dict__ = json.loads(json_string)
        logger.end(FROM_JSON_METHOD_NAME,
                   object={'json_dict': self.__dict__})
        return self

    def __eq__(self, other) -> bool:
        warnings.warn("DELETE __eq__",DeprecationWarning,stacklevel=2)
        """Checks if two objects are equal"""
        if not isinstance(other, OurObject):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        warnings.warn("DELETE __ne__",DeprecationWarning,stacklevel=2)
        """Checks if two objects are not equal"""
        return not self.__eq__(other)
