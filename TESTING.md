# Testing

## Running the tests

Use the `.venv-pyspark` environment (it has `pyspark` and `pytest`). From the project root:

```
.venv-pyspark/Scripts/python -m pytest tests
```

`.venv` has `databricks-connect` but no `pytest`, and Databricks Connect cannot start a local Spark session,
so it is not used for these tests.

## Why `tests/conftest.py` exists

`test_get_trip_duration_mins(spark)` takes a `spark` argument. pytest resolves test arguments by name from
*fixtures*, and pytest has no built-in `spark` fixture. Without one, the test fails at setup with
`fixture 'spark' not found` before any test code runs.

`tests/conftest.py` is loaded automatically by pytest and defines that fixture:

- `scope="session"`: Spark takes several seconds to start, so it starts once per test run, not once per test.
- `master("local[1]")`: runs Spark in-process, so no Databricks cluster is needed.
- `yield` then `session.stop()`: shuts the session down cleanly after the last test.
- `sys.path.append(os.getcwd())`: lets `from src.utils... import ...` resolve when pytest runs from the project root.

## Why the test file was changed

- Removed `spark = SparkSession.builder.getOrCreate()` inside the test. It overwrote the injected fixture with a
  new session, so the fixture was no longer the single place that controls how Spark is created.
- Removed the now-unused `SparkSession` import.

## Running on the Databricks cluster (`.venv`)

The `spark` fixture tries `DatabricksSession.builder.getOrCreate()` first and falls back to local Spark if
`databricks.connect` is not installed. So:

- `.venv` (databricks-connect + pytest): tests run on the cluster from the `DEFAULT` profile in `~/.databrickscfg`.
  If the cluster is terminated, the first run starts it and can take several minutes.
- `.venv-pyspark`: tests run on local Spark.

Run with `.venv/Scripts/python -m pytest tests`.
