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


def generate_employees_table(n=1000):
    # Open MD file for employees schema
    path = Path("data/schema/employee.md")
    schema = path.read_text()
    print("Schema:\n", schema)

    df: pd.DataFrame = mdpd.from_md(schema)
    print("Dataframe:\n", df)

    # Generate data
    new_df = pd.DataFrame(columns=df["Column"])
    print("New Dataframe:\n", new_df)
    for row in df.iterrows():
        data = row[1]
        vartype = str(data["Type"])
        column = str(data["Column"])
        description = str(data["Description"])
        print("Column:", column, "Type:", vartype, "Description:", description)

        if "int" in vartype.lower():
            # insert n rows in column of the new_df
            new_df[column] = [fake.random_int(20, 65) for _ in range(n)]
        elif "date" in vartype.lower():
            new_df[column] = [fake.date_of_birth() for _ in range(n)]
        elif "float" in vartype.lower():
            new_df[column] = [fake.random_int(30000, 150000) / 1000 for _ in range(n)]
        elif "timestamp" in vartype.lower():
            new_df[column] = [fake.date_time_this_decade() for _ in range(n)]
        elif "varchar" in vartype.lower():
            if "email" in column.lower():
                new_df[column] = [fake.email() for _ in range(n)]
            elif "name" in column.lower():
                new_df[column] = [fake.name() for _ in range(n)]
            elif "city" in column.lower():
                new_df[column] = [fake.city() for _ in range(n)]
            elif "phone" in column.lower() or "contact" in column.lower():
                new_df[column] = [fake.phone_number() for _ in range(n)]
            elif "department" in column.lower():
                new_df[column] = [fake.random_element(elements=("Engineering", "Marketing", "Sales")) for _ in range(n)]
            elif "address" in column.lower():
                new_df[column] = [fake.address().replace("\\r\\n", " ") for _ in range(n)]
            elif "company" in column.lower():
                new_df[column] = [fake.company() for _ in range(n)]
            elif "job" in column.lower():
                new_df[column] = [fake.job() for _ in range(n)]
            elif "text" in vartype.lower():
                new_df[column] = [fake.text() for _ in range(n)]
            elif "password" in column.lower():
                new_df[column] = [fake.password() for _ in range(n)]
            elif "url" in column.lower():
                new_df[column] = [fake.url() for _ in range(n)]
            elif "username" in column.lower():
                new_df[column] = [fake.user_name() for _ in range(n)]
            elif "uuid" in column.lower() or "id" in column.lower() or "code" in column.lower():
                new_df[column] = [fake.uuid4() for _ in range(n)]
            elif "country" in column.lower():
                new_df[column] = [fake.country() for _ in range(n)]
            elif "state" in column.lower():
                new_df[column] = [fake.state() for _ in range(n)]
            elif "zip" in column.lower() or "postal" in column.lower():
                new_df[column] = [fake.zipcode() for _ in range(n)]
            elif "color" in column.lower():
                new_df[column] = [fake.color_name() for _ in range(n)]
            elif "passport" in column.lower():
                new_df[column] = [fake.random_int(1000000000, 9999999999) for _ in range(n)]
            else:
                new_df[column] = [fake.word() for _ in range(n)]

    # replace all \n with \\n
    csv_out = new_df.to_csv(index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
    print("New Dataframe:\n", csv_out)
    # save to csv with proper string escaping
    filename = "data/table/employees.csv"
    new_df.to_csv(filename, index=False, quoting=csv.QUOTE_NONE, escapechar="\\")


if __name__ == "__main__":
    from fire import Fire

    Fire({"gen_employees": generate_employees_table})
