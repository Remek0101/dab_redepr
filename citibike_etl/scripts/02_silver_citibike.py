import sys
from utils.citibike_utils import get_trip_duration_mins, timestamp_to_date 
# we are using whl soo it works without src prefix in "from", this was configured from setup.py and then build dist and insalled
# as a package installed via the wheel, we can import it directly without the src prefix
# the whl file was also imported to databricks and installed as package on compute package
# for jobs we need to install it on jobs cluster aswell
# in the UI jobs this sits under Dependent libraries

from pyspark.sql.functions import create_map, lit

pipeline_id = sys.argv[1]
run_id = sys.argv[2]
task_id = sys.argv[3]
processed_timestamp = sys.argv[4]
catalog = sys.argv[5]

df = spark.read.table(f"{catalog}.01_bronze.citibike")

df = get_trip_duration_mins(spark, df, "started_at", "ended_at", "trip_duration_mins")

df = timestamp_to_date(df, "started_at", "start_date")

df = df.withColumn("metadata", 
              create_map(
                  lit("pipeline_id"), lit(pipeline_id),
                  lit("run_id"), lit(run_id),
                  lit("task_id"), lit(task_id),
                  lit("processed_date"), lit(processed_timestamp)
                  ))



df.write.\
    mode("overwrite").\
    option("overwriteSchema", "true").\
    saveAsTable(f"{catalog}.02_silver.jc_citibike")