
import sys

sys.path += ["../../../core", "../../../config"]

print(f'sys.path: {sys.path}')

import json
import os
from typing import List

from tabulate import tabulate

# noinspection PyUnresolvedReferences
from snowflake.snowpark.functions import col

# noinspection PyUnresolvedReferences
from snowflake.snowpark.row import Row

# noinspection PyUnresolvedReferences
from snowflake.snowpark.types import StructType, StructField, StringType, DateType, TimestampType, DecimalType, BooleanType

from hl_config import HLConfig
from snowflake.hl_snowflake import HLSnowflake


def import_data(data_import_section_name: str) -> None:
    """Imports data from a CSV file using a section config
    :param data_import_section_name: Name of the section in the data import section config
    :type data_import_section_name: int
    :return:
    :rtype:
    """
    # Initialize all the variables
    project_root = HLConfig.PROJECT_ROOT
    config_path = os.path.join(project_root, "config.json")
    config = json.loads(open(config_path, "r").read())

    csv_params = config["data_import"]["csv_params"]

    # To import a specific CSV file, change the last key name
    data_import_params = config["data_import"]["csv_params"][data_import_section_name]

    csv_file_name = data_import_params["csv_file_name"]

    csv_path = os.path.join(project_root, HLConfig.CSV_FILE_PATH, csv_file_name)

    stage_name = csv_params["stage_name"]
    file_format_name = csv_params["file_format_name"]

    stage_file_path = f"{stage_name}/{csv_file_name}.gz"

    table_name = data_import_params["table_name"]

    schema_json_name = data_import_params["schema_json_name"]

    schema_json_path = os.path.join(project_root, HLConfig.CSV_DATA_SCHEMA_PATH, schema_json_name)

    print(f"config_path: {config_path}")
    print(f"schema_json_path: {schema_json_path}")
    print(f"csv_path: {csv_path}")
    print(f"stage_name: {stage_name}")
    print(f"file_format_name: {file_format_name}")
    print(f"stage_file_path: {stage_file_path}")
    print(f"table_name: {table_name}")

    # Open the connection and initialize the session
    snowpark_session = HLSnowflake.create_session()

    # Create the staging area
    snowpark_session.sql(f"CREATE OR REPLACE STAGE {stage_name};").collect()

    snowpark_session.sql(f"CREATE OR REPLACE FILE FORMAT {file_format_name} TYPE = 'csv' FIELD_DELIMITER = ',' FIELD_OPTIONALLY_ENCLOSED_BY = '\"';").collect()

    # Upload the local file to the stage
    snowpark_session.file.put(csv_path, f"@{stage_name}", overwrite=True)

    # Read the CSV file and write to the table
    table_ref = snowpark_session.table(table_name)

    # Delete the existing records as per the flag
    delete_params = data_import_params["delete_params"]
    delete_existing_rows = delete_params["flag"]

    if delete_existing_rows:
        delete_sql_text = delete_params["sql_text"]
        delete_filter_col_name = delete_params["filter_query"]["filter_column"]
        delete_filter_value = delete_params["filter_query"]["filter_value"]

        if delete_sql_text != "":
            snowpark_session.sql(delete_sql_text).collect()
        elif delete_filter_col_name != "":
            table_ref.delete(table_ref[delete_filter_col_name] == delete_filter_value)
        # else:
        # WARNING: UNCOMMENT IF YOU WANT TO GO NUCLEAR
        #    table_ref.delete()

    # Read and build the table schema array
    schema_json = json.loads(open(schema_json_path, mode="r").read())

    fields = []

    for column in schema_json:
        if column["type"] == "string":
            fields.append(StructField(column["name"], StringType(), column["nullable"]))
        elif column["type"] == "number":
            fields.append(StructField(column["name"], DecimalType(), column["nullable"]))
        elif column["type"] == "boolean":
            fields.append(StructField(column["name"], BooleanType(), column["nullable"]))
        elif column["type"] == "date":
            fields.append(StructField(column["name"], DateType(), column["nullable"]))
        elif column["type"] == "datetime":
            fields.append(StructField(column["name"], TimestampType(), column["nullable"]))

    table_schema = StructType(fields)

    read_options = {"field_delimiter": ",", "field_optionally_enclosed_by": '"'}
    csv_data_df = snowpark_session.read.options(read_options).schema(table_schema).csv(f"@{stage_file_path}")

    csv_data_df.write.save_as_table({table_name}, mode="append", column_order="name")

    table_ref = snowpark_session.table(table_name)

    select_params = data_import_params["select_params"]
    select_sql_text = select_params["sql_text"]
    select_filter_col_name = select_params["filter_query"]["filter_column"]
    select_filter_value = select_params["filter_query"]["filter_value"]

    if select_sql_text != "":
        select_results: List[Row] = snowpark_session.sql(select_sql_text).collect()
        tabulate(select_results, headers="keys", tablefmt="pretty")
    elif select_filter_col_name != "":
        tabulate(table_ref.filter(col(select_filter_col_name) == select_filter_value).toPandas(), headers="keys", tablefmt="pretty")
    # else:
    #     tabulate(table_ref.toPandas(), headers="keys", tablefmt="pretty")

    # Clean up
    snowpark_session.sql(f"REMOVE @{stage_file_path};").collect()

    snowpark_session.sql(f"DROP FILE FORMAT IF EXISTS {file_format_name};").collect()

    snowpark_session.sql(f"DROP STAGE IF EXISTS {stage_name};").collect()

    # Close the session
    snowpark_session.close()

    print(f"CSV data imported: {csv_path}")


if __name__ == "__main__":
    # dm_rule
    # search_hits
    data_import_csv_section_name = "search_hits"

    import_data(data_import_csv_section_name)

    print(f"Data import complete for the section: {data_import_csv_section_name}")
