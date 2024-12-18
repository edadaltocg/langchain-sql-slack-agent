import json
import pandas as pd
import os
import json
from pathlib import Path
from pprint import pprint


def main():
    root_path = Path("data_v2/slack_5_17")
    channel_name = "demo_v2"
    with open(root_path / "users.json") as f:
        users = json.load(f)

    channel = "demo"
    files_in_demo = os.listdir(root_path / channel)
    messages = []
    for file in files_in_demo:
        with open(root_path / channel / file) as f:
            messages.extend(json.load(f))
    threads = {}
    for msg in messages:
        thread_ts = msg.get("thread_ts", None)
        if not thread_ts:
            continue

        new_msg = {}
        type_of_msg = msg.get("type")
        if type_of_msg == "message":
            if msg.get("text") == "An error occurred. Please try again later.":
                continue
            if thread_ts not in threads:
                threads[thread_ts] = []
            new_msg["username"] = msg.get("user")
            new_msg["content"] = msg.get("text")
            threads[thread_ts].append(new_msg)
    del_keys = []
    for thr in threads.keys():
        if len(threads[thr]) < 2:
            del_keys.append(thr)
    for key in del_keys:
        del threads[key]
    # save to pandas
    df = pd.DataFrame(columns=["thread_ts", "username", "message"])
    for thread_ts in threads.keys():
        for msg in threads[thread_ts]:
            df.loc[len(df)] = [thread_ts, msg["username"], msg["content"]]

    df.to_csv("data_v2/slack_fake_data/threads.csv", index=False)


if __name__ == "__main__":
    main()