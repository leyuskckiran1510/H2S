import os
import logging
from typing import List, Dict
from bs4 import BeautifulSoup, Tag
from h2s import Har, _entry, _Content, _Request


logging.basicConfig(
    format="[%(asctime)s] %(message)s",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.info("Initializing....")


LOW: Dict[str, List] = {"text": ["html"]}
MID: Dict[str, List] = {"multipart": ["form-data", "related"], "text": ["*"]}
HIGH: Dict[str, List] = {
    "application": [
        "javascript",
        "x-javascript",
        "json",
        "xml",
        "xhtml+xml",
        "x-www-form-urlencoded",
        "pgp",
        "pgp-signature",
        "x-perl",
        "x-python",
        "x-shellscript",
        "yaml",
    ],
    "message": ["*"],
    "multipart": ["*"],
    "text": ["*"],
}
INSANE: Dict[str, List] = {
    "application": ["*"],
    "audio": ["*"],
    "font": ["*"],
    "image": ["*"],
    "message": ["*"],
    "model": ["*"],
    "multipart": ["*"],
    "text": ["*"],
    "video": ["*"],
}


LEVEL = LOW


class ParseJs:
    def __init__(self, html, text) -> None:
        self.soup = BeautifulSoup(html, "html5lib").find("body")
        self.to_match = text
        assert isinstance(self.soup, Tag)
        self.childs = self.soup.findChildren()
        self.matcher = []
        self.parseit()

    def parseit(self, state=None):
        print(self.childs)


class ParseHTML:
    def __init__(self, html, text) -> None:
        self.soup = BeautifulSoup(html, "html5lib").find("body")
        self.to_match = text
        assert isinstance(self.soup, Tag)
        self.childs = self.soup.findChildren()
        self.matcher = []
        self.parseit()

    def parseit(self, state=None):
        print(self.childs[0].__dir__())
        for i in self.childs:
            if self.to_match in i.text:
                self.matcher.append((i.name, i.attrs))
        print(self.matcher)


def conAnalyzer(content: _Content, sample: str):
    __cont = str(content.content)
    if sample not in __cont:
        return None
    if content.mimeType == "text/html":
        parser_obj = ParseHTML(__cont, sample)
    elif content.mimeType == "application/x-javascript":
        parser_obj = ParseJS(__cont, sample)
    else:
        parser_obj = None
    return parser_obj


def reqAnalyzer(reqs: _Request):
    ...


def resAnalyzer(entry: _entry, sample: str):
    if not entry.response._content:
        return [None, None]
    conA = conAnalyzer(entry.response._content, sample)
    if not conA:
        return [None, None]
    reqA = reqAnalyzer(entry.request)
    return [conA, reqA]


def cleaner(entries: List[_entry]) -> List[_entry]:
    logging.info("Removing Unnecessary Entries...")
    __temp: List[_entry] = []
    for i in entries:
        mime: str = str(i.response._content.mimeType)  # type/subtype
        m_split = str(mime).split("/")
        if (m_split[0] in LEVEL) and (m_split[-1] in LEVEL[m_split[0]] or LEVEL[m_split[0]][0] == "*"):
            __temp.append(i)
    return __temp


def prepear(filename: str, sample: str):
    if not os.path.exists(filename):
        raise FileNotFoundError("please double check the file name")
    _har = Har(filename=filename)
    sample = sample.strip()
    logging.info("Http Archive Extracted Sucessfully")
    cleaned: List[_entry] = cleaner(_har.entries())
    operations = []
    for i in cleaned:
        operations.append(resAnalyzer(i, sample=sample))
    print(operations)


LEVEL = HIGH
prepear("test.har", "Fifty shades of neigh!")
