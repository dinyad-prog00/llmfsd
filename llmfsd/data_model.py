from typing import Dict, Union, List, Optional


class DataModel:
    def __init__(
        self, name: str, schema: Union[Dict[str, Optional[str]], List[str]]
    ) -> None:
        self.name = name
        self.schema = schema

    def get_description(self) -> Dict[str, str]:
        """
        Returns a dictionary of attributes with their descriptions.
        - If the schema is a list, returns an empty dictionary.
        - If the schema is a dictionary, only includes attributes with non-None descriptions.
        """
        if isinstance(self.schema, dict):
            return {
                key: value for key, value in self.schema.items() if value is not None
            }
        elif isinstance(self.schema, list):
            return {}
        else:
            raise ValueError("Invalid schema format")

    def get_attributes(self) -> List[str]:
        """
        Returns a list of all attributes.
        - For a dictionary schema, returns all keys.
        - For a list schema, returns all items in the list.
        """
        if isinstance(self.schema, dict):
            return list(self.schema.keys())
        elif isinstance(self.schema, list):
            return self.schema
        else:
            raise ValueError("Invalid schema format")
