from sentineltoolbox.typedefs import MetadataType_L, category_paths


def path_relative_to_category(path: str, category: MetadataType_L | None) -> str:
    if category in ("properties", "stac_discovery", "metadata"):
        return path.replace(category_paths[category], "")
    else:
        return path
