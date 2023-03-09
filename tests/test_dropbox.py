from os import getenv

from src.dropbox import Dropbox


class TestDropbox:
    dropbox = Dropbox(token=getenv("DROPBOX_TOKEN", ""))

    def test_substitute_query_params(self):
        result = self.dropbox.substitute_query_params("www.test.com?dl=0")
        assert result == "dl.test.com"

    def test_list_dir(self):
        result = self.dropbox.list_dir("/feed/test")
        assert len(result) == 2
        assert result[0].name == "image.jpg"
        assert result[1].name == "text.md"

    def test_generate_url(self):
        result = self.dropbox.generate_url("/feed/test/image.jpg")
        assert result == "https://dl.dropbox.com/s/n0wuj80nwqslcsu/image.jpg"

    def test_get_metadata(self):
        result = self.dropbox.get_metadata("/feed/test/image.jpg")
        assert result.name == "image.jpg"
        assert result.size == 3322517

    def test_get_content(self):
        result = self.dropbox.get_content("/feed/test/text.md")
        print(result)
        assert result == "## Test\n\nThis is a test file\n"
