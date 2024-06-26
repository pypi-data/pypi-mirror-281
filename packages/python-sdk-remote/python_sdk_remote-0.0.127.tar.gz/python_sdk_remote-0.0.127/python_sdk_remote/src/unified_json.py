from .valid_json_versions import valid_json_versions
import warnings


# TODO Shall we merge it with the machine-learning-unified-json?
class UnifiedJson:
    def __init__(self, data: dict, json_version: str):
        warnings.warn("DELETE __init__",DeprecationWarning,stacklevel=2)
        if json_version not in valid_json_versions:
            raise Exception(
                f"version {json_version} is not in valid_json_versions {valid_json_versions}, "
                f"please make sure you run sql2code."
            )
        self.json_version = json_version
        self.data = data

    def get_unified_json(self):
        warnings.warn("DELETE get_unified_json",DeprecationWarning,stacklevel=2)
        return {"version": self.json_version, "data": self.data}

    def get_data(self):
        warnings.warn("DELETE get_data",DeprecationWarning,stacklevel=2)
        return self.data

    def get_json_version(self):
        warnings.warn("DELETE get_json_version",DeprecationWarning,stacklevel=2)
        return self.json_version

    def __str__(self):
        warnings.warn("DELETE __str__",DeprecationWarning,stacklevel=2)
        return self.get_unified_json()

    def __repr__(self):
        warnings.warn("DELETE __repr__",DeprecationWarning,stacklevel=2)
        return self.__str__()
