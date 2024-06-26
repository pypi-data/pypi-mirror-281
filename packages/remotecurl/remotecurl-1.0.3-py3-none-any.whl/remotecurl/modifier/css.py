"""This file contain a CSS modifier class"""


from typing import Optional
from re import Match, sub, MULTILINE
from remotecurl.modifier.abstract import Modifier
from remotecurl.common.util import remove_quote


class CSSModifier(Modifier):
    """A CSS modifier"""

    css: str

    def __init__(
        self, css: bytes, url: str, base_url: str = "", encoding: Optional[str] = None,
        allow_url_rules: list[str] = ["^(.*)$"], deny_url_rules: list[str] = []
    ) -> None:
        """Initialize a CSS modifier"""
        self.css = css.decode(encoding) 
        super().__init__(url, base_url, encoding, allow_url_rules, deny_url_rules)

    def _get_new_url_string(self, mobj: Match) -> str:
        url = remove_quote(mobj.group(1))
        whole_matched = mobj.group(0)
        front, back = whole_matched.split(url, 1)
        url = self._modify_link(url)
        return front + url + back

    def _modify_css(self) -> None:
        """Modify css content"""
        self.css = sub(r"url\(([^)]+)\)", self._get_new_url_string, self.css, flags=MULTILINE)

    def get_modified_content(self) -> bytes:
        """Return a tuple of css content bytes and encoding"""
        self._modify_css()
        return bytes(self.css, self.encoding)
