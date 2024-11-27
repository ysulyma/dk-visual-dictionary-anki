import genanki
import sqlite3
from typing import List

# config
AUDIO_DIR = "audio"
DECK_ID = 1892930485
DECK_NAME = "Ukrainian Visual Dictionary"
OUTPUT_FILE = "output.apkg"

# don't change this
NULL_STRING = "(null)"


def make_note(front: str, back: str, audio: str, tags: List[str]):
    """
    Makes a note
    """
    return genanki.Note(
        model=genanki.BASIC_AND_REVERSED_CARD_MODEL,
        fields=[f"{front}<br>[sound:{audio}]", back],
        tags=tags,
    )


# create a deck
deck = genanki.Deck(DECK_ID, DECK_NAME)

# create a package
package = genanki.Package(deck)

# connect to the database
with sqlite3.connect("db.sqlite3") as conn:
    conn.row_factory = sqlite3.Row

    cursor = conn.execute(
        """
            -- chapter
            SELECT
                orderID order_id,
                'chapter' row_type,
                chaptername front,
                chaptertrans back,
                chapteraudioref audio,
                chapterpagenumber page_number
            FROM Chapter
        UNION
            -- article
            SELECT
                orderid order_id,
                'article' row_type,
                articlename front,
                articletrans back,
                articleaudioref audio,
                articlepagenumber page_number
            FROM Article
        UNION
            -- section
            SELECT
                orderid order_id,
                'section' row_type,
                sectionname front,
                sectiontrans back,
                sectionaudioref audio,
                sectionpagenumber page_number
            FROM section
        UNION
            -- word
            SELECT
                orderid order_id,
                'word' row_type,
                wordname front,
                wordtrans back,
                wordaudioref audio,
                wordpagenumber page_number
            FROM Word
        ORDER BY order_id
        """
    )

    for row in cursor:
        audio = row["audio"]
        back = row["back"]
        front = row["front"]
        page_number = row["page_number"]
        type = row["row_type"]

        if audio == NULL_STRING:
            continue

        # add audio
        package.media_files.append(f"{AUDIO_DIR}/{audio}")

        # add note
        deck.add_note(
            make_note(
                front=front,
                back=back,
                audio=audio,
                tags=[f"page:{page_number}"],
            )
        )


# export the package
package.write_to_file(OUTPUT_FILE)
