from __future__ import annotations

import packaging.version
from importlib_metadata import version

__all__ = ["__version__"]


__version__ = version("apache_airflow_granulate_databricks")

MIN_DBX_PROVIDER_SUPPORTED_VERSION = "4.2.0"
MAX_DBX_PROVIDER_SUPPORTED_VERSION = "6.5.0"


try:
    from airflow.providers.databricks import __version__ as airflow_dbx_version
except ImportError:
    raise RuntimeError(
        "The package `apache-airflow-granulate-databricks` couldn't verify "
        "the version of apache-airflow-providers-databricks"
    )

if packaging.version.parse(packaging.version.parse(airflow_dbx_version).base_version) < packaging.version.parse(
    MIN_DBX_PROVIDER_SUPPORTED_VERSION
):
    raise RuntimeError(
        f"The package `apache-airflow-granulate-databricks:{__version__}` requires "
        f"apache-airflow-providers-databricks version {MIN_DBX_PROVIDER_SUPPORTED_VERSION} or higher."
    )

if packaging.version.parse(packaging.version.parse(airflow_dbx_version).base_version) > packaging.version.parse(
    MAX_DBX_PROVIDER_SUPPORTED_VERSION
):
    raise RuntimeError(
        f"The package `apache-airflow-granulate-databricks:{__version__}` is not compatible "
        f"with apache-airflow-providers-databricks versions higher than {MAX_DBX_PROVIDER_SUPPORTED_VERSION}."
    )
