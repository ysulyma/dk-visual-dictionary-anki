import pprint
import sqlite3

pp = pprint.PrettyPrinter(indent=2)


def describe_table(cursor: sqlite3.Cursor, table_name: str):
    """
    (development only) Prints the first row of table to the console
    """
    # describe section table
    cursor.execute(f"SELECT * FROM {table_name}")

    for row in cursor:
        dict = {}
        for i in row.keys():
            dict[i] = row[i]

        pp.pprint(dict)
        break
