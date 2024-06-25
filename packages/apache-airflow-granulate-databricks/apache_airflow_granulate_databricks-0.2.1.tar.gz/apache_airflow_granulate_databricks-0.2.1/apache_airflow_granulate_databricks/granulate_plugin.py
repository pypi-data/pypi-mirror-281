from __future__ import annotations

import importlib.util
import inspect
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Type

from airflow import __version__ as airflow_version
from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.databricks import __version__ as airflow_dbx_version
from airflow.providers.databricks.operators.databricks import (
    DatabricksSubmitRunDeferrableOperator,
    DatabricksSubmitRunOperator,
)

if TYPE_CHECKING:
    from airflow.utils.context import Context

logger = logging.getLogger("airflow.plugins.apache_airflow_granulate_databricks")

GRANULATE_JOB_NAME_KEY: str = "GRANULATE_JOB_NAME"
GRANULATE_JOB_NAME_VALUE: str = "{{ task.task_id }}_{{ task.dag_id }}"


def _add_granulate_env_vars_to_cluster(
    new_cluster: Dict[str, Any], granulate_job_name_value: Optional[str] = None
) -> Dict[str, Any]:
    """
    Adds Granulate environment variables to the new_cluster dictionary.
    If new_cluster is None, initializes it with the required structure.
    """
    if granulate_job_name_value is not None:
        new_cluster.setdefault("spark_env_vars", {})[GRANULATE_JOB_NAME_KEY] = granulate_job_name_value
    else:
        new_cluster.setdefault("spark_env_vars", {})[GRANULATE_JOB_NAME_KEY] = GRANULATE_JOB_NAME_VALUE

    new_cluster["spark_env_vars"]["GRANULATE_AIRFLOW_VERSION"] = str(airflow_version)
    new_cluster["spark_env_vars"]["GRANULATE_AIRFLOW_DATABRICKS_PLUGIN_VERSION"] = str(airflow_dbx_version)
    return new_cluster


class GranulateDatabricksSubmitRunOperator(DatabricksSubmitRunOperator):
    """
    Modified DatabricksSubmitRunOperator to include Granulate-specific environment variables.
    """

    def __init__(self, *args: Any, new_cluster: Optional[Dict[str, Any]] = None, **kwargs: Any):
        if new_cluster is not None:
            new_cluster = _add_granulate_env_vars_to_cluster(new_cluster)
        super().__init__(*args, new_cluster=new_cluster, **kwargs)


class GranulateDatabricksSubmitRunDeferrableOperator(DatabricksSubmitRunDeferrableOperator):
    """
    Modified DatabricksSubmitRunDeferrableOperator to include Granulate-specific environment variables.
    """

    def __init__(self, *args: Any, new_cluster: Optional[Dict[str, Any]] = None, **kwargs: Any):
        if new_cluster is not None:
            new_cluster = _add_granulate_env_vars_to_cluster(new_cluster)
        super().__init__(*args, new_cluster=new_cluster, **kwargs)  # type: ignore


def _validate_method(operator: Type[BaseOperator], method_name: str, expected_signature: inspect.Signature) -> None:
    if not hasattr(operator, method_name):
        raise RuntimeError(
            f"The operator {operator.__name__} does not have the method {method_name}. "
            "You might be using an unsupported version of apache-airflow-providers-databricks."
        )

    actual_signature = inspect.signature(getattr(operator, method_name))

    actual_param_names = [param.name for param in actual_signature.parameters.values()]
    expected_param_names = [param.name for param in expected_signature.parameters.values()]

    if actual_param_names != expected_param_names:
        raise RuntimeError(
            f"The method {method_name} of {operator.__name__} has an unexpected signature. "
            "You might be using an unsupported version of apache-airflow-providers-databricks."
        )


def patch() -> None:
    """
    Patches the DAG to include Granulate job name for Databricks operators.
    """
    try:
        from airflow.providers.databricks.operators.databricks import (
            DatabricksSubmitRunDeferrableOperator,
            DatabricksSubmitRunOperator,
        )

        def granulate_execute(self: Any, context: Context, original_execute: Callable[..., Any]) -> Any:
            try:
                if "new_cluster" in self.json:
                    _add_granulate_env_vars_to_cluster(
                        self.json["new_cluster"], granulate_job_name_value=f"{self.task_id}_{self.dag.dag_id}"
                    )
                else:
                    self.log.info("Operator's json doesn't contain `new_cluster`, skip patching")

                self.log.debug("Passed Granulate job name to Databricks Submit Run Operator API")
            except Exception:
                logger.exception("Got an exception in granulate_execute")
            return original_execute(self, context)

        def patch_execute_method(operator_class: Type[BaseOperator], original_execute: Callable[..., Any]) -> None:
            def patched_execute(self: Any, context: Context) -> Any:
                return granulate_execute(self, context, original_execute)

            expected_execute_signature = inspect.signature(patched_execute)
            _validate_method(DatabricksSubmitRunOperator, "execute", expected_execute_signature)
            _validate_method(DatabricksSubmitRunDeferrableOperator, "execute", expected_execute_signature)

            operator_class.execute = patched_execute  # type: ignore

        patch_execute_method(DatabricksSubmitRunOperator, DatabricksSubmitRunOperator.execute)
        logger.debug("Patched DatabricksSubmitRunOperator.execute")

        patch_execute_method(DatabricksSubmitRunDeferrableOperator, DatabricksSubmitRunDeferrableOperator.execute)
        logger.debug("Patched DatabricksSubmitRunDeferrableOperator.execute")

    except ImportError as e:
        logger.warning(f"Failed to import {e.name}, skipping patch")
    except Exception:
        logger.exception("Failed to patch Databricks Operator classes.")


class GranulatePlugin(AirflowPlugin):
    """
    Airflow Plugin to integrate Granulate with Databricks operators.
    """

    name = "granulate"

    def on_load(*args: Any, **kwargs: Any) -> Any:  # type: ignore
        """
        Loads the Granulate plugin. Patches DAG if the auto-patch feature is enabled.
        """
        if importlib.util.find_spec("apache_airflow_granulate_databricks_auto_patch") is not None:
            patch()
        else:
            logger.debug("Granulate auto-patch feature not enabled")
