import sqlite3

import genanki

from schema import Article, Chapter, Context
from utils import fetch_all_ordered, log, make_note

# config
AUDIO_DIR = "audio/ukrainian"
DB_FILE = "db/ukrainian-us.sqlite3"

DECK_NAME = "Ukrainian Visual Dictionary"
OUTPUT_FILE = "out/ukrainian-english.apkg"

# read deck id from file
with open("deck-id.txt") as f:
    DECK_ID = int(f.read())

print(DECK_ID)
exit()
# create a package
package = genanki.Package([])

# to make mypy happy
if package.decks is None:
    package.decks = []

# connect to the database
with sqlite3.connect(DB_FILE) as conn:
    conn.row_factory = sqlite3.Row

    ctx = Context(AUDIO_DIR=AUDIO_DIR, conn=conn, package=package)

    # get chapters
    chapters_with_duplicates = [*Chapter.fetch_all(ctx)]

    # remove duplicates (transportation chapter is duplicated in Ukrainian)
    chapters: list[Chapter] = []
    seen_names = set()
    for chapter in chapters_with_duplicates:
        if chapter.chaptertrans in seen_names:
            continue
        seen_names.add(chapter.chaptertrans)
        chapters.append(chapter)

    # loop through chapters
    for i, chapter in enumerate(chapters):
        # compute page boundaries
        chapter_first_page = chapter.chapterpagenumber
        if i == len(chapters) - 1:
            chapter_last_page = 10000000000000000000000
        else:
            chapter_last_page = chapters[i + 1].chapterpagenumber - 1

        # log
        log(
            f"{chapter.chaptertrans} {chapter_first_page} - {chapter_last_page}",
            fg="red",
        )

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
            log(
                f"{article.articletrans} {article_first_page} - {article_last_page}",
                level=1,
                fg="blue",
            )

            # make deck
            deck = genanki.Deck(
                deck_id=DECK_ID + article.orderid,
                name=f"{DECK_NAME}::{chapter.chaptertrans}::{article.articletrans}",
            )
            package.decks.append(deck)

            # include chapter card
            if article_index == 0:
                deck.add_note(make_note(ctx, chapter.to_entry()))

            # include article card
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
                # log
                if entry.row_type == "word":
                    log(f"{entry.back} {entry.page_number}", level=2)
                elif entry.row_type == "section":
                    log(
                        f"--- {entry.back} --- {entry.page_number}", level=2, fg="white"
                    )

                # add note
                deck.add_note(make_note(ctx, entry))


# export the package
package.write_to_file(OUTPUT_FILE)
