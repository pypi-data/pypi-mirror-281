import logging
from typing import Any

from sentineltoolbox.attributes_utils import path_relative_to_category
from sentineltoolbox.typedefs import MetadataType_L

logger = logging.getLogger("sentineltoolbox")

valid_aliases: dict[str, str] = {"eo:bands": "bands", "eopf:type": "product:type", "eopf:timeline": "product:timeline"}
short_names_stac_properties: dict[str, str] = {"bands": "bands", "platform": "platform"}
short_names_stac: dict[str, str] = {}
short_names_metadata: dict[str, str] = {}

legacy_aliases = {v: k for k, v in valid_aliases.items()}
attribute_short_names: dict[str, tuple[MetadataType_L, str]] = {}

for key, path in short_names_stac_properties.items():
    attribute_short_names[key] = ("properties", path)
for key, path in short_names_stac.items():
    attribute_short_names[key] = ("stac_discovery", path)
for key, path in short_names_metadata.items():
    attribute_short_names[key] = ("metadata", path)


for legacy, valid in valid_aliases.items():
    if valid in attribute_short_names:
        attribute_short_names[legacy] = attribute_short_names[valid]


def fix_attribute_value(path: str, value: Any, category: MetadataType_L | None) -> Any:

    if category is None:
        category = guess_category(path)
    if category is None:
        return value
    else:
        new_value = value
        relpath = path_relative_to_category(path, category)

        # Fix properties
        if category == "properties":

            if relpath == "platform":
                if isinstance(value, str):
                    new_value = value.lower()

        if value != new_value:
            logger.warning(f"{path}: value {value!r} has been fixed to {new_value!r}")
        return new_value


def guess_category(path: str, **kwargs: Any) -> MetadataType_L | None:
    if path.startswith("properties") or path.startswith("stac_discovery/properties"):
        return "properties"
    elif path.startswith("stac_discovery"):
        return "stac_discovery"
    elif path.startswith("other_metadata") or path.startswith("metadata"):
        return "metadata"
    elif path in attribute_short_names:
        # search in prop lookuptable / short names
        return attribute_short_names[path][0]
    else:
        # else: no category in path, not find in lookup table => None
        return None
