import os
from tqdm import tqdm
from pathlib import Path
import glob
import pandas as pd
from langchain_openai import ChatOpenAI
import asyncio

col_cache = {}


def get_table_description(table_name: str, model_id="gpt-4o"):
    llm = ChatOpenAI(model=model_id)
    prompt = f"""Describe in less than 100 characters the table with name: {table_name}

Description:"""
    description = llm.invoke(prompt)
    return description


def get_column_description(column_name: str, model_id="gpt-3.5-turbo"):
    if column_name in col_cache:
        return {column_name: col_cache[column_name]}
    llm = ChatOpenAI(model=model_id, temperature=0)
    prompt = f"""Describe in less than 100 characters a column with a given name that belongs to a table.
Examples:
main_entity_of_page, Description: Identifies the main entity of the page
url, Stores website addresses
{column_name}, Description:"""
    description = llm.invoke(prompt).content
    col_cache[column_name] = description
    return {column_name: description}


async def main(source: str = "data_v2/demo_0_1_0", target: str = "data_v2/encodings_0_1_0"):
    encodings = pd.DataFrame(columns=["table", "table_description", "column", "column_description"])
    for file in tqdm(glob.glob(source + "/*.csv")):
        table_name = os.path.basename(file).split(".")[0]
        table_description = get_table_description(table_name, model_id="gpt-3.5-turbo").content
        df = pd.read_csv(file)
        cols = df.columns.tolist()
        loop = asyncio.get_running_loop()
        cols_description = await asyncio.gather(
            *[loop.run_in_executor(None, get_column_description, col) for col in cols]
        )
        cols_description = {k: v for d in cols_description for k, v in d.items()}
        for col in cols:
            col_description = cols_description[col]
            new_row = {
                "table": table_name,
                "table_description": table_description,
                "column": col,
                "column_description": col_description,
            }
            encodings.loc[len(encodings)] = list(new_row.values())

    encodings.to_csv(f"{target}.csv", index=False)
    print(encodings)


if __name__ == "__main__":
    asyncio.run(main())