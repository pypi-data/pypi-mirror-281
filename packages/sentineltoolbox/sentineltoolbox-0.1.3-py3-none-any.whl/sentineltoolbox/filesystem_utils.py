from pathlib import Path, PurePosixPath
from typing import Any

import fsspec

from sentineltoolbox._utils import _credential_required, fix_url, split_protocol
from sentineltoolbox.configuration import get_config
from sentineltoolbox.models.credentials import S3BucketCredentials
from sentineltoolbox.readers._utils import is_eopf_adf
from sentineltoolbox.typedefs import Credentials, PathOrPattern


def get_fsspec_filesystem(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> tuple[Any, PurePosixPath]:
    """
    Function to instantiate fsspec.filesystem from url.
    Return path relative to filesystem. Can be absolute or not depending on fs.
    This function clean url and extract credentials (if necessary) for you.

    >>> fs, root = get_fsspec_filesystem("tests")
    >>> fs, root = get_fsspec_filesystem("s3://s3-input/Products/", secret_alias="s3-input") # doctest: +SKIP
    >>> fs.ls(root) # doctest: +SKIP

    See `fsspec documentation <https://filesystem-spec.readthedocs.io/en/latest/usage.html>`_

    :param path_or_pattern: path to use to build filesystem
    :param kwargs: see generic input parameters in :obj:`sentineltoolbox.typedefs` module
    :return: fsspec.AbstractFileSystem, path relative to filesystem
    """
    if "filesystem" in kwargs:
        return kwargs["filesystem"]
    else:
        url, credentials = get_url_and_credentials(path_or_pattern, **kwargs)
        protocols, relurl = split_protocol(url)
        if credentials:
            return fsspec.filesystem(**credentials.to_kwargs(target=fsspec.filesystem)), relurl
        else:
            return fsspec.filesystem("::".join(protocols)), relurl


def get_url_and_credentials(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> tuple[str, Credentials | None]:
    """
    Function that cleans url and extract credentials (if necessary) for you.

    :param path_or_pattern:
    :param credentials:
    :param kwargs:
    :return:
    """
    credentials = kwargs.get("credentials")
    if isinstance(path_or_pattern, (str, Path)):
        url = fix_url(str(path_or_pattern))
        conf = get_config(**kwargs)
        secret_alias = conf.get_secret_alias(url)
        if secret_alias:
            kwargs["secret_alias"] = secret_alias
        if _credential_required(url, credentials):
            credentials = S3BucketCredentials.from_env(**kwargs)
    elif is_eopf_adf(path_or_pattern):
        url = str(path_or_pattern.path.original_url)
        if _credential_required(url, credentials):
            storage_options = path_or_pattern.store_params["storage_options"]
            credentials = S3BucketCredentials.from_kwargs(**storage_options)
    else:
        raise NotImplementedError(f"path {path_or_pattern} of type {type(path_or_pattern)} is not supported yet")

    return url, credentials
