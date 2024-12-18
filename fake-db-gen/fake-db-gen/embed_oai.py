import pandas as pd
from tqdm.asyncio import tqdm_asyncio
import asyncio
from langchain_openai import OpenAIEmbeddings


def get_embedding(i, text: str, model_id="text-embedding-ada-002"):
    model = OpenAIEmbeddings(model=model_id)
    embeddings = model.embed_query(text)
    return (i, embeddings)


async def main():
    df = pd.read_csv("data_v2/encodings_0_1_0.csv")
    args = [
        f"""Table: {row['table']}
Table Description: {row['table_description']}
Column: {row['column']}
Column Description: {row['column_description']}"""
        for _, row in df.iterrows()
    ]
    loop = asyncio.get_running_loop()
    results = await tqdm_asyncio.gather(
        *[loop.run_in_executor(None, get_embedding, i, arg) for i, arg in enumerate(args)]
    )
    results = sorted(results, key=lambda x: x[0])
    results = [r[1] for r in results]
    df["embeddings"] = results
    # save to csv
    df.to_csv("data_v2/encodings_with_embeddings_0_1_0.csv", index=False)


if __name__ == "__main__":
    asyncio.run(main())