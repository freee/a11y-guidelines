"""
YAML validation module for accessibility guidelines.

This module provides validation functionality for YAML files using JSON Schema.
"""

import json
import os
import sys
from typing import Dict, Any, Literal
from jsonschema import Draft202012Validator, RefResolver


class ValidationError(Exception):
    """YAML validation specific error"""
    pass


ValidationMode = Literal["strict", "warning", "disabled"]


class YamlValidator:
    """Validator for YAML files using JSON Schema definitions"""

    def __init__(self, schema_dir: str, validation_mode: ValidationMode = "strict"):
        """
        Initialize the validator with schema directory.

        Args:
            schema_dir: Directory containing JSON schema files
            validation_mode: Validation mode ("strict", "warning", or "disabled")
        """
        self.schema_dir = schema_dir
        self.validation_mode = validation_mode
        self.schemas: Dict[str, Dict[str, Any]] = {}
        self.resolvers: Dict[str, RefResolver] = {}
        self._load_schemas()

    def _load_schemas(self):
        """Load all schema files and create resolvers"""
        schema_files = ['check.json', 'guideline.json', 'faq.json', 'common.json']

        for schema_file in schema_files:
            schema_path = os.path.join(self.schema_dir, schema_file)
            try:
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                    schema_name = schema_file.replace('.json', '')
                    self.schemas[schema_name] = schema

                    # Create resolver for $ref resolution
                    base_uri = f"file://{os.path.abspath(self.schema_dir)}/"
                    self.resolvers[schema_name] = RefResolver(base_uri, schema)
            except FileNotFoundError:
                print(f"Warning: Schema file {schema_path} not found", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in schema file {schema_path}: {e}", file=sys.stderr)
                sys.exit(1)

    def validate_yaml_data(self, data: Dict[str, Any], schema_name: str, file_path: str):
        """
        Validate YAML data against specified schema.

        Args:
            data: Parsed YAML data to validate
            schema_name: Name of the schema to validate against
            file_path: Path to the YAML file being validated (for error reporting)

        Raises:
            ValidationError: If validation fails
        """
        if schema_name not in self.schemas:
            raise ValidationError(f"Schema '{schema_name}' not found")

        schema = self.schemas[schema_name]
        resolver = self.resolvers[schema_name]

        # Create validator with resolver for $ref support
        validator = Draft202012Validator(schema, resolver=resolver)

        errors = list(validator.iter_errors(data))
        if errors:
            error_messages = []
            for error in errors:
                path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
                error_messages.append(f"  - Path: {path}\n    Error: {error.message}")

            raise ValidationError(
                f"Validation failed for file: {file_path}\n"
                f"Schema: {schema_name}\n"
                f"Errors:\n" + "\n".join(error_messages)
            )

    def validate_with_mode(self, data: Dict[str, Any], schema_name: str, file_path: str) -> bool:
        """
        Validate YAML data with respect to the configured validation mode.

        Args:
            data: Parsed YAML data to validate
            schema_name: Name of the schema to validate against
            file_path: Path to the YAML file being validated (for error reporting)

        Returns:
            True if validation passed or was skipped, False if validation failed in warning mode

        Raises:
            ValidationError: If validation fails in strict mode
        """
        if self.validation_mode == "disabled":
            return True

        try:
            self.validate_yaml_data(data, schema_name, file_path)
            return True
        except ValidationError as e:
            if self.validation_mode == "strict":
                # Re-raise the error to maintain strict behavior
                raise
            elif self.validation_mode == "warning":
                # Log warning and continue processing
                print(f"YAML Validation Warning: {e}", file=sys.stderr)
                return False

        return True

    def get_available_schemas(self):
        """
        Get list of available schema names.

        Returns:
            List of schema names
        """
        return list(self.schemas.keys())
