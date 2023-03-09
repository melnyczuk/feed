from datetime import datetime, timezone

from feedgen.feed import FeedEntry, FeedGenerator
from markdown import markdown


class Rss:
    __client = FeedGenerator()

    def __init__(
        self: "Rss",
        url: str,
        author: str,
        email: str,
        title: str,
        description: str,
    ) -> None:
        self.__client.id(url)
        self.__client.author(name=author, email=email)
        self.__client.title(title)
        self.__client.description(description)
        self.__client.language("en")
        self.__client.link(href=url, rel="self")

    def generate_xml(self: "Rss", path: str) -> None:
        print(f"Saving rss xml to {path}")
        return self.__client.rss_file(path, pretty=True)

    @property
    def title(self: "Rss") -> str:
        return self.__client.title()

    @property
    def url(self: "Rss") -> str:
        return self.__client.id()

    @property
    def entries(self: "Rss") -> list[FeedEntry]:
        return self.__client.entry()

    def clear_entries(self: "Rss") -> None:
        self.__client.entry([], replace=True)

    def add_image(
        self: "Rss",
        title: str,
        description: str,
        date: datetime,
        url: str,
        length: int,
        type: str,
    ) -> None:
        _entry = self.__add_entry(
            title=title, description=description, date=date
        )
        _entry.enclosure(url=url, length=str(length), type=type)
        _entry.rss_entry()

    def add_text(
        self: "Rss", title: str, description: str, date: datetime, content: str
    ) -> None:
        _entry = self.__add_entry(
            title=title, description=description, date=date
        )
        _entry.content(content=markdown(content), type="text/html")
        _entry.rss_entry()

    def __add_entry(
        self: "Rss", title: str, description: str, date: datetime
    ) -> FeedEntry:
        _date = (
            date
            if date.tzinfo is not None
            else date.replace(tzinfo=timezone.utc)
        )

        _entry = self.__client.add_entry()
        _entry.title(title)
        _entry.description(description)
        _entry.published(_date)
        _entry.updated(_date)
        return _entry
