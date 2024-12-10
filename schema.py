from dataclasses import dataclass
import genanki
import sqlite3
from typing import Literal, Optional


# context object
@dataclass
class Context:
    AUDIO_DIR: str
    conn: sqlite3.Connection
    package: genanki.Package


@dataclass()
class Entry:
    order_id: int
    row_type: Literal["article", "chapter", "section", "word"]
    front: str
    back: str
    audio: str
    page_number: int

    @staticmethod
    def from_row(row: sqlite3.Row):
        return Entry(
            order_id=row["order_id"],
            row_type=row["row_type"],
            front=row["front"],
            back=row["back"],
            audio=row["audio"],
            page_number=row["page_number"],
        )


# sqlite database
@dataclass
class Article:
    """
    Example:
    ```json
    {
        "articleaudioref": "bvd_ukrn012derkor_002_lang.m4a",
        "articleaudiotranref": "bvd_englis012derkor_002_USeng.m4a",
        "articleid": 1,
        "articleimageref": "(null)",
        "articlename": "тіло",
        "articlepagenumber": 12,
        "articlepron": "",
        "articlerefid": "BVD_ENGLIS012DERKOR_001",
        "articletrans": "body",
        "chapterid": 1,
        "isfav": 0,
        "orderid": 1
    }
    ```
    """

    # instance properties
    articleid: int
    "1"
    articlename: str
    "тіло"
    articletrans: str
    "body"
    articleimageref: Optional[str]
    "(null)"
    articleaudioref: str
    "bvd_ukrn012derkor_002_lang.m4a"
    articlerefid: str
    "BVD_ENGLIS012DERKOR_001"
    chapterid: int
    "1"
    articlepagenumber: int
    "12"
    orderid: int
    "1"
    articleaudiotranref: str
    "bvd_englis012derkor_002_USeng.m4a"
    isfav: int
    "0"
    articlepron: str
    ""

    # instance methods
    def to_entry(self):
        return Entry(
            order_id=self.orderid,
            row_type="article",
            front=self.articlename,
            back=self.articletrans,
            audio=self.articleaudioref,
            page_number=self.articlepagenumber,
        )

    # static properties
    entry_query = """
        SELECT
            orderid order_id,
            'article' row_type,
            articlename front,
            articletrans back,
            articleaudioref audio,
            articlepagenumber page_number
        FROM Article
        """

    # static methods
    @staticmethod
    def fetch_all(ctx: Context, chapter_id: Optional[int] = None):
        if chapter_id is not None:
            query = f"""
                SELECT * FROM article
                WHERE chapterid = {chapter_id} AND articletrans != '(null)'
                """
        else:
            query = Article.entry_query

        for row in ctx.conn.execute(query):
            yield Article.from_row(row)

    @staticmethod
    def from_row(row: sqlite3.Row):
        return Article(
            articleid=row["articleid"],
            articlename=row["articlename"],
            articletrans=row["articletrans"],
            articleimageref=row["articleimageref"],
            articleaudioref=row["articleaudioref"],
            articlerefid=row["articlerefid"],
            chapterid=row["chapterid"],
            articlepagenumber=row["articlepagenumber"],
            orderid=row["orderid"],
            articleaudiotranref=row["articleaudiotranref"],
            isfav=row["isfav"],
            articlepron=row["articlepron"],
        )

    @staticmethod
    def page_clause(
        page_min: Optional[int] = None, page_max: Optional[int] = None
    ) -> str:
        if page_min is not None and page_max is not None:
            return f"articlepagenumber BETWEEN {page_min} AND {page_max}"
        elif page_min is not None:
            return f"articlepagenumber >= {page_min}"
        elif page_max is not None:
            return f"articlepagenumber <= {page_max}"
        return ""


