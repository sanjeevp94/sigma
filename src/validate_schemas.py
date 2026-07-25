import json
import logging
import os
import sys

from jsonschema import validate
from jsonschema.exceptions import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCHEMA_MAP = {
    "workbooks": "schemas/workbook.json",
    "data_models": "schemas/data_model.json",
}


def load_schema(schema_path: str) -> dict:
    with open(schema_path, "r") as f:
        return json.load(f)


def validate_artifacts():
    """
    Validates all JSON files in the artifacts directory against their respective schemas.
    """
    artifact_dirs = {"workbooks": "artifacts/workbooks", "data_models": "artifacts/data_models"}
    has_errors = False

    for artifact_type, dir_path in artifact_dirs.items():
        if not os.path.exists(dir_path):
            continue

        schema_path = SCHEMA_MAP.get(artifact_type)
        if not schema_path or not os.path.exists(schema_path):
            logger.warning(f"No schema found for {artifact_type} at {schema_path}")
            continue

        schema = load_schema(schema_path)

        for filename in os.listdir(dir_path):
            if filename.endswith(".json"):
                file_path = os.path.join(dir_path, filename)
                logger.info(f"Validating {file_path} against {schema_path}")

                try:
                    with open(file_path, "r") as f:
                        payload = json.load(f)
                    validate(instance=payload, schema=schema)
                    logger.info(f"Success: {file_path} is valid.")
                except ValidationError as e:
                    logger.error(f"Validation failed for {file_path}: {e.message}")
                    has_errors = True
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON in {file_path}: {e}")
                    has_errors = True

    if has_errors:
        logger.error("JSON Schema validation failed for one or more artifacts.")
        sys.exit(1)


if __name__ == "__main__":
    validate_artifacts()
