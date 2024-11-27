import sqlite3

import genanki

from schema import Article, Chapter, Context
from utils import fetch_all_ordered, make_note

# config
AUDIO_DIR = "audio"
DB_FILE = "db.sqlite3"

DECK_ID = 1892930485
# TEST_DECK_ID = 1355766856


DECK_NAME = "Ukrainian Visual Dictionary"
OUTPUT_FILE = "ukrainian-english.apkg"

# don't change this
NULL_STRING = "(null)"

deck_counter = 0


# create a deck
# deck = genanki.Deck(DECK_ID, DECK_NAME)

# create a package
package = genanki.Package([])

# connect to the database
with sqlite3.connect(DB_FILE) as conn:
    conn.row_factory = sqlite3.Row

    ctx = Context(AUDIO_DIR=AUDIO_DIR, conn=conn, package=package)

    # get chapters
    chapters = [*Chapter.fetch_all(ctx)]
    for i, chapter in enumerate(chapters):
        # compute page boundaries
        chapter_first_page = chapter.chapterpagenumber
        if i == len(chapters) - 1:
            chapter_last_page = 10000000000000000000000
        else:
            chapter_last_page = chapters[i + 1].chapterpagenumber - 1

        # log
        print(f"{chapter.chaptertrans} {chapter_first_page} - {chapter_last_page}")

        # get articles
        articles = [*Article.fetch_all(ctx, chapter.chapterid)]

        for article_index, article in enumerate(articles):
            # compute page boundaries
            article_first_page = article.articlepagenumber
            if article_index == len(articles) - 1:
                article_last_page = chapter_last_page
            else:
                article_last_page = articles[article_index + 1].articlepagenumber - 1

            # log
            print(
                f"\t{article.articletrans} {article_first_page} - {article_last_page}"
            )

            # make deck
            deck = genanki.Deck(
                deck_id=DECK_ID + deck_counter,
                name=f"{DECK_NAME}::{chapter.chaptertrans}::{article.articletrans}",
            )
            deck_counter += 1
            if package.decks is None:
                package.decks = []
            package.decks.append(deck)

            # include chapter card
            if article_index == 0:
                deck.add_note(make_note(ctx, chapter.to_entry()))

            # include article card
            # null string for some reason
            if article.articleaudioref == NULL_STRING:
                continue

            deck.add_note(
                make_note(
                    ctx,
                    article.to_entry(),
                )
            )

            # get words and sections
            for entry in fetch_all_ordered(
                ctx,
                chapters=False,
                articles=False,
                page_min=article_first_page,
                page_max=article_last_page,
            ):
                # null string for some reason
                if entry.audio == NULL_STRING:
                    continue

                # log
                if entry.row_type == "word":
                    print(f"\t\t{entry.back} {entry.page_number}")
                elif entry.row_type == "section":
                    print(f"\t\t--- {entry.back} --- {entry.page_number}")

                # add note
                deck.add_note(make_note(ctx, entry))


# export the package
package.write_to_file(OUTPUT_FILE)