@dataclass
class Chapter:
    """
    ```json
    {
        "chapteraudioref": "bvd_ukrn010diemen_001_lang.m4a",
        "chapteraudiotranref": "bvd_englis010diemen_001_USeng.m4a",
        "chapterid": 1,
        "chapterimageref": "(null)",
        "chaptername": "люди",
        "chapterpagenumber": 10,
        "chapterpron": "",
        "chapterrefid": "BVD_ENGLIS010-027DIEMEN",
        "chaptertrans": "people",
        "isfav": 0,
        "orderID": 0
    }
    ```
    """

    # instance properties
    chapterid: int
    """1"""
    chaptername: str
    """люди"""
    chaptertrans: str
    """people"""
    chapterimageref: Optional[str]
    """(null)"""
    chapteraudioref: str
    """bvd_ukrn010diemen_001_lang.m4a"""
    chapterrefid: str
    """BVD_ENGLIS010-027DIEMEN"""
    chapterpagenumber: int
    """10"""
    chapterpron: str
    """""" ""
    chapteraudiotranref: str
    """bvd_englis010diemen_001_USeng.m4a"""
    isfav: int
    """0"""
    orderID: int
    """0"""

    # instance methods
    def to_entry(self):
        return Entry(
            order_id=self.orderID,
            row_type="chapter",
            front=self.chaptername,
            back=self.chaptertrans,
            audio=self.chapteraudioref,
            page_number=self.chapterpagenumber,
        )

    # static properties
    entry_query = """
        SELECT
            orderID order_id,
            'chapter' row_type,
            chaptername front,
            chaptertrans back,
            chapteraudioref audio,
            chapterpagenumber page_number
        FROM Chapter
        """

    # static methods
    @staticmethod
    def fetch_all(ctx: Context):
        for row in ctx.conn.execute("SELECT * FROM chapter"):
            yield Chapter.from_row(row)

    @staticmethod
    def from_row(row: sqlite3.Row):
        return Chapter(
            chapterid=row["chapterid"],
            chaptername=row["chaptername"],
            chaptertrans=row["chaptertrans"],
            chapterimageref=row["chapterimageref"],
            chapteraudioref=row["chapteraudioref"],
            chapterrefid=row["chapterrefid"],
            chapterpagenumber=row["chapterpagenumber"],
            chapterpron=row["chapterpron"],
            chapteraudiotranref=row["chapteraudiotranref"],
            isfav=row["isfav"],
            orderID=row["orderID"],
        )

    @staticmethod
    def page_clause(
        page_min: Optional[int] = None, page_max: Optional[int] = None
    ) -> str:
        if page_min is not None and page_max is not None:
            return f"chapterpagenumber BETWEEN {page_min} AND {page_max}"
        elif page_min is not None:
            return f"chapterpagenumber >= {page_min}"
        elif page_max is not None:
            return f"chapterpagenumber <= {page_max}"
        return ""


@dataclass
class Word:
    """
    Example:
    ```json
    {
        "annotationid": 0,
        "isarticle": 1,
        "isfav": 0,
        "orderid": 2,
        "refid": 1,
        "wordaudioref": "bvd_ukrn012derkor_004_lang.m4a",
        "wordaudiotransref": "bvd_englis012derkor_004_USeng.m4a",
        "wordid": 1,
        "wordimageref": "",
        "wordname": "чоловіче",
        "wordpagenumber": 12,
        "wordpron": "",
        "wordrefid": "BVD_ENGLIS012DERKOR_003",
        "wordtrans": "male"
    }
    """

    # instance properties
    wordid: int
    """1"""
    annotationid: int
    """0"""
    wordname: str
    """чоловіче"""
    wordtrans: str
    """male"""
    wordimageref: str
    """""" ""
    wordaudioref: str
    """bvd_ukrn012derkor_004_lang.m4a"""
    wordrefid: str
    """BVD_ENGLIS012DERKOR_003"""
    wordpagenumber: int
    """12"""
    wordpron: str
    """""" ""
    wordaudiotransref: str
    """bvd_englis012derkor_004_USeng.m4a"""
    isarticle: int
    """1"""
    isfav: int
    """0"""
    orderid: int
    """2"""
    refid: int
    """1"""

    # static properties
    entry_query = """
        SELECT
            orderid order_id,
            'word' row_type,
            wordname front,
            wordtrans back,
            wordaudioref audio,
            wordpagenumber page_number
        FROM Word
        """

    # static methods
    @staticmethod
    def from_row(row: sqlite3.Row):
        return Word(
            wordid=row["wordid"],
            wordname=row["wordname"],
            wordtrans=row["wordtrans"],
            wordimageref=row["wordimageref"],
            wordaudioref=row["wordaudioref"],
            wordrefid=row["wordrefid"],
            wordpagenumber=row["wordpagenumber"],
            wordpron=row["wordpron"],
            wordaudiotransref=row["wordaudiotransref"],
            annotationid=row["annotationid"],
            isarticle=row["isarticle"],
            isfav=row["isfav"],
            orderid=row["orderid"],
            refid=row["refid"],
        )

    @staticmethod
    def page_clause(
        page_min: Optional[int] = None, page_max: Optional[int] = None
    ) -> str:
        if page_min is not None and page_max is not None:
            return f"wordpagenumber BETWEEN {page_min} AND {page_max}"
        elif page_min is not None:
            return f"wordpagenumber >= {page_min}"
        elif page_max is not None:
            return f"wordpagenumber <= {page_max}"
        return ""


