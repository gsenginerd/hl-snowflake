import sys

sys.path += ["src/core", "src/common", "src/utils"]
import pandas as pd

from IPython.display import display

# noinspection PyUnresolvedReferences
from snowflake.snowpark.functions import col

from conflicts_check.snowflake.hl_snowflake import HLSnowflake


def stage_request_stripped_names(cc_request_id: int) -> None:
    """
    This function stages stripped names from a conflicts check request in a Snowflake staging table.

    :param cc_request_id: The parameter cc_request_id is an integer that represents the ID of a
    conflicts check request. This function retrieves the stripped names associated with the conflicts
    check request and stages them in a Snowflake table for further processing
    :type cc_request_id: int
    """
    # Open the connection and initialize the session
    snowpark_session = HLSnowflake.create_session()

    get_request_stripped_names_result = snowpark_session.sql(f"CALL DBO.STO_GET_REQUEST_STRIPPED_NAMES({cc_request_id})").collect()

    request_stripped_names_df = pd.DataFrame(get_request_stripped_names_result)

    # Update the request ID for all the rows
    request_stripped_names_df.insert(0, "CONFLICTS_CHECK_REQUEST_ID", cc_request_id)

    # Delete the existing records for the request from the staging table
    stage_request_stripped_name_table = snowpark_session.table("STAGE_REQUEST_STRIPPED_NAME")
    stage_request_stripped_name_table.delete(stage_request_stripped_name_table["CONFLICTS_CHECK_REQUEST_ID"] == cc_request_id)

    # Write the name strings to the staging table
    request_stripped_names_stage_df = snowpark_session.create_dataframe(request_stripped_names_df)

    request_stripped_names_stage_df.write.mode("append").save_as_table("STAGE_REQUEST_STRIPPED_NAME")

    # Get the inserted records
    get_inserted_records_result = stage_request_stripped_name_table.filter(col("CONFLICTS_CHECK_REQUEST_ID") == cc_request_id).collect()
    inserted_records_df = pd.DataFrame(get_inserted_records_result)

    display(inserted_records_df)


if __name__ == "__main__":
    stage_request_stripped_names(78353)
