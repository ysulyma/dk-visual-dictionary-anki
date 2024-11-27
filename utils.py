import genanki
import pprint
import sqlite3
from typing import Generator, Iterator, Optional

from schema import Article, Chapter, Context, Entry, Section, Word

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


def fetch_all_ordered(
    ctx: Context,
    chapters=True,
    articles=True,
    sections=True,
    words=True,
    page_min: Optional[int] = None,
    page_max: Optional[int] = None,
) -> Generator[Entry, None, None]:
    """
    Fetches all entries ordered by order_id, collapsing Article/Chapter/Section/Word distinctions
    """

    # build query
    queries = []
    if chapters:
        chapter_query = Chapter.entry_query

        if page_min is not None or page_max is not None:
            chapter_query += " WHERE " + Chapter.page_clause(page_min, page_max)

        queries.append(chapter_query)
    if articles:
        article_query = Article.entry_query

        if page_min is not None or page_max is not None:
            article_query += " WHERE " + Article.page_clause(page_min, page_max)

        queries.append(article_query)
    if sections:
        section_query = Section.entry_query

        if page_min is not None or page_max is not None:
            section_query += " WHERE " + Section.page_clause(page_min, page_max)

        queries.append(section_query)
    if words:
        word_query = Word.entry_query

        if page_min is not None or page_max is not None:
            word_query += " WHERE " + Word.page_clause(page_min, page_max)

        queries.append(word_query)

    union_query = " UNION ".join(queries)

    cursor = ctx.conn.execute(
        f"""
        {union_query}
        ORDER BY order_id
        """
    )

    for row in cursor:
        yield Entry.from_row(row)


def make_note(ctx: Context, entry: Entry):
    """
    Makes a note
    """
    # add audio
    ctx.package.media_files.append(f"{ctx.AUDIO_DIR}/{entry.audio}")

    # add note
    return genanki.Note(
        model=genanki.BASIC_AND_REVERSED_CARD_MODEL,
        fields=[f"{entry.front}<br>[sound:{entry.audio}]", entry.back],
        tags=[f"page:{entry.page_number}"],
    )
