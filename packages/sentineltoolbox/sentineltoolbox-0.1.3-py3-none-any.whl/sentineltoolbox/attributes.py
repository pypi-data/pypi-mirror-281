import logging
from typing import Any, MutableMapping, TypeAlias

from datatree import DataTree
from xarray import Dataset

from sentineltoolbox._utils import string_to_slice
from sentineltoolbox.attributes_hotfix import (
    fix_attribute_value,
    guess_category,
    legacy_aliases,
    valid_aliases,
)
from sentineltoolbox.typedefs import MetadataType_L

__all__ = ["AttributeHandler"]

ContainerWithAttributes: TypeAlias = DataTree[Any] | Dataset | dict[str, Any]

logger = logging.getLogger("sentineltoolbox")


def get_valid_alias(path: str) -> str:

    if path in valid_aliases:
        newpath = valid_aliases[path]
    else:
        newpath = path
    if path != newpath:
        logger.warning(f"{path!r} is deprecated, use {newpath!r} instead")
    return newpath


def get_legacy_alias(part: str) -> str:
    if part in legacy_aliases:
        return legacy_aliases[part]
    else:
        return part


def _extract_category(
    attrs: MutableMapping[str, Any],
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """

    :param attrs:
    :param category:
    :param strict: if True and right place found, consider only this place
    :return:
    """
    strict = kwargs.get("strict", False)
    if category == "properties":
        # search order: stac_discovery/properties -> properties -> root
        if strict:
            places = [attrs.get("stac_discovery", attrs).get("properties", attrs)]
        else:
            places = [attrs.get("stac_discovery", {}).get("properties"), attrs.get("properties"), attrs]
    elif category == "metadata":
        # search order: other_metadata -> root
        if strict:
            places = [attrs.get("other_metadata", attrs)]
        else:
            places = [attrs.get("other_metadata"), attrs]
    elif category == "stac_discovery":
        # search order: stac_discovery -> root
        if strict:
            places = [attrs.get("stac_discovery", attrs)]
        else:
            places = [attrs.get("stac_discovery"), attrs]
    elif category == "root":
        places = [attrs]
    else:
        places = (
            [attrs]
            + _extract_category(attrs, category="stac_discovery")
            + _extract_category(attrs, category="properties")
            + _extract_category(attrs, category="metadata")
        )

    return [place for place in places if place]


def _get_attr_dict(data: ContainerWithAttributes) -> MutableMapping[Any, Any]:
    if isinstance(data, (DataTree, Dataset)):
        return data.attrs
    else:
        return data


def extract_attr(
    data: ContainerWithAttributes,
    path: str | None = None,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> Any:
    attrs = _get_attr_dict(data)
    if category is None and path is not None:
        category = guess_category(path)

    places = _extract_category(attrs, category=category, **kwargs)
    all_properties = {}
    for place in places[::-1]:
        all_properties.update(place)

    if path is None:
        return all_properties
    else:
        path = path.strip().rstrip("/")
        group = all_properties
        parts: list[str] = path.split("/")
        for part in parts:
            try:
                valid_part: int | slice | str = int(part)
            except ValueError:
                try:
                    valid_part = string_to_slice(part)
                except ValueError:
                    valid_part = part

            if isinstance(valid_part, (int, slice)):
                if isinstance(group, list):
                    group = group[valid_part]
                else:
                    raise KeyError(
                        f"Invalid path {path!r}. Part {valid_part!r} is not correct because {group} is not a list",
                    )
            else:
                valid_name = get_valid_alias(valid_part)
                legacy_name = get_legacy_alias(valid_part)
                if valid_name in group:
                    group = group[valid_name]
                elif valid_part in group:
                    group = group[valid_part]
                elif legacy_name in group:
                    group = group[legacy_name]
                else:
                    group = group[valid_part]
        if category:
            return fix_attribute_value(path, group, category=category)
        else:
            return group


def fix_attribute_path(path: str, category: MetadataType_L | None) -> str:

    path = get_valid_alias(path)

    if category is None:
        category = guess_category(path)
    if category is None:
        return path

    recognized_properties = ["stac_discovery/properties/", "properties/"]
    recognized_stac = ["stac_discovery/"]
    recognized_metadata = ["other_metadata/", "metadata/"]
    recognized_prefixes = recognized_properties + recognized_stac + recognized_metadata

    if category == "properties":
        prefix = "stac_discovery/properties/"
    elif category == "stac_discovery":
        prefix = "stac_discovery/"
    elif category == "metadata":
        prefix = "other_metadata/"
    else:
        prefix = ""

    for possible_prefix in recognized_prefixes:
        prefix_parts = possible_prefix.split("/")

        for prefix_part in prefix_parts:
            if prefix_part and path.startswith(prefix_part):
                path = path[len(prefix_part) + 1 :]  # noqa: E203

    return prefix + path


def set_attr(
    data: ContainerWithAttributes,
    path: str,
    value: Any,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> MutableMapping[Any, Any]:
    root_attrs = _get_attr_dict(data)
    path = fix_attribute_path(path, category=category)
    attrs = root_attrs
    parts = path.split("/")
    for part in parts[:-1]:
        attrs = attrs.setdefault(part, {})
    attrs[parts[-1]] = fix_attribute_value(path, value, category=category)
    return root_attrs


class AttributeHandler:

    def __init__(self, container: ContainerWithAttributes, **kwargs: Any):
        """

        :param container:
        :param kwargs:
          - template: template name to use
          - context: template context
        """
        self._container = container

    def set_property(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="properties", **kwargs)

    def set_metadata(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="metadata", **kwargs)

    def set_stac(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="stac_discovery", **kwargs)

    def set_root_attr(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="root", **kwargs)

    def set_attr(self, path: str, value: Any, category: MetadataType_L | None = None, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category=category, **kwargs)

    def get_attr(self, path: str | None = None, category: MetadataType_L | None = None, **kwargs: Any) -> Any:
        if path is None:
            kwargs["strict"] = True
        return extract_attr(self._container, path, category=category, **kwargs)
