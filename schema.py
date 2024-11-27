from dataclasses import dataclass
import sqlite3
from typing import Optional


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

    articleid: int
    """1"""
    articlename: str
    """тіло"""
    articletrans: str
    """body"""
    articleimageref: Optional[str]
    """(null)"""
    articleaudioref: str
    """bvd_ukrn012derkor_002_lang.m4a"""
    articlerefid: str
    """BVD_ENGLIS012DERKOR_001"""
    chapterid: int
    """1"""
    articlepagenumber: int
    """12"""
    orderid: int
    """1"""
    articleaudiotranref: str
    """bvd_englis012derkor_002_USeng.m4a"""
    isfav: int
    """0"""
    articlepron: str
    """""" ""

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