@dataclass
class Section:
    """
    Example:
    ```json
    {
        "articleid": 2,
        "isfav": 0,
        "orderid": 55,
        "sectionaudioref": "bvd_ukrn014dasges_050_lang.m4a",
        "sectionaudiotransref": "bvd_englis014dasges_050_USeng.m4a",
        "sectionid": 1,
        "sectionimageref": "(null)",
        "sectionname": "кисть",
        "sectionpagenumber": 14,
        "sectionpron": "",
        "sectionrefid": "BVD_ENGLIS014DASGES_049",
        "sectiontrans": "hand"
    }
    ```
    """

    # instance properties
    sectionid: int
    """1"""
    sectionname: str
    """кисть"""
    sectiontrans: str
    """hand"""
    sectionimageref: Optional[str]
    """(null)"""
    sectionaudioref: str
    """bvd_ukrn014dasges_050_lang.m4a"""
    sectionrefid: str
    """BVD_ENGLIS014DASGES_049"""
    sectionpagenumber: int
    """14"""
    sectionpron: str
    """""" ""
    sectionaudiotransref: str
    """bvd_englis014dasges_050_USeng.m4a"""
    articleid: int
    """2"""
    isfav: int
    """0"""
    orderid: int
    """55"""

    # instance methods
    def to_entry(self):
        return Entry(
            order_id=self.orderid,
            row_type="section",
            front=self.sectionname,
            back=self.sectiontrans,
            audio=self.sectionaudioref,
            page_number=self.sectionpagenumber,
        )

    # static properties
    entry_query = """
        SELECT
            orderid order_id,
            'section' row_type,
            sectionname front,
            sectiontrans back,
            sectionaudioref audio,
            sectionpagenumber page_number
        FROM section
        """

    # static methods
    @staticmethod
    def from_row(row: sqlite3.Row):
        return Section(
            sectionid=row["sectionid"],
            sectionname=row["sectionname"],
            sectiontrans=row["sectiontrans"],
            sectionimageref=row["sectionimageref"],
            sectionaudioref=row["sectionaudioref"],
            sectionrefid=row["sectionrefid"],
            sectionpagenumber=row["sectionpagenumber"],
            sectionpron=row["sectionpron"],
            sectionaudiotransref=row["sectionaudiotransref"],
            articleid=row["articleid"],
            isfav=row["isfav"],
            orderid=row["orderid"],
        )

    @staticmethod
    def page_clause(
        page_min: Optional[int] = None, page_max: Optional[int] = None
    ) -> str:
        if page_min is not None and page_max is not None:
            return f"sectionpagenumber BETWEEN {page_min} AND {page_max}"
        elif page_min is not None:
            return f"sectionpagenumber >= {page_min}"
        elif page_max is not None:
            return f"sectionpagenumber <= {page_max}"
        return ""
