import os
import csv
import mdpd
import pandas as pd
from pathlib import Path
from faker import Faker
import utils

pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 1000)

fake = Faker()
Faker.seed(42)


def schemas2csv(filename: str):
    path = Path(f"data/schema/{filename}.md")
    schema = path.read_text()
    if not schema:
        print("Schema not found")
        return
    if schema == "":
        print("Schema is empty")
        return

    df: pd.DataFrame = mdpd.from_md(schema)
    print("Dataframe:\n", df)
    csvfile = f"data/schema/{filename}.csv"
    df["Column"] = df["Column"].apply(lambda x: str(x).lower())
    df.columns = [str(col).lower() for col in df.columns]
    df.to_csv(csvfile, index=False)


def generate_table(filename: str, n=1000):
    # Open MD file for employees schema
    path = Path(f"data/schema/{filename}.md")
    schema = path.read_text()
    print("Schema:\n", schema)

    df: pd.DataFrame = mdpd.from_md(schema)
    print("Dataframe:\n", df)

    # Generate data
    new_df = pd.DataFrame()
    print("New Dataframe:\n", new_df)
    for row in df.iterrows():
        data = row[1]
        vartype = str(data["Type"]).lower()
        column = str(data["Column"]).lower()
        description = str(data["Description"]).lower()
        print("Column:", column, "Type:", vartype, "Description:", description)

        if "int" in vartype:
            # insert n rows in column of the new_df
            if "id" in column:
                new_df[column] = [fake.uuid4() for _ in range(n)]
            else:
                new_df[column] = [fake.random_int(0, 999999) for _ in range(n)]
        elif "date" in vartype:
            new_df[column] = [fake.date_of_birth() for _ in range(n)]
        elif "float" in vartype:
            new_df[column] = [fake.random_int(30000, 150000) / 1000 for _ in range(n)]
        elif "timestamp" in vartype:
            new_df[column] = [fake.date_time_this_decade() for _ in range(n)]
        elif "bool" in vartype:
            new_df[column] = [fake.boolean() for _ in range(n)]

        if "email" in column:
            new_df[column] = [fake.email() for _ in range(n)]
        elif "name" in column:
            new_df[column] = [fake.name() for _ in range(n)]
        elif "city" in column:
            new_df[column] = [fake.city() for _ in range(n)]
        elif "phone" in column or "contact" in column:
            new_df[column] = [fake.phone_number() for _ in range(n)]
        elif "department" in column:
            new_df[column] = [fake.random_element(elements=("Engineering", "Marketing", "Sales")) for _ in range(n)]
        elif "address" in column:
            new_df[column] = [fake.address().replace("\n", " ") for _ in range(n)]
        elif "company" in column:
            new_df[column] = [fake.company() for _ in range(n)]
        elif "job" in column:
            new_df[column] = [fake.job() for _ in range(n)]
        elif "text" in vartype:
            new_df[column] = [fake.text() for _ in range(n)]
        elif "password" in column:
            new_df[column] = [fake.password() for _ in range(n)]
        elif "url" in column:
            new_df[column] = [fake.url() for _ in range(n)]
        elif "username" in column:
            new_df[column] = [fake.user_name() for _ in range(n)]
        elif "uuid" in column or "id" in column:
            new_df[column] = [fake.uuid4() for _ in range(n)]
        elif "country" in column:
            new_df[column] = [fake.country() for _ in range(n)]
        elif "state" in column:
            new_df[column] = [fake.state() for _ in range(n)]
        elif "zip" in column or "postal" in column:
            new_df[column] = [fake.zipcode() for _ in range(n)]
        elif "color" in column:
            new_df[column] = [fake.color_name() for _ in range(n)]
        elif "passport" in column:
            new_df[column] = [fake.random_int(1000000000, 9999999999) for _ in range(n)]
        elif "ssn" in column:
            new_df[column] = [fake.ssn() for _ in range(n)]
        elif "credit" in column:
            new_df[column] = [fake.credit_card_number() for _ in range(n)]
        elif "currency" in column:
            new_df[column] = [fake.currency_code() for _ in range(n)]
        else:
            new_df[column] = [fake.word() for _ in range(n)]

        print("New Dataframe:\n", new_df)

    # replace all \n with space
    new_df = new_df.apply(lambda x: x.str.replace("\n", " "), axis=1)

    csv_out = new_df.to_csv(index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
    print("New Dataframe:\n", csv_out)
    filename = f"data/table/{filename}.csv"
    new_df.to_csv(filename, index=False, quoting=csv.QUOTE_NONE, escapechar="\\")


def gen_all(n=1000):
    for file in os.listdir("data/schema"):
        if file.endswith(".md"):
            filename = file.split(".")[0]
            schemas2csv(filename)
            generate_table(filename, n)


if __name__ == "__main__":
    from fire import Fire

    Fire(
        {
            "gen_table": generate_table,
            "schemas2csv": schemas2csv,
            "all": gen_all,
        }
    )
