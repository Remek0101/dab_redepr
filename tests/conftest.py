import os
import sys

import pytest
from pyspark.sql import SparkSession

sys.path.append(os.getcwd())


@pytest.fixture(scope="session")
def spark():
    try:
        from databricks.connect import DatabricksSession

        session = DatabricksSession.builder.getOrCreate()
    except ImportError:
        session = SparkSession.builder.master("local[1]").appName("tests").getOrCreate()
    yield session
    session.stop()
