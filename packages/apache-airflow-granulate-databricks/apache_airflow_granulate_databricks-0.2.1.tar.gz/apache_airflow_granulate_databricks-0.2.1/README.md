# Granulate Airflow-Databricks Integration

## Overview
The Granulate Airflow-Databricks Integration is an open-source plugin for Apache Airflow. It's specifically designed to set environment variables that allow Granulate's performance monitoring agent to identify and integrate with Databricks jobs orchestrated by Airflow. This plugin tags Databricks jobs, aiding the Granulate optimizing agent.

## Modes of Operation
The Granulate plugin can operate in three different modes:

1. **Passive Mode**: In this mode, you need to manually replace `DatabricksSubmitRunOperator` and `DatabricksSubmitRunDeferrableOperator` with `GranulateDatabricksSubmitRunOperator` and `GranulateDatabricksSubmitRunDeferrableOperator` respectively in your DAGs. This mode allows you to selectively apply Granulate to specific operators. The `Granulate` operators are drop-in replacement for their respective operators, so you can just swap them in code for relevant DAGs.

2. **Auto-Patch for Specific DAGs**: To enable auto-patching on specific DAGs, import and invoke the `patch` function from the plugin at the beginning of your DAG file:
   ```python
   from apache_airflow_granulate_databricks.granulate_plugin import patch
   patch()
   ```
    This method patches the Databricks operators in the DAG where it's called, enabling the Granulate environment variable.

3. **Auto-Patch for All DAGs**: For an all-encompassing approach, install the plugin with the 'auto-patch' extra:
   ```pip install apache-airflow-granulate-databricks[auto-patch]```
    This mode patches all Databricks operators across all DAGs in your Airflow environment, automatically applying Granulate enhancements.

## Installation
To install the apache-airflow-granulate-databricks package, choose the method that best fits your setup:
- Using pip:
  - For a standard installation, run:
    ```pip install apache-airflow-granulate-databricks```
  - To enable automatic DAG patching, include the auto-patch extra:
    ```pip install apache-airflow-granulate-databricks[auto-patch]```
- Using `_PIP_ADDITIONAL_REQUIREMENTS` in Airflow:
    - Append the following line to your _PIP_ADDITIONAL_REQUIREMENTS:
      ```apache-airflow-granulate-databricks```
    - For auto-patching, use:
      ```apache-airflow-granulate-databricks[auto-patch]```
    - Restart your Airflow services to apply these changes.

## Package Removal
- If you used pip to install, run: ```pip uninstall apache-airflow-granulate-databricks```
- If you used `_PIP_ADDITIONAL_REQUIREMENTS`, remove `apache-airflow-granulate-databricks`
- Make sure to revert your code if you used Granulate's operators, or you you used the `patch` function.
- Restart your Airflow services to apply these changes.

## Requirements
- Tested on Databricks Airflow Provider (4.2.0 <= version <= 6.5.0)
- Python version 3.8 or higher

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support
For support, questions, or issues, please open an issue in the GitHub repository.
