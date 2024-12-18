import os
from pathlib import Path
import pandas as pd

data_path = Path("data_v2")
schema_path = data_path / "schema_org" / "types.csv"

keep_columns = ["label", "properties", "comment"]
types_df = pd.read_csv(schema_path)
types_df = types_df[keep_columns]

# clean
types_df.properties = types_df.properties.str.replace("https://schema.org/", "")
# remove NaN rows
types_df = types_df.dropna(axis=0).reset_index(drop=True)

# print df summary
print(types_df.info())

# types with invoice, offer, job, credit, organization, order, employer, product, person in the label
label_filter = ["invoice", "offer", "job", "creditcard", "organization", "order", "employer", "product", "person"]
types_df_filtered = types_df[types_df["label"].str.contains("|".join(label_filter), case=False)]
remove_labels = [
    "FinancialProduct",
    "OfferForLease",
    "IndividualProduct",
    "ArchiveOrganization",
    "ResearchOrganization",
    "MedicalOrganization",
    "EducationalOrganization",
    "GovernmentOrganization",
    "SportsOrganization",
    "SearchRescueOrganization",
    "NewsMediaOrganization",
    "NGO",
    "LocalBusiness",
    "Corporation",
    "Organization",
]
types_df_filtered = types_df_filtered[~types_df_filtered["label"].isin(remove_labels)]
types_df_filtered = types_df_filtered.reset_index(drop=True)
# replace all comments by empty string
types_df_filtered = types_df_filtered.assign(comment="")
types_df_filtered.to_csv(data_path / "schema_org" / "tables_raw.csv", index=False)
print(types_df_filtered)

# get all unique properties:
columns = types_df_filtered["properties"].str.split(",").explode().unique()
columns.sort()
columns = pd.DataFrame(columns, columns=["properties"])
columns = columns.assign(comment="")
# remove leading whitespaces
columns = columns.apply(lambda x: x.str.strip())
# find tables they appear
tables_for_column = {}
for col in columns["properties"]:
    tables_for_column[col] = ", ".join(
        types_df_filtered[types_df_filtered["properties"].str.contains(col)]["label"].values.tolist()
    )
# insert new coumn with tables
columns["tables"] = columns["properties"].map(tables_for_column)
# reorder columns
columns = columns[["properties", "tables", "comment"]]
# rename columns
columns.rename(
    columns={"properties": "column", "tables": "tables_column_appears", "comment": "description"}, inplace=True
)

columns.to_csv(data_path / "schema_org" / "columns_raw.csv", index=False)

print(columns)
