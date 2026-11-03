from pyspark.sql.functions import unix_timestamp, col, to_date
from pyspark.sql import DataFrame

def get_trip_duration_mins(spark, df: "DataFrame", start_col: str, end_col: str, output_col: str) -> "DataFrame":

    """
    Calculate the trip duration in minutes.

    Parameters:
    spark : SparkSession
        The Spark session.
    df : DataFrame
        The input DataFrame containing the trip data.
    start_col : str
        The name of the column containing the trip start timestamp.
    end_col : str
        The name of the column containing the trip end timestamp.
    output_col : str
        The name of the column to store the calculated trip duration in minutes.

    Returns:
    DataFrame
        The DataFrame with an additional column for trip duration in minutes.
    """

    return df.withColumn(
        output_col,
        (unix_timestamp(col(end_col)) - unix_timestamp(col(start_col))) / 60
    )




def timestamp_to_date(df: "DataFrame", timestamp_col: str, output_col: str) -> "DataFrame":
    """
    Convert a timestamp column to a date column.

    Parameters:
    df : DataFrame
        The input DataFrame containing the timestamp column.
    timestamp_col : str
        The name of the column containing the timestamp.
    output_col : str
        The name of the column to store the converted date.

    Returns:
    DataFrame
        The DataFrame with an additional column for the date.
    """

    return df.withColumn(output_col, to_date(col(timestamp_col)))
