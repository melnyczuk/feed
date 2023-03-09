from datetime import datetime

from src.rss import Rss


class TestRss:
    rss = Rss(
        url="https://test.test/rss",
        title="Test",
        description="a test RSS feed",
        author="How Melnyczuk",
        email="how@test.test",
    )

    def test_url(self):
        assert self.rss.url == "https://test.test/rss"

    def test_title(self):
        assert self.rss.title == "Test"

    def test_clear_entries(self):
        assert len(self.rss.entries) == 0

        self.rss.add_image(
            title="test",
            description="test description",
            date=datetime(2023, 3, 6, 14, 44, 34),
            url="https://test.com",
            length="3322517",
            type="image/jpg",
        )

        assert len(self.rss.entries) == 1

        self.rss.clear_entries()

        assert len(self.rss.entries) == 0

    def test_add_image(self):
        self.rss.clear_entries()

        self.rss.add_image(
            title="test image",
            description="image image image",
            date=datetime(2023, 3, 6, 14, 44, 34),
            url="https://dl.dropbox.com/s/n0wuj80nwqslcsu/image.jpg",
            length=3322517,
            type="image/jpg",
        )

        entries = self.rss.entries
        assert len(entries) == 1

        entry = entries[0]

        enclosure = entry.enclosure()
        assert (
            enclosure["url"]
            == "https://dl.dropbox.com/s/n0wuj80nwqslcsu/image.jpg"
        )
        assert enclosure["length"] == "3322517"

        links = entry.link()
        assert len(links) == 1

        link = links[0]
        assert (
            link["href"] == "https://dl.dropbox.com/s/n0wuj80nwqslcsu/image.jpg"
        )

        assert str(entry.pubDate()) == "2023-03-06 14:44:34+00:00"

    def test_add_text(self):
        self.rss.clear_entries()

        self.rss.add_text(
            title="test text",
            description="text text text",
            date=datetime(2023, 3, 6, 14, 44, 34),
            content="## Test\n\nThis is a test file\n",
        )

        entries = self.rss.entries
        assert len(entries) == 1

        entry = entries[0]

        content = entry.content()
        assert content["content"] == "<h2>Test</h2>\n<p>This is a test file</p>"

        assert str(entry.pubDate()) == "2023-03-06 14:44:34+00:00"
