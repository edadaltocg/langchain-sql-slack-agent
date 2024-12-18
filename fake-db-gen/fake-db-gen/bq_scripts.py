from google.cloud import bigquery
import os
from pathlib import Path
from google.cloud import storage
import pandas as pd
import random
import re


def test_create_public_csv():
    client = bigquery.Client()
    project_name = "future-frame"
    dataset_name = "all_data"
    table_name = "fake_data"
    table_id = f"{project_name}.{dataset_name}.{table_name}"

    # SchemaField(
    #     name: str,
    #     field_type: str,
    #     mode: str = "NULLABLE",
    #     default_value_expression: str | None = None,
    #     description: str | _DefaultSentinel = _DEFAULT_VALUE,
    #     fields: Iterable[SchemaField] = (),
    #     policy_tags: PolicyTagList | _DefaultSentinel | None = _DEFAULT_VALUE,
    #     precision: int | _DefaultSentinel = _DEFAULT_VALUE,
    #     scale: int | _DefaultSentinel = _DEFAULT_VALUE,
    #     max_length: int | _DefaultSentinel = _DEFAULT_VALUE,
    #     range_element_type: FieldElementType | str | None = None
    # )
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("post_abbr", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))


def clean_bulk_upload_empty_tables(project_name="future-frame", dataset_name="demo_0_1_0"):
    client = bigquery.Client()
    dataset_id = f"{project_name}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset = client.create_dataset(dataset, exists_ok=True, timeout=30)
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
    snake_case_pattern = re.compile(r"(?<!^)(?=[A-Z])")
    make_table_id = lambda x: f"{dataset_id}.{x}"

    for _ in range(1):
        tables = pd.read_csv("data_v2/schema_org/tables.csv")
        # tables df columns: "label","properties","comment"
        columns = pd.read_csv("data_v2/schema_org/columns.csv")
        # columns df columns: column,tables,description
        for i, row in tables.iterrows():
            table_name_has_underline = False
            table_name = row["label"]
            if table_name_has_underline:
                table_name = snake_case_pattern.sub("_", table_name).lower()
            table_name_has_old = False
            if table_name_has_old:
                table_name = f"{table_name}_old"
            table_name_has_year = False
            if table_name_has_year:
                table_name = f"{table_name}_{random.randint(2015, 2020)}"

            table_id = make_table_id(table_name)
            table_description = row["comment"]
            table_columns = row["properties"].split(",")
            # clean white spaces
            table_columns = [col.strip() for col in table_columns]
            # print(table_id, columns, table_description)
            schema = []
            for col_name in table_columns:
                # query columns df
                col_description = columns[columns["column"] == col_name]["description"]
                col_description_str = col_description.to_string(index=False)
                assert isinstance(col_description_str, str)
                col_name_has_underline = False
                if col_name_has_underline:
                    col_name = snake_case_pattern.sub("_", col_name).lower()
                schema.append(bigquery.SchemaField(col_name, "STRING", description=col_description_str))

            table = bigquery.Table(table_id, schema=schema)
            table.description = table_description
            table = client.create_table(table, exists_ok=True, timeout=30)
            print(
                "Created table {}.{}.{} with description: {}".format(
                    table.project, table.dataset_id, table.table_id, table.description
                )
            )


def bulk_upload_empty_tables(project_name="future-frame", dataset_name="demo_0_1_0", n=10):
    client = bigquery.Client()
    dataset_id = f"{project_name}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset = client.create_dataset(dataset, exists_ok=True, timeout=30)
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
    snake_case_pattern = re.compile(r"(?<!^)(?=[A-Z])")
    make_table_id = lambda x: f"{dataset_id}.{x}"

    for _ in range(n):
        tables = pd.read_csv("data_v2/schema_org/tables.csv")
        # tables df columns: "label","properties","comment"
        columns = pd.read_csv("data_v2/schema_org/columns.csv")
        # columns df columns: column,tables,description
        for i, row in tables.iterrows():
            table_name_has_underline = random.random() < 0.25
            table_name = row["label"]
            if table_name_has_underline:
                table_name = snake_case_pattern.sub("_", table_name).lower()
            table_name_has_old = random.random() < 0.2
            if table_name_has_old:
                table_name = f"{table_name}_old"
            table_name_has_year = random.random() < 0.5
            if table_name_has_year:
                table_name = f"{table_name}_{random.randint(2015, 2020)}"

            table_id = make_table_id(table_name)
            table_description = row["comment"]
            table_columns = row["properties"].split(",")
            # clean white spaces
            table_columns = [col.strip() for col in table_columns]
            # print(table_id, columns, table_description)
            schema = []
            for col_name in table_columns:
                # query columns df
                col_description = columns[columns["column"] == col_name]["description"]
                col_description_str = col_description.to_string(index=False)
                assert isinstance(col_description_str, str)
                col_name_has_underline = random.random() < 0.5
                if col_name_has_underline:
                    col_name = snake_case_pattern.sub("_", col_name).lower()
                schema.append(bigquery.SchemaField(col_name, "STRING", description=col_description_str))

            table = bigquery.Table(table_id, schema=schema)
            table.description = table_description
            table = client.create_table(table, exists_ok=True, timeout=30)
            print(
                "Created table {}.{}.{} with description: {}".format(
                    table.project, table.dataset_id, table.table_id, table.description
                )
            )


def create_bucket_class_location(bucket_name: str = "future-frame"):
    """
    Create a new bucket in the US region with the coldline storage
    class
    """
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket


def export_tables_to_bucket(project="future-frame", dataset_id: str = "demo_0_1_0"):
    client = bigquery.Client()
    bucket_name = "future-frame"
    tables = client.list_tables(dataset_id)
    for table in tables:
        table_id = table.table_id

        destination_uri = "gs://{}/{}/{}".format(bucket_name, dataset_id, f"{table_id}.csv")
        dataset_ref = bigquery.DatasetReference(project, dataset_id)
        table_ref = dataset_ref.table(table_id)

        extract_job = client.extract_table(table_ref, destination_uri)
        extract_job.result()  # Waits for job to complete.

        print("Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri))


def delete_bucket(bucket_name: str = "future-frame", folder_name: str = "demo_0_1_0"):
    storage_client = storage.Client()
    bucket_name = f"{bucket_name}/{folder_name}"
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()
        print(f"Deleted {blob.name}")
    bucket.delete()
    print(f"Deleted {bucket_name}")


def download_bucket(bucket_name: str = "future-frame", folder_name: str = "demo_0_1_0", destination="data_v2"):
    storage_client = storage.Client()
    dest_path = Path(destination)
    bucket = storage_client.bucket(bucket_name)
    # list blobs in the bucket
    blobs = bucket.list_blobs()
    for blob in blobs:
        if not (dest_path / blob.name).exists():
            blob.download_to_filename(dest_path / blob.name)
            print(f"Downloaded {blob.name} to {dest_path / blob.name}")
        # print(f"Downloaded {blob.name} to {dest_path / blob.name}")


if __name__ == "__main__":
    from fire import Fire

    Fire(
        {
            "bulk_upload_empty_tables": bulk_upload_empty_tables,
            "clean_bulk_upload_empty_tables": clean_bulk_upload_empty_tables,
            "create_bucket": create_bucket_class_location,
            "export_tables_to_bucket": export_tables_to_bucket,
            "delete_bucket": delete_bucket,
            "download_bucket": download_bucket,
        }
    )
