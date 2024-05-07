import re
import pandas as pd


def mdtable2csv(markdown_table):
    """It does not work with empty cells."""
    pattern = r"\| ([\w\s]+) \| ([\w\s]+) \| ([\w\s]+) \|"
    matches = re.findall(pattern, markdown_table)
    header = matches[0]
    data = matches[1:]
    csv_table = ",".join(header) + "\n"
    for row in data:
        csv_table += ",".join(row) + "\n"
    return csv_table


def mdtable2pandas(markdown_table):
    """It does not work with empty cells."""
    pattern = r"\| ([\w\s]+) \| ([\w\s]+) \| ([\w\s]+) \|"
    matches = re.findall(pattern, markdown_table)
    header = matches[0]
    data = matches[1:]
    df = pd.DataFrame(data, columns=header)
    return df


# Example usage
def test_mdtable2csv():
    markdown_table = """
| Name | Age | City |
| ----- | ----- | ----- |
| Alice | 25 | New York |
| Bob | 30 | Los Angeles |
| Charlie | 22 | Chicago |
"""
    expected_csv = "Name,Age,City\nAlice,25,New York\nBob,30,Los Angeles\nCharlie,22,Chicago\n"

    csv_output = mdtable2csv(markdown_table)
    print(csv_output)
    assert csv_output == expected_csv


if __name__ == "__main__":
    test_mdtable2csv()