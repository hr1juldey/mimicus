"""OpenAPI JSON schema to example data converter."""

from typing import Dict, Any


class SchemaToExampleConverter:
    """Convert JSON schema to example data."""

    @staticmethod
    def convert(schema: Dict[str, Any]) -> Any:
        """Convert JSON schema to example data.

        Args:
            schema: JSON schema object

        Returns:
            Example data matching schema
        """
        type_ = schema.get("type", "object")

        if type_ == "object":
            props = schema.get("properties", {})
            return {k: SchemaToExampleConverter.convert(v) for k, v in props.items()}

        elif type_ == "array":
            items = schema.get("items", {})
            return [SchemaToExampleConverter.convert(items)]

        elif type_ == "string":
            return "string"

        elif type_ == "number":
            return 0

        elif type_ == "integer":
            return 0

        elif type_ == "boolean":
            return True

        return None
